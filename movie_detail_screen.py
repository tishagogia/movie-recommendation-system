"""
Movie Detail Screen module for the Movie Recommendation System
"""
import tkinter as tk
from tkinter import ttk
import re

from config import BG_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, TEXT_COLOR, TEXT_COLOR_LIGHT
from screens.base_screen import BaseScreen
from ui_components import (
    ScrollableFrame, MovieCard, RatingWidget, HoverButton
)
from utils import extract_names_from_dict_list
from assets.styles import (
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE,
    LABEL_STYLE, BUTTON_STYLE, ACCENT_BUTTON_STYLE
)

class MovieDetailScreen(BaseScreen):
    """Screen for displaying detailed information about a movie"""
    
    def __init__(self, parent, data_handler, user_manager, recommender, **kwargs):
        # Extract callbacks before passing to super()
        self.on_add_watchlist = kwargs.pop('on_add_watchlist', None)
        self.on_add_bookmark = kwargs.pop('on_add_bookmark', None)
        self.on_movie_click = kwargs.pop('on_movie_click', None)
        
        # Initialize the base screen
        super().__init__(parent, data_handler, user_manager, **kwargs)
        
        # Store the recommender
        self.recommender = recommender
        
        # Current movie
        self.movie_id = None
        self.movie = None
        
        # Set screen title
        self.set_title("Movie Details")
        
        # Initialize the UI
        self._create_ui()
    
    def set_movie(self, movie_id):
        """Set the movie to display"""
        self.movie_id = movie_id
        self.movie = self.data_handler.get_movie_by_id(movie_id)
        
        if self.movie:
            self.set_title(self.movie.get('title', 'Movie Details'))
            self.update_screen()
        else:
            self.set_status(f"Error: Movie with ID {movie_id} not found")
    
    def _create_ui(self):
        """Create the movie detail UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if not self.movie:
            # Show a message if no movie is selected
            no_movie_label = tk.Label(
                self.content_frame,
                text="No movie selected",
                font=("Helvetica", 14),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=50
            )
            no_movie_label.pack(expand=True)
            return
        
        # Create a scrollable frame for the content
        self.scroll_frame = ScrollableFrame(self.content_frame, bg=BG_COLOR)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main detail container
        detail_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR,
            padx=PADDING_LARGE,
            pady=PADDING_LARGE
        )
        detail_container.pack(fill=tk.BOTH, expand=True)
        
        # Top section with poster and basic info
        top_frame = tk.Frame(detail_container, bg=BG_COLOR)
        top_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Left side - poster placeholder
        poster_frame = tk.Frame(
            top_frame,
            bg=PRIMARY_COLOR,
            width=250,
            height=375
        )
        poster_frame.pack(side=tk.LEFT, padx=PADDING_MEDIUM)
        poster_frame.pack_propagate(False)
        
        # Add a placeholder image or icon
        poster_label = tk.Label(
            poster_frame, 
            text="🎬",
            font=("Helvetica", 48),
            bg=PRIMARY_COLOR,
            fg=BG_COLOR
        )
        poster_label.pack(fill=tk.BOTH, expand=True)
        
        # Right side - movie info
        info_frame = tk.Frame(top_frame, bg=BG_COLOR, padx=PADDING_MEDIUM)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            info_frame,
            text=self.movie.get('title', 'Unknown Title'),
            font=("Helvetica", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            wraplength=500,
            justify=tk.LEFT,
            anchor='w'
        )
        title_label.pack(fill=tk.X, anchor='w', pady=(0, PADDING_MEDIUM))
        
        # Release year
        year = self.movie.get('release_year', '')
        if not year and 'release_date' in self.movie:
            year_match = re.search(r'(\d{4})', str(self.movie['release_date']))
            if year_match:
                year = year_match.group(1)
        
        if year:
            year_label = tk.Label(
                info_frame,
                text=f"Release Year: {year}",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w'
            )
            year_label.pack(fill=tk.X, anchor='w', pady=(0, PADDING_SMALL))
        
        # Rating
        rating_frame = tk.Frame(info_frame, bg=BG_COLOR)
        rating_frame.pack(fill=tk.X, anchor='w', pady=PADDING_SMALL)
        
        rating_label = tk.Label(
            rating_frame,
            text="Rating: ",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        rating_label.pack(side=tk.LEFT)
        
        rating_value = self.movie.get('vote_average', 0)
        rating_widget = RatingWidget(
            rating_frame,
            rating=rating_value / 2,  # Convert 10-scale to 5-scale
            bg=BG_COLOR
        )
        rating_widget.pack(side=tk.LEFT)
        
        vote_count = self.movie.get('vote_count', 0)
        vote_label = tk.Label(
            rating_frame,
            text=f"({vote_count} votes)",
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT,
            anchor='w'
        )
        vote_label.pack(side=tk.LEFT, padx=(PADDING_SMALL, 0))
        
        # Genres
        genres = self.movie.get('genres', '')
        if genres:
            if isinstance(genres, list):
                genres_text = ", ".join(genres)
            else:
                genres_text = str(genres)
            
            genres_label = tk.Label(
                info_frame,
                text=f"Genres: {genres_text}",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w',
                wraplength=500,
                justify=tk.LEFT
            )
            genres_label.pack(fill=tk.X, anchor='w', pady=(0, PADDING_SMALL))
        
        # Runtime
        runtime = self.movie.get('runtime', 0)
        if runtime:
            runtime_label = tk.Label(
                info_frame,
                text=f"Runtime: {runtime} minutes",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w'
            )
            runtime_label.pack(fill=tk.X, anchor='w', pady=(0, PADDING_SMALL))
        
        # Director
        director = self.movie.get('director', '')
        if director:
            director_label = tk.Label(
                info_frame,
                text=f"Director: {director}",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w',
                wraplength=500,
                justify=tk.LEFT
            )
            director_label.pack(fill=tk.X, anchor='w', pady=(0, PADDING_SMALL))
        
        # Action buttons
        action_frame = tk.Frame(info_frame, bg=BG_COLOR)
        action_frame.pack(fill=tk.X, anchor='w', pady=PADDING_MEDIUM)
        
        # Add to Watchlist button
        watchlist_button = HoverButton(
            action_frame,
            text="Add to Watchlist",
            **BUTTON_STYLE,
            command=self._handle_add_watchlist
        )
        watchlist_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Add to Bookmarks button
        bookmark_button = HoverButton(
            action_frame,
            text="Bookmark",
            **BUTTON_STYLE,
            command=self._handle_add_bookmark
        )
        bookmark_button.pack(side=tk.LEFT)
        
        # Overview section
        overview_frame = tk.Frame(detail_container, bg=BG_COLOR)
        overview_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        overview_header = tk.Label(
            overview_frame,
            text="Overview",
            font=("Helvetica", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        overview_header.pack(fill=tk.X, anchor='w', pady=(0, PADDING_SMALL))
        
        overview_text = self.movie.get('overview', 'No overview available')
        overview_label = tk.Label(
            overview_frame,
            text=overview_text,
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w',
            wraplength=700,
            justify=tk.LEFT
        )
        overview_label.pack(fill=tk.X, anchor='w')
        
        # Cast section
        cast = self.movie.get('cast_list', [])
        if cast:
            cast_frame = tk.Frame(detail_container, bg=BG_COLOR)
            cast_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
            
            cast_header = tk.Label(
                cast_frame,
                text="Cast",
                font=("Helvetica", 14, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w'
            )
            cast_header.pack(fill=tk.X, anchor='w', pady=(0, PADDING_SMALL))
            
            # Show first 10 cast members
            cast_text = ", ".join(cast[:10])
            if len(cast) > 10:
                cast_text += f"... and {len(cast) - 10} more"
                
            cast_label = tk.Label(
                cast_frame,
                text=cast_text,
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w',
                wraplength=700,
                justify=tk.LEFT
            )
            cast_label.pack(fill=tk.X, anchor='w')
        
        # Similar Movies section
        similar_header = tk.Label(
            detail_container,
            text="Similar Movies",
            font=("Helvetica", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        similar_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_SMALL))
        
        # Get similar movies
        similar_movies = self.recommender.get_similar_movies(self.movie_id, 5)
        
        # Container for similar movie cards
        similar_container = tk.Frame(detail_container, bg=BG_COLOR)
        similar_container.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Add similar movie cards
        for movie in similar_movies:
            card = MovieCard(
                similar_container,
                movie=movie,
                on_click=self.on_movie_click,
                width=180,
                height=280,
                bg=BG_COLOR
            )
            card.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Set status
        self.set_status(f"Viewing details for: {self.movie.get('title', 'Unknown Movie')}")
    
    def _handle_add_watchlist(self):
        """Handle adding the movie to watchlist"""
        if not self.user_manager.get_current_user():
            self.set_status("You must be logged in to add movies to your watchlist")
            return
        
        if self.on_add_watchlist and self.movie:
            self.on_add_watchlist(self.movie)
    
    def _handle_add_bookmark(self):
        """Handle adding the movie to bookmarks"""
        if not self.user_manager.get_current_user():
            self.set_status("You must be logged in to bookmark movies")
            return
        
        if self.on_add_bookmark and self.movie:
            self.on_add_bookmark(self.movie)
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Recreate UI to reflect any changes
        self._create_ui()
