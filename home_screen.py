"""
Home Screen module for the Movie Recommendation System
"""
import tkinter as tk
from tkinter import ttk

from config import TRENDING_MOVIES_COUNT, POPULAR_MOVIES_COUNT, BG_COLOR
from screens.base_screen import BaseScreen
from ui_components import (
    ScrollableFrame, SearchBar, MovieCard
)
from assets.styles import (
    PADDING_MEDIUM, PADDING_LARGE, SUBHEADER_STYLE
)

class HomeScreen(BaseScreen):
    """Home screen showing trending and popular movies"""
    
    def __init__(self, parent, data_handler, user_manager, recommender, **kwargs):
        # Extract callbacks before passing to super()
        self.on_movie_click = kwargs.pop('on_movie_click', None)
        self.on_search = kwargs.pop('on_search', None)
        
        # Initialize the base screen
        super().__init__(parent, data_handler, user_manager, **kwargs)
        
        # Store the recommender
        self.recommender = recommender
        
        # Set screen title
        self.set_title("MovieMaster")
        
        # Initialize the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the home screen UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create a search bar
        genres = self.data_handler.get_all_genres()
        self.search_bar = SearchBar(
            self.content_frame,
            on_search=self._handle_search,
            genres=genres,
            bg=BG_COLOR
        )
        self.search_bar.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Create a scrollable frame for movie sections
        self.scroll_frame = ScrollableFrame(self.content_frame, bg=BG_COLOR)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Get user for personalized recommendations
        self.user = self.user_manager.get_current_user()
        
        # First show any personalized content for logged-in users
        if self.user:
            self._create_personalized_section()
            self._create_watchlist_recommendations()
            # Add a hybrid recommendation section if user has a watchlist
            watchlist = self.user_manager.get_watchlist()
            if watchlist:
                self._create_hybrid_recommendations(watchlist)
        
        # Then show general sections for all users
        self._create_trending_section()
        self._create_popular_section()
        self._create_genre_based_recommendations()
        
        # Set status
        self.set_status("Ready")
    
    def _create_trending_section(self):
        """Create the trending movies section"""
        # Section header
        trending_header = tk.Label(
            self.scroll_frame.scrollable_frame,
            text="Trending Movies",
            **SUBHEADER_STYLE
        )
        trending_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_MEDIUM))
        
        # Get trending movies
        trending_movies = self.recommender.get_trending_recommendations(TRENDING_MOVIES_COUNT)
        
        # Create trending movies container
        trending_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        trending_container.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Add movie cards
        self._add_movie_cards(trending_container, trending_movies)
    
    def _create_popular_section(self):
        """Create the popular movies section"""
        # Section header
        popular_header = tk.Label(
            self.scroll_frame.scrollable_frame,
            text="Popular Movies",
            **SUBHEADER_STYLE
        )
        popular_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_MEDIUM))
        
        # Get popular movies
        popular_movies = self.recommender.get_popular_recommendations(POPULAR_MOVIES_COUNT)
        
        # Create popular movies container
        popular_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        popular_container.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Add movie cards
        self._add_movie_cards(popular_container, popular_movies)
    
    def _create_personalized_section(self):
        """Create personalized recommendations section"""
        # Section header
        personal_header = tk.Label(
            self.scroll_frame.scrollable_frame,
            text="Recommended for You",
            **SUBHEADER_STYLE
        )
        personal_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_MEDIUM))
        
        # Get user preferences
        user_preferences = self.user.get('profile', {}).get('preferences', {})
        
        # Get personalized recommendations
        personal_movies = self.recommender.get_personalized_recommendations(
            user_preferences, POPULAR_MOVIES_COUNT
        )
        
        # Create recommendations container
        personal_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        personal_container.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Add movie cards
        self._add_movie_cards(personal_container, personal_movies)
    
    def _create_watchlist_recommendations(self):
        """Create recommendations based on watchlist"""
        # Get user's watchlist
        watchlist = self.user_manager.get_watchlist()
        
        # Only show section if watchlist has items
        if not watchlist:
            return
        
        # Section header
        watchlist_header = tk.Label(
            self.scroll_frame.scrollable_frame,
            text="Because You Watchlisted",
            **SUBHEADER_STYLE
        )
        watchlist_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_MEDIUM))
        
        # Get recommendations based on watchlist
        watchlist_recs = self.recommender.get_recommendations_for_watchlist(
            watchlist, POPULAR_MOVIES_COUNT
        )
        
        # Create recommendations container
        watchlist_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        watchlist_container.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Add movie cards
        self._add_movie_cards(watchlist_container, watchlist_recs)
        
    def _create_hybrid_recommendations(self, watchlist):
        """Create recommendations using the hybrid recommendation algorithm"""
        if not watchlist:
            return
            
        # Section header with explanation of advanced algorithm
        hybrid_header = tk.Label(
            self.scroll_frame.scrollable_frame,
            text="AI-Powered Recommendations",
            **SUBHEADER_STYLE
        )
        hybrid_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_MEDIUM))
        
        # Add explanation text
        explanation = tk.Label(
            self.scroll_frame.scrollable_frame,
            text="Using advanced machine learning to find movies you'll love",
            font=("Helvetica", 10, "italic"),
            bg=BG_COLOR,
            fg="#666666"
        )
        explanation.pack(fill=tk.X, anchor='w', padx=PADDING_MEDIUM)
        
        # Get hybrid recommendations
        hybrid_recs = self.recommender.get_hybrid_recommendations(
            watchlist, POPULAR_MOVIES_COUNT
        )
        
        # Create recommendations container
        hybrid_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        hybrid_container.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Add movie cards
        self._add_movie_cards(hybrid_container, hybrid_recs)
        
    def _create_genre_based_recommendations(self):
        """Create recommendations based on popular genres"""
        # Get all genres
        all_genres = self.data_handler.get_all_genres()
        
        if not all_genres:
            return
            
        # Select top genres to show (limit to 3 to avoid cluttering the UI)
        top_genres = all_genres[:3] if len(all_genres) > 3 else all_genres
        
        # For each genre, show a row of movies
        for genre in top_genres:
            # Create section header for the genre
            genre_header = tk.Label(
                self.scroll_frame.scrollable_frame,
                text=f"Popular in {genre}",
                **SUBHEADER_STYLE
            )
            genre_header.pack(fill=tk.X, anchor='w', pady=(PADDING_LARGE, PADDING_MEDIUM))
            
            # Search for movies with this genre
            genre_movies = self.data_handler.search_movies(
                filters={"genres": [genre]},
                limit=POPULAR_MOVIES_COUNT
            )
            
            # Create movie container
            genre_container = tk.Frame(
                self.scroll_frame.scrollable_frame,
                bg=BG_COLOR
            )
            genre_container.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
            
            # Add movie cards
            self._add_movie_cards(genre_container, genre_movies)
    
    def _add_movie_cards(self, container, movies):
        """Add movie cards to a container"""
        if not movies:
            # Display a message if no movies
            no_movies_label = tk.Label(
                container,
                text="No movies available",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg="#666666",
                pady=20
            )
            no_movies_label.pack()
            return
        
        # Create a horizontal frame for the movie cards
        cards_frame = tk.Frame(container, bg=BG_COLOR)
        cards_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add each movie card
        for movie in movies:
            card = MovieCard(
                cards_frame,
                movie=movie,
                on_click=self.on_movie_click,
                width=180,
                height=280,
                bg=BG_COLOR
            )
            card.pack(side=tk.LEFT, padx=10, pady=10)
    
    def _handle_search(self, query, filters):
        """Handle search requests"""
        if self.on_search:
            self.on_search(query, filters)
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Recreate UI to reflect any changes
        self._create_ui()
