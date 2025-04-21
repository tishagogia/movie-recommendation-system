"""
Reusable UI components for the Movie Recommendation System
"""
import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk, ImageDraw
import io
import base64
import re
import math
from config import (
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, BG_COLOR,
    TEXT_COLOR, TEXT_COLOR_LIGHT, TEXT_COLOR_INVERSE,
    FONT_FAMILY, FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE, 
    FONT_SIZE_EXTRA_LARGE, FONT_SIZE_TITLE,
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE,
    BUTTON_PADDING, ENTRY_PADDING
)
from utils import truncate_text, create_circular_frame

class ScrollableFrame(tk.Frame):
    """A scrollable frame widget"""
    
    def __init__(self, container, *args, **kwargs):
        # Extract bg color before passing to ttk.Frame
        bg_color = kwargs.pop('bg', BG_COLOR) if 'bg' in kwargs else BG_COLOR
        
        # Initialize with tk.Frame instead of ttk.Frame
        super().__init__(container, bg=bg_color, *args, **kwargs)
        
        # Create a canvas
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create frame inside canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Add frame to canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas to work with scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure frame to expand with canvas
        self.scrollable_frame.bind("<Configure>", self._configure_scrollable_frame)
        self.canvas.bind("<Configure>", self._configure_canvas)
        
        # Bind mouse wheel event
        self.bind_mousewheel()
    
    def _configure_scrollable_frame(self, event):
        """Update the scrollbar when the frame size changes"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _configure_canvas(self, event):
        """Update the scrollable frame width when canvas size changes"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def bind_mousewheel(self):
        """Bind mouse wheel events to scroll the frame"""
        def _on_mousewheel(event):
            # Different platforms use different event deltas
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")
        
        # Bind events for different platforms
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", _on_mousewheel)  # Linux
        self.canvas.bind_all("<Button-5>", _on_mousewheel)  # Linux
    
    def unbind_mousewheel(self):
        """Unbind mouse wheel events"""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

class HoverButton(tk.Button):
    """A button that changes appearance when hovered"""
    
    def __init__(self, master=None, hover_bg=None, hover_fg=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get('bg', self['bg'])
        self.default_fg = kwargs.get('fg', self['fg'])
        self.hover_bg = hover_bg if hover_bg else SECONDARY_COLOR
        self.hover_fg = hover_fg if hover_fg else TEXT_COLOR_INVERSE
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Change colors when mouse enters"""
        self['bg'] = self.hover_bg
        self['fg'] = self.hover_fg
    
    def _on_leave(self, event):
        """Restore colors when mouse leaves"""
        self['bg'] = self.default_bg
        self['fg'] = self.default_fg

class LabelButton(tk.Label):
    """A label that acts like a button with hover effects"""
    
    def __init__(self, master=None, hover_bg=None, hover_fg=None, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get('bg', self['bg'])
        self.default_fg = kwargs.get('fg', self['fg'])
        self.hover_bg = hover_bg if hover_bg else SECONDARY_COLOR
        self.hover_fg = hover_fg if hover_fg else TEXT_COLOR_INVERSE
        self.command = command
        
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    
    def _on_enter(self, event):
        """Change colors when mouse enters"""
        self['bg'] = self.hover_bg
        self['fg'] = self.hover_fg
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        """Restore colors when mouse leaves"""
        self['bg'] = self.default_bg
        self['fg'] = self.default_fg
        self.config(cursor="")
    
    def _on_click(self, event):
        """Execute command when clicked"""
        if self.command:
            self.command()

class MovieCard(tk.Frame):
    """A card widget displaying movie information"""
    
    def __init__(self, master, movie, on_click=None, width=200, height=300, **kwargs):
        bg_color = kwargs.pop('bg', BG_COLOR)
        super().__init__(master, bg=bg_color, width=width, height=height, **kwargs)
        
        self.movie = movie
        self.on_click = on_click
        self.width = width
        self.height = height
        
        # Ensure the frame maintains its size
        self.pack_propagate(False)
        
        # Create card content
        self._create_content()
        
        # Bind click event to the whole card
        self.bind("<Button-1>", self._handle_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _create_content(self):
        """Create the card content"""
        # Card container with rounded corners effect
        self.card_container = tk.Frame(self, bg=PRIMARY_COLOR, bd=1, relief=tk.SOLID)
        self.card_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inner card with padding
        self.card = tk.Frame(self.card_container, bg=BG_COLOR, padx=5, pady=5)
        self.card.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.card.bind("<Button-1>", self._handle_click)
        
        # Title with truncation
        title = self.movie.get('title', 'Unknown Title')
        title_label = tk.Label(
            self.card, 
            text=truncate_text(title, 20),
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            wraplength=self.width - 20,
            anchor='w',
            justify='left'
        )
        title_label.pack(fill=tk.X, padx=5, pady=5)
        title_label.bind("<Button-1>", self._handle_click)
        
        # Create a gradient effect for the poster background
        poster_frame = tk.Frame(self.card, bg=PRIMARY_COLOR, width=self.width-20, height=160)
        poster_frame.pack_propagate(False)
        poster_frame.pack(fill=tk.X, padx=5, pady=5)
        poster_frame.bind("<Button-1>", self._handle_click)
        
        # Movie icon with improved styling
        icon_type = "🎬"
        # Different icons based on genre if available
        genres = self.movie.get('genres', [])
        if genres:
            if isinstance(genres, str):
                genres = [g.strip() for g in genres.split(',')]
            
            # Map genres to emojis for visual variety
            genre_icons = {
                'Action': '💥', 'Adventure': '🌄', 'Animation': '🧸',
                'Comedy': '😄', 'Crime': '🕵️', 'Documentary': '📹',
                'Drama': '🎭', 'Family': '👨‍👩‍👧‍👦', 'Fantasy': '🧙',
                'History': '📜', 'Horror': '👻', 'Music': '🎵',
                'Mystery': '🔍', 'Romance': '❤️', 'Science Fiction': '🚀',
                'TV Movie': '📺', 'Thriller': '😱', 'War': '⚔️',
                'Western': '🤠'
            }
            
            for genre in genres:
                if genre in genre_icons:
                    icon_type = genre_icons[genre]
                    break
                    
        # Custom background for poster based on movie rating
        rating = float(self.movie.get('vote_average', 0))
        bg_color = PRIMARY_COLOR
        if rating >= 8:
            bg_color = "#1a936f"  # High rating - green
        elif rating >= 6:
            bg_color = "#88a4bf"  # Medium rating - blue
        elif rating >= 4:
            bg_color = "#c3943a"  # Low rating - yellow/orange
        else:
            bg_color = "#9c6b6c"  # Poor rating - reddish
        
        poster_label = tk.Label(
            poster_frame, 
            text=icon_type,
            font=(FONT_FAMILY, 48, "bold"),
            bg=bg_color,
            fg="#ffffff"
        )
        poster_label.pack(fill=tk.BOTH, expand=True)
        poster_label.bind("<Button-1>", self._handle_click)
        
        # Add popularity indicator with eye-catching design
        popularity = self.movie.get('popularity', 0)
        if popularity and float(popularity) > 20:
            popularity_frame = tk.Frame(poster_frame, bg="#d6193f", bd=0)
            popularity_frame.place(relx=1.0, x=-10, y=10, anchor="ne")
            
            trending_label = tk.Label(
                popularity_frame,
                text="🔥 HOT",
                font=(FONT_FAMILY, 8, "bold"),
                bg="#d6193f",
                fg="#ffffff",
                padx=5,
                pady=2
            )
            trending_label.pack()
        
        # Info area with improved layout
        info_frame = tk.Frame(self.card, bg=BG_COLOR)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        info_frame.bind("<Button-1>", self._handle_click)
        
        # Grid layout for info
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        
        # Row 1: Year and Vote Count
        row = 0
        year = self.movie.get('release_year', '')
        if not year and 'release_date' in self.movie:
            year_match = re.search(r'(\d{4})', str(self.movie['release_date']))
            if year_match:
                year = year_match.group(1)
        
        if year:
            year_label = tk.Label(
                info_frame, 
                text=f"📅 {year}",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                anchor='w'
            )
            year_label.grid(row=row, column=0, sticky='w', pady=2)
            year_label.bind("<Button-1>", self._handle_click)
        
        # Vote count on the right if available
        vote_count = self.movie.get('vote_count', 0)
        if vote_count:
            vote_label = tk.Label(
                info_frame,
                text=f"👥 {vote_count}",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                anchor='e'
            )
            vote_label.grid(row=row, column=1, sticky='e', pady=2)
            vote_label.bind("<Button-1>", self._handle_click)
            row += 1
        
        # Row 2: Rating
        rating = self.movie.get('vote_average', 0)
        if rating:
            rating_frame = tk.Frame(info_frame, bg=BG_COLOR)
            rating_frame.grid(row=row, column=0, columnspan=2, sticky='w', pady=2)
            rating_frame.bind("<Button-1>", self._handle_click)
            
            # Star rating with improved styling
            rating_value = min(10, max(0, float(rating)))
            # Create a visual score indicator
            rating_txt = f"⭐ {rating_value:.1f}/10"
            
            rating_label = tk.Label(
                rating_frame, 
                text=rating_txt,
                font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
                bg=BG_COLOR,
                fg=ACCENT_COLOR,
                anchor='w'
            )
            rating_label.pack(side=tk.LEFT)
            rating_label.bind("<Button-1>", self._handle_click)
            row += 1
        
        # Row 3: Genres with improved visual
        genres = self.movie.get('genres', '')
        if genres:
            if isinstance(genres, list):
                genres_text = ", ".join(genres[:2])  # Show at most 2 genres
            else:
                genres_text = str(genres).split(",")[:2]
                genres_text = ", ".join([g.strip() for g in genres_text])
            
            genres_label = tk.Label(
                info_frame, 
                text=truncate_text(f"🎭 {genres_text}", 25),
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                anchor='w'
            )
            genres_label.grid(row=row, column=0, columnspan=2, sticky='w', pady=2)
            genres_label.bind("<Button-1>", self._handle_click)
            row += 1
        
        # Row 4: View Details button
        button_frame = tk.Frame(self.card, bg=BG_COLOR)
        button_frame.pack(fill=tk.X, pady=5)
        
        details_button = HoverButton(
            button_frame,
            text="View Details",
            font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR_INVERSE,
            hover_bg=PRIMARY_COLOR,
            activebackground=PRIMARY_COLOR,
            activeforeground=TEXT_COLOR_INVERSE,
            bd=0,
            borderwidth=0,
            relief="flat",
            padx=10,
            pady=5,
            command=self._on_button_click
        )
        details_button.pack(side=tk.TOP, pady=3)
    
    def _handle_click(self, event):
        """Handle click on the card"""
        if self.on_click:
            self.on_click(self.movie)
    
    def _on_button_click(self):
        """Handle click on the view details button"""
        if self.on_click:
            self.on_click(self.movie)
            
    def _on_enter(self, event):
        """Handle mouse enter event"""
        # Create a hover effect by changing the border color
        self.card_container.config(bg=ACCENT_COLOR)
        self.config(cursor="hand2")
    
    def _on_leave(self, event):
        """Handle mouse leave event"""
        # Restore original appearance
        self.card_container.config(bg=PRIMARY_COLOR)
        self.config(cursor="")

class RatingWidget(tk.Frame):
    """A widget for displaying and selecting ratings"""
    
    def __init__(self, master, rating=0, max_rating=5, size=FONT_SIZE_MEDIUM, 
                 interactive=False, command=None, **kwargs):
        bg_color = kwargs.pop('bg', BG_COLOR)
        super().__init__(master, bg=bg_color, **kwargs)
        
        self.rating = rating
        self.max_rating = max_rating
        self.size = size
        self.interactive = interactive
        self.command = command
        
        self._create_stars()
    
    def _create_stars(self):
        """Create the star rating display"""
        self.star_labels = []
        
        for i in range(self.max_rating):
            star_label = tk.Label(
                self,
                text="★",
                font=(FONT_FAMILY, self.size),
                bg=self['bg']
            )
            
            # Set initial color
            if i < math.floor(self.rating):
                star_label.config(fg=ACCENT_COLOR)
            else:
                star_label.config(fg=TEXT_COLOR_LIGHT)
            
            star_label.pack(side=tk.LEFT, padx=1)
            self.star_labels.append(star_label)
            
            # Add interactivity if enabled
            if self.interactive:
                star_label.bind("<Enter>", lambda e, idx=i: self._on_star_hover(idx))
                star_label.bind("<Leave>", self._on_star_leave)
                star_label.bind("<Button-1>", lambda e, idx=i: self._on_star_click(idx))
                star_label.config(cursor="hand2")
    
    def set_rating(self, rating):
        """Update the displayed rating"""
        self.rating = min(self.max_rating, max(0, rating))
        self._update_stars()
    
    def _update_stars(self):
        """Update the star display based on current rating"""
        full_stars = math.floor(self.rating)
        
        for i, star_label in enumerate(self.star_labels):
            if i < full_stars:
                star_label.config(fg=ACCENT_COLOR)
            else:
                star_label.config(fg=TEXT_COLOR_LIGHT)
    
    def _on_star_hover(self, index):
        """Handle mouse hover over a star"""
        if not self.interactive:
            return
            
        for i, star_label in enumerate(self.star_labels):
            if i <= index:
                star_label.config(fg=ACCENT_COLOR)
            else:
                star_label.config(fg=TEXT_COLOR_LIGHT)
    
    def _on_star_leave(self, event):
        """Handle mouse leaving the stars"""
        if not self.interactive:
            return
            
        self._update_stars()
    
    def _on_star_click(self, index):
        """Handle clicking on a star"""
        if not self.interactive:
            return
            
        self.rating = index + 1
        self._update_stars()
        
        if self.command:
            self.command(self.rating)

class SearchBar(tk.Frame):
    """A search bar widget with filters"""
    
    def __init__(self, master, on_search=None, genres=None, **kwargs):
        bg_color = kwargs.pop('bg', BG_COLOR)
        super().__init__(master, bg=bg_color, **kwargs)
        
        self.on_search = on_search
        self.genres = genres if genres else []
        self.filters_visible = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the search bar widgets"""
        # Main search frame
        search_frame = tk.Frame(self, bg=self['bg'])
        search_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bd=1,
            relief=tk.SOLID,
            highlightthickness=1,
            highlightcolor=SECONDARY_COLOR
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, PADDING_SMALL))
        self.search_entry.bind("<Return>", self._on_search)
        
        # Search button
        search_button = HoverButton(
            search_frame,
            text="Search",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR_INVERSE,
            hover_bg=PRIMARY_COLOR,
            activebackground=PRIMARY_COLOR,
            activeforeground=TEXT_COLOR_INVERSE,
            bd=0,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_search_button
        )
        search_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Filters toggle button
        self.filter_button = HoverButton(
            search_frame,
            text="Filters ▼",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=PRIMARY_COLOR,
            fg=TEXT_COLOR_INVERSE,
            hover_bg=SECONDARY_COLOR,
            activebackground=SECONDARY_COLOR,
            activeforeground=TEXT_COLOR_INVERSE,
            bd=0,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._toggle_filters
        )
        self.filter_button.pack(side=tk.LEFT)
        
        # Filters frame (hidden initially)
        self.filters_frame = tk.Frame(self, bg=self['bg'], bd=1, relief=tk.SOLID)
        
        # Create filter controls
        self._create_filters()
    
    def _create_filters(self):
        """Create filter controls"""
        # Main container
        container = tk.Frame(self.filters_frame, bg=self['bg'], padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        container.pack(fill=tk.X)
        
        # Create two columns for filters
        left_frame = tk.Frame(container, bg=self['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, PADDING_MEDIUM))
        
        right_frame = tk.Frame(container, bg=self['bg'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(PADDING_MEDIUM, 0))
        
        # Genre filter
        genre_frame = tk.Frame(left_frame, bg=self['bg'])
        genre_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        tk.Label(
            genre_frame, 
            text="Genre:",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR
        ).pack(side=tk.LEFT)
        
        self.genre_var = tk.StringVar()
        genre_menu = ttk.Combobox(
            genre_frame,
            textvariable=self.genre_var,
            values=["All"] + self.genres,
            state="readonly",
            width=15
        )
        genre_menu.pack(side=tk.LEFT, padx=PADDING_SMALL)
        genre_menu.current(0)
        
        # Release year filters
        year_frame = tk.Frame(left_frame, bg=self['bg'])
        year_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        tk.Label(
            year_frame, 
            text="Year:",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR
        ).pack(side=tk.LEFT)
        
        self.year_from_var = tk.StringVar()
        tk.Entry(
            year_frame,
            textvariable=self.year_from_var,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            width=5,
            bd=1,
            relief=tk.SOLID
        ).pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        tk.Label(
            year_frame, 
            text="to",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR
        ).pack(side=tk.LEFT)
        
        self.year_to_var = tk.StringVar()
        tk.Entry(
            year_frame,
            textvariable=self.year_to_var,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            width=5,
            bd=1,
            relief=tk.SOLID
        ).pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Rating filter
        rating_frame = tk.Frame(right_frame, bg=self['bg'])
        rating_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        tk.Label(
            rating_frame, 
            text="Min Rating:",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR
        ).pack(side=tk.LEFT)
        
        self.rating_var = tk.StringVar()
        rating_values = ["Any", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        rating_menu = ttk.Combobox(
            rating_frame,
            textvariable=self.rating_var,
            values=rating_values,
            state="readonly",
            width=5
        )
        rating_menu.pack(side=tk.LEFT, padx=PADDING_SMALL)
        rating_menu.current(0)
        
        # Director/Cast filter
        person_frame = tk.Frame(right_frame, bg=self['bg'])
        person_frame.pack(fill=tk.X, pady=PADDING_SMALL)
        
        self.person_type_var = tk.StringVar(value="Director")
        person_type_menu = ttk.Combobox(
            person_frame,
            textvariable=self.person_type_var,
            values=["Director", "Cast"],
            state="readonly",
            width=8
        )
        person_type_menu.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        self.person_var = tk.StringVar()
        tk.Entry(
            person_frame,
            textvariable=self.person_var,
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bd=1,
            relief=tk.SOLID,
            width=15
        ).pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Button frame
        button_frame = tk.Frame(container, bg=self['bg'])
        button_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Apply filters button
        apply_button = HoverButton(
            button_frame,
            text="Apply Filters",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR_INVERSE,
            hover_bg=PRIMARY_COLOR,
            activebackground=PRIMARY_COLOR,
            activeforeground=TEXT_COLOR_INVERSE,
            bd=0,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_search_button
        )
        apply_button.pack(side=tk.RIGHT, padx=PADDING_SMALL)
        
        # Reset filters button
        reset_button = HoverButton(
            button_frame,
            text="Reset Filters",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=TEXT_COLOR_LIGHT,
            fg=TEXT_COLOR_INVERSE,
            hover_bg=TEXT_COLOR,
            activebackground=TEXT_COLOR,
            activeforeground=TEXT_COLOR_INVERSE,
            bd=0,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._reset_filters
        )
        reset_button.pack(side=tk.RIGHT, padx=PADDING_SMALL)
    
    def _toggle_filters(self):
        """Toggle filters visibility"""
        if self.filters_visible:
            self.filters_frame.pack_forget()
            self.filter_button.config(text="Filters ▼")
        else:
            self.filters_frame.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=(0, PADDING_MEDIUM))
            self.filter_button.config(text="Filters ▲")
        
        self.filters_visible = not self.filters_visible
    
    def _reset_filters(self):
        """Reset all filters to default values"""
        self.genre_var.set("All")
        self.year_from_var.set("")
        self.year_to_var.set("")
        self.rating_var.set("Any")
        self.person_var.set("")
        self.person_type_var.set("Director")
    
    def _get_filters(self):
        """Get current filter values as a dictionary"""
        filters = {}
        
        # Genre filter
        genre = self.genre_var.get()
        if genre and genre != "All":
            filters['genres'] = genre
        
        # Year range
        year_from = self.year_from_var.get().strip()
        if year_from:
            try:
                filters['year_from'] = int(year_from)
            except ValueError:
                pass
        
        year_to = self.year_to_var.get().strip()
        if year_to:
            try:
                filters['year_to'] = int(year_to)
            except ValueError:
                pass
        
        # Rating filter
        rating = self.rating_var.get()
        if rating and rating != "Any":
            try:
                filters['min_rating'] = float(rating)
            except ValueError:
                pass
        
        # Director/Cast filter
        person = self.person_var.get().strip()
        if person:
            person_type = self.person_type_var.get()
            if person_type == "Director":
                filters['director'] = person
            elif person_type == "Cast":
                filters['cast'] = person
        
        return filters
    
    def _on_search(self, event=None):
        """Handle search event from pressing Enter"""
        self._on_search_button()
    
    def _on_search_button(self):
        """Handle search button click"""
        query = self.search_var.get().strip()
        filters = self._get_filters()
        
        if self.on_search:
            self.on_search(query, filters)

class StatusBar(tk.Frame):
    """A status bar for displaying messages"""
    
    def __init__(self, master, **kwargs):
        bg_color = kwargs.pop('bg', BG_COLOR)
        super().__init__(master, bg=bg_color, **kwargs)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create status bar widgets"""
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            self,
            textvariable=self.status_var,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            bg=self['bg'],
            fg=TEXT_COLOR_LIGHT,
            anchor='w',
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL
        )
        self.status_label.pack(fill=tk.X)
        
        # Separator
        separator = tk.Frame(self, height=1, bg=TEXT_COLOR_LIGHT)
        separator.pack(fill=tk.X, side=tk.TOP)
    
    def set_status(self, message):
        """Set the status message"""
        self.status_var.set(message)

class UserPanel(tk.Frame):
    """User panel showing login status and actions"""
    
    def __init__(self, master, on_login=None, on_register=None, on_logout=None, 
                 on_profile=None, on_watchlist=None, on_bookmarks=None, **kwargs):
        bg_color = kwargs.pop('bg', PRIMARY_COLOR)
        super().__init__(master, bg=bg_color, **kwargs)
        
        self.on_login = on_login
        self.on_register = on_register
        self.on_logout = on_logout
        self.on_profile = on_profile
        self.on_watchlist = on_watchlist
        self.on_bookmarks = on_bookmarks
        
        self.user = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Create user panel widgets"""
        # Container frame
        container = tk.Frame(self, bg=self['bg'], padx=PADDING_MEDIUM, pady=PADDING_SMALL)
        container.pack(fill=tk.X)
        
        # Left side - user info
        self.user_frame = tk.Frame(container, bg=self['bg'])
        self.user_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Right side - actions
        actions_frame = tk.Frame(container, bg=self['bg'])
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons for guest users
        self.login_button = LabelButton(
            actions_frame,
            text="Login",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR_INVERSE,
            hover_bg=SECONDARY_COLOR,
            hover_fg=TEXT_COLOR_INVERSE,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_login_click
        )
        
        self.register_button = LabelButton(
            actions_frame,
            text="Register",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR_INVERSE,
            hover_bg=SECONDARY_COLOR,
            hover_fg=TEXT_COLOR_INVERSE,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_register_click
        )
        
        # Action buttons for logged-in users
        self.watchlist_button = LabelButton(
            actions_frame,
            text="Watchlist",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR_INVERSE,
            hover_bg=SECONDARY_COLOR,
            hover_fg=TEXT_COLOR_INVERSE,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_watchlist_click
        )
        
        self.bookmarks_button = LabelButton(
            actions_frame,
            text="Bookmarks",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR_INVERSE,
            hover_bg=SECONDARY_COLOR,
            hover_fg=TEXT_COLOR_INVERSE,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_bookmarks_click
        )
        
        self.profile_button = LabelButton(
            actions_frame,
            text="Profile",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR_INVERSE,
            hover_bg=SECONDARY_COLOR,
            hover_fg=TEXT_COLOR_INVERSE,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_profile_click
        )
        
        self.logout_button = LabelButton(
            actions_frame,
            text="Logout",
            font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
            bg=self['bg'],
            fg=TEXT_COLOR_INVERSE,
            hover_bg=ACCENT_COLOR,
            hover_fg=TEXT_COLOR_INVERSE,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_logout_click
        )
        
        # Initialize the display based on user login status
        self.update_user(None)
    
    def update_user(self, user):
        """Update the displayed user"""
        self.user = user
        
        # Clear existing widgets
        for widget in self.user_frame.winfo_children():
            widget.destroy()
        
        if user:
            # Hide login/register, show user actions
            self.login_button.pack_forget()
            self.register_button.pack_forget()
            
            self.watchlist_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            self.bookmarks_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            self.profile_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            self.logout_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            
            # Show user info
            display_name = user.get("profile", {}).get("display_name", user.get("username", "User"))
            
            tk.Label(
                self.user_frame,
                text=f"Welcome, {display_name}",
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                bg=self['bg'],
                fg=TEXT_COLOR_INVERSE,
                padx=PADDING_SMALL
            ).pack(side=tk.LEFT)
            
        else:
            # Hide user actions, show login/register
            self.watchlist_button.pack_forget()
            self.bookmarks_button.pack_forget()
            self.profile_button.pack_forget()
            self.logout_button.pack_forget()
            
            self.login_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            self.register_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            
            # Show guest info
            tk.Label(
                self.user_frame,
                text="Guest User",
                font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                bg=self['bg'],
                fg=TEXT_COLOR_INVERSE,
                padx=PADDING_SMALL
            ).pack(side=tk.LEFT)
    
    def _on_login_click(self):
        """Handle login button click"""
        if self.on_login:
            self.on_login()
    
    def _on_register_click(self):
        """Handle register button click"""
        if self.on_register:
            self.on_register()
    
    def _on_logout_click(self):
        """Handle logout button click"""
        if self.on_logout:
            self.on_logout()
    
    def _on_profile_click(self):
        """Handle profile button click"""
        if self.on_profile:
            self.on_profile()
    
    def _on_watchlist_click(self):
        """Handle watchlist button click"""
        if self.on_watchlist:
            self.on_watchlist()
    
    def _on_bookmarks_click(self):
        """Handle bookmarks button click"""
        if self.on_bookmarks:
            self.on_bookmarks()
