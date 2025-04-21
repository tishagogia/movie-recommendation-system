"""
Base Screen module providing common functionality for all screens
"""
import tkinter as tk
from config import BG_COLOR, PRIMARY_COLOR, SECONDARY_COLOR
from ui_components import StatusBar, UserPanel

class BaseScreen(tk.Frame):
    """Base class for all screens in the application"""
    
    def __init__(self, parent, data_handler, user_manager=None, **kwargs):
        """Initialize a base screen"""
        super().__init__(parent, bg=BG_COLOR)
        
        self.data_handler = data_handler
        self.user_manager = user_manager
        
        # Extract callback functions from kwargs
        self.on_login = kwargs.get('on_login')
        self.on_register = kwargs.get('on_register')
        self.on_logout = kwargs.get('on_logout')
        self.on_profile = kwargs.get('on_profile')
        self.on_watchlist = kwargs.get('on_watchlist')
        self.on_bookmarks = kwargs.get('on_bookmarks')
        self.on_home = kwargs.get('on_home')
        self.on_back = kwargs.get('on_back')
        
        # Create the basic layout
        self._create_layout()
    
    def _create_layout(self):
        """Create the base layout for the screen"""
        # Header frame
        self.header_frame = tk.Frame(self, bg=PRIMARY_COLOR)
        self.header_frame.pack(fill=tk.X)
        
        # Title frame in the header
        self.title_frame = tk.Frame(self.header_frame, bg=PRIMARY_COLOR)
        self.title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # If we have an on_home callback, add a home button
        if self.on_home:
            home_btn = tk.Button(
                self.title_frame, 
                text="Home", 
                bg=PRIMARY_COLOR,
                fg="white",
                font=("Helvetica", 12, "bold"),
                bd=0,
                padx=10,
                pady=5,
                command=self.on_home
            )
            home_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # If we have an on_back callback, add a back button
        if self.on_back:
            back_btn = tk.Button(
                self.title_frame, 
                text="← Back", 
                bg=PRIMARY_COLOR,
                fg="white",
                font=("Helvetica", 12),
                bd=0,
                padx=10,
                pady=5,
                command=self.on_back
            )
            back_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Screen title (to be overridden by subclasses)
        self.title_label = tk.Label(
            self.title_frame,
            text="",
            bg=PRIMARY_COLOR,
            fg="white",
            font=("Helvetica", 16, "bold"),
            padx=10,
            pady=5
        )
        self.title_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # User panel if user_manager is provided
        if self.user_manager:
            self.user_panel = UserPanel(
                self.header_frame,
                on_login=self.on_login,
                on_register=self.on_register,
                on_logout=self.on_logout,
                on_profile=self.on_profile,
                on_watchlist=self.on_watchlist,
                on_bookmarks=self.on_bookmarks
            )
            self.user_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Main content frame
        self.content_frame = tk.Frame(self, bg=BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def set_title(self, title):
        """Set the screen title"""
        self.title_label.config(text=title)
    
    def set_status(self, message):
        """Set the status bar message"""
        self.status_bar.set_status(message)
    
    def update_screen(self):
        """Update the screen content - to be overridden by subclasses"""
        # Update user panel if available
        if hasattr(self, 'user_panel') and self.user_manager:
            self.user_panel.update_user(self.user_manager.get_current_user())
