"""
Search Screen module for the Movie Recommendation System
"""
import tkinter as tk
from tkinter import ttk
import math

from config import BG_COLOR, SEARCH_RESULT_LIMIT
from screens.base_screen import BaseScreen
from ui_components import (
    ScrollableFrame, SearchBar, MovieCard
)
from assets.styles import (
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE,
    TEXT_COLOR, TEXT_COLOR_LIGHT
)

class SearchScreen(BaseScreen):
    """Screen for searching and filtering movies"""
    
    def __init__(self, parent, data_handler, user_manager, **kwargs):
        # Extract callbacks before passing to super()
        self.on_movie_click = kwargs.pop('on_movie_click', None)
        
        # Initialize the base screen
        super().__init__(parent, data_handler, user_manager, **kwargs)
        
        # Search parameters
        self.search_query = ""
        self.search_filters = {}
        
        # Set screen title
        self.set_title("Search Movies")
        
        # Initialize the UI
        self._create_ui()
    
    def set_search_params(self, query="", filters=None):
        """Set search parameters and perform search"""
        self.search_query = query if query else ""
        self.search_filters = filters if filters else {}
        self.update_screen()
    
    def _create_ui(self):
        """Create the search screen UI"""
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
        
        # Set initial search parameters
        if self.search_query:
            self.search_bar.search_var.set(self.search_query)
        
        if self.search_filters:
            # Set genre
            if 'genres' in self.search_filters:
                self.search_bar.genre_var.set(self.search_filters['genres'])
            
            # Set year range
            if 'year_from' in self.search_filters:
                self.search_bar.year_from_var.set(str(self.search_filters['year_from']))
            if 'year_to' in self.search_filters:
                self.search_bar.year_to_var.set(str(self.search_filters['year_to']))
            
            # Set rating
            if 'min_rating' in self.search_filters:
                rating_str = str(int(self.search_filters['min_rating']))
                self.search_bar.rating_var.set(rating_str)
            
            # Set director/cast
            if 'director' in self.search_filters:
                self.search_bar.person_type_var.set("Director")
                self.search_bar.person_var.set(self.search_filters['director'])
            elif 'cast' in self.search_filters:
                self.search_bar.person_type_var.set("Cast")
                self.search_bar.person_var.set(self.search_filters['cast'])
        
        # Create a scrollable frame for search results
        self.results_frame = ScrollableFrame(self.content_frame, bg=BG_COLOR)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Results header
        self.results_header = tk.Label(
            self.results_frame.scrollable_frame,
            text="Search Results",
            font=("Helvetica", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        self.results_header.pack(fill=tk.X, anchor='w', pady=(0, PADDING_MEDIUM))
        
        # Perform search if we have parameters
        if self.search_query or self.search_filters:
            self._perform_search()
        else:
            # Show a message to start searching
            self._show_search_prompt()
    
    def _show_search_prompt(self):
        """Show a prompt to start searching"""
        prompt_frame = tk.Frame(self.results_frame.scrollable_frame, bg=BG_COLOR)
        prompt_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        prompt_label = tk.Label(
            prompt_frame,
            text="Enter search terms or set filters above to find movies",
            font=("Helvetica", 14),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT,
            pady=20
        )
        prompt_label.pack()
    
    def _perform_search(self):
        """Perform search with current parameters"""
        # Get search results
        results = self.data_handler.search_movies(
            self.search_query, 
            self.search_filters,
            SEARCH_RESULT_LIMIT
        )
        
        # Clear any existing results
        for widget in self.results_frame.scrollable_frame.winfo_children():
            if widget != self.results_header:
                widget.destroy()
        
        # Update results header
        result_count = len(results)
        if result_count == 0:
            self.results_header.config(text="No Results Found")
            
            # Show a no results message
            no_results_label = tk.Label(
                self.results_frame.scrollable_frame,
                text="Try adjusting your search terms or filters",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                pady=20
            )
            no_results_label.pack()
            
            self.set_status("No results found")
            return
        
        # Update header text
        count_text = f"{result_count} movie{'s' if result_count != 1 else ''}"
        if result_count == SEARCH_RESULT_LIMIT:
            count_text += f" (showing first {SEARCH_RESULT_LIMIT})"
        self.results_header.config(text=f"Search Results: {count_text}")
        
        # Create a grid container for results
        results_container = tk.Frame(self.results_frame.scrollable_frame, bg=BG_COLOR)
        results_container.pack(fill=tk.BOTH, expand=True)
        
        # Calculate number of columns based on window width
        # For now, use a fixed number
        num_columns = 4
        
        # Create movie cards in a grid layout
        for i, movie in enumerate(results):
            row = i // num_columns
            col = i % num_columns
            
            card = MovieCard(
                results_container,
                movie=movie,
                on_click=self.on_movie_click,
                width=180,
                height=280,
                bg=BG_COLOR
            )
            card.grid(row=row, column=col, padx=10, pady=10)
        
        # Set status
        self.set_status(f"Found {result_count} movies")
    
    def _handle_search(self, query, filters):
        """Handle search requests"""
        self.search_query = query
        self.search_filters = filters
        self._perform_search()
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Recreate UI to reflect any changes
        self._create_ui()
