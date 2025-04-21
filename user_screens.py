"""
User-related screens for the Movie Recommendation System
"""
import tkinter as tk
from tkinter import ttk
import re
from datetime import datetime

from config import (
    BG_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, 
    TEXT_COLOR, TEXT_COLOR_LIGHT, TEXT_COLOR_INVERSE, USERNAME_MIN_LENGTH, PASSWORD_MIN_LENGTH
)
from screens.base_screen import BaseScreen
from ui_components import (
    ScrollableFrame, MovieCard, HoverButton, LabelButton
)
from utils import show_error, show_confirmation, show_info, create_circular_frame, truncate_text
from assets.styles import (
    PADDING_SMALL, PADDING_MEDIUM, PADDING_LARGE,
    BUTTON_STYLE, ACCENT_BUTTON_STYLE, ENTRY_STYLE
)

class LoginScreen(BaseScreen):
    """Screen for user login"""
    
    def __init__(self, parent, user_manager, **kwargs):
        # Extract callbacks before passing to super()
        self.on_login_success = kwargs.pop('on_login_success', None)
        
        # Initialize the base screen without a data_handler
        super().__init__(parent, None, user_manager, **kwargs)
        
        # Set screen title
        self.set_title("Login")
        
        # Initialize the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the login screen UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create a centered login form
        form_frame = tk.Frame(
            self.content_frame,
            bg=BG_COLOR,
            padx=PADDING_LARGE,
            pady=PADDING_LARGE
        )
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Login header
        header_label = tk.Label(
            form_frame,
            text="Login to Your Account",
            font=("Helvetica", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            pady=PADDING_MEDIUM
        )
        header_label.pack(fill=tk.X)
        
        # Username field
        username_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        username_frame.pack(fill=tk.X)
        
        username_label = tk.Label(
            username_frame,
            text="Username:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor='w'
        )
        username_label.pack(side=tk.LEFT)
        
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            **ENTRY_STYLE,
            width=30
        )
        username_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        password_frame.pack(fill=tk.X)
        
        password_label = tk.Label(
            password_frame,
            text="Password:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor='w'
        )
        password_label.pack(side=tk.LEFT)
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            **ENTRY_STYLE,
            width=30
        )
        password_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Error message label
        self.error_var = tk.StringVar()
        self.error_label = tk.Label(
            form_frame,
            textvariable=self.error_var,
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
            wraplength=300
        )
        self.error_label.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_MEDIUM)
        buttons_frame.pack(fill=tk.X)
        
        # Login button
        login_button = HoverButton(
            buttons_frame,
            text="Login",
            **BUTTON_STYLE,
            command=self._handle_login
        )
        login_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Cancel button
        cancel_button = HoverButton(
            buttons_frame,
            text="Cancel",
            bg=TEXT_COLOR_LIGHT,
            fg="white",
            activebackground=TEXT_COLOR,
            activeforeground="white",
            font=("Helvetica", 12),
            padx=15,
            pady=5,
            bd=0,
            command=self.on_back
        )
        cancel_button.pack(side=tk.LEFT)
        
        # Set initial focus
        username_entry.focus_set()
        
        # Bind enter key to login
        username_entry.bind("<Return>", lambda e: self._handle_login())
        password_entry.bind("<Return>", lambda e: self._handle_login())
    
    def _handle_login(self):
        """Handle login button press"""
        # Clear previous error
        self.error_var.set("")
        
        # Get input values
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # Validate inputs
        if not username:
            self.error_var.set("Username is required")
            return
        
        if not password:
            self.error_var.set("Password is required")
            return
        
        # Attempt login
        success, message = self.user_manager.login(username, password)
        
        if success:
            # Call success callback
            if self.on_login_success:
                self.on_login_success()
            # Clear fields
            self.username_var.set("")
            self.password_var.set("")
        else:
            # Show error message
            self.error_var.set(message)
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Clear fields
        if hasattr(self, 'username_var'):
            self.username_var.set("")
        if hasattr(self, 'password_var'):
            self.password_var.set("")
        if hasattr(self, 'error_var'):
            self.error_var.set("")

class RegisterScreen(BaseScreen):
    """Screen for user registration"""
    
    def __init__(self, parent, user_manager, **kwargs):
        # Extract callbacks before passing to super()
        self.on_register_success = kwargs.pop('on_register_success', None)
        
        # Initialize the base screen without a data_handler
        super().__init__(parent, None, user_manager, **kwargs)
        
        # Set screen title
        self.set_title("Register")
        
        # Initialize the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the registration screen UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create a centered registration form
        form_frame = tk.Frame(
            self.content_frame,
            bg=BG_COLOR,
            padx=PADDING_LARGE,
            pady=PADDING_LARGE
        )
        form_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Registration header
        header_label = tk.Label(
            form_frame,
            text="Create a New Account",
            font=("Helvetica", 18, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            pady=PADDING_MEDIUM
        )
        header_label.pack(fill=tk.X)
        
        # Username field
        username_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        username_frame.pack(fill=tk.X)
        
        username_label = tk.Label(
            username_frame,
            text="Username:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor='w'
        )
        username_label.pack(side=tk.LEFT)
        
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            **ENTRY_STYLE,
            width=30
        )
        username_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Email field
        email_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        email_frame.pack(fill=tk.X)
        
        email_label = tk.Label(
            email_frame,
            text="Email:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor='w'
        )
        email_label.pack(side=tk.LEFT)
        
        self.email_var = tk.StringVar()
        email_entry = tk.Entry(
            email_frame,
            textvariable=self.email_var,
            **ENTRY_STYLE,
            width=30
        )
        email_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Password field
        password_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        password_frame.pack(fill=tk.X)
        
        password_label = tk.Label(
            password_frame,
            text="Password:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor='w'
        )
        password_label.pack(side=tk.LEFT)
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="*",
            **ENTRY_STYLE,
            width=30
        )
        password_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Confirm password field
        confirm_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        confirm_frame.pack(fill=tk.X)
        
        confirm_label = tk.Label(
            confirm_frame,
            text="Confirm:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=10,
            anchor='w'
        )
        confirm_label.pack(side=tk.LEFT)
        
        self.confirm_var = tk.StringVar()
        confirm_entry = tk.Entry(
            confirm_frame,
            textvariable=self.confirm_var,
            show="*",
            **ENTRY_STYLE,
            width=30
        )
        confirm_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Requirements info
        requirements_text = f"Username must be at least {USERNAME_MIN_LENGTH} characters\n" \
                           f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
        requirements_label = tk.Label(
            form_frame,
            text=requirements_text,
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT,
            anchor='w',
            justify=tk.LEFT
        )
        requirements_label.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Error message label
        self.error_var = tk.StringVar()
        self.error_label = tk.Label(
            form_frame,
            textvariable=self.error_var,
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=ACCENT_COLOR,
            wraplength=300
        )
        self.error_label.pack(fill=tk.X, pady=PADDING_SMALL)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_MEDIUM)
        buttons_frame.pack(fill=tk.X)
        
        # Register button
        register_button = HoverButton(
            buttons_frame,
            text="Register",
            **BUTTON_STYLE,
            command=self._handle_register
        )
        register_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Cancel button
        cancel_button = HoverButton(
            buttons_frame,
            text="Cancel",
            bg=TEXT_COLOR_LIGHT,
            fg="white",
            activebackground=TEXT_COLOR,
            activeforeground="white",
            font=("Helvetica", 12),
            padx=15,
            pady=5,
            bd=0,
            command=self.on_back
        )
        cancel_button.pack(side=tk.LEFT)
        
        # Set initial focus
        username_entry.focus_set()
        
        # Bind enter key to register
        username_entry.bind("<Return>", lambda e: self._handle_register())
        email_entry.bind("<Return>", lambda e: self._handle_register())
        password_entry.bind("<Return>", lambda e: self._handle_register())
        confirm_entry.bind("<Return>", lambda e: self._handle_register())
    
    def _handle_register(self):
        """Handle register button press"""
        # Clear previous error
        self.error_var.set("")
        
        # Get input values
        username = self.username_var.get().strip()
        email = self.email_var.get().strip()
        password = self.password_var.get()
        confirm = self.confirm_var.get()
        
        # Validate inputs
        if not username:
            self.error_var.set("Username is required")
            return
        
        if len(username) < USERNAME_MIN_LENGTH:
            self.error_var.set(f"Username must be at least {USERNAME_MIN_LENGTH} characters")
            return
        
        if not password:
            self.error_var.set("Password is required")
            return
        
        if len(password) < PASSWORD_MIN_LENGTH:
            self.error_var.set(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")
            return
        
        if password != confirm:
            self.error_var.set("Passwords do not match")
            return
        
        # Attempt registration
        success, message = self.user_manager.register(username, password, email)
        
        if success:
            # Call success callback
            if self.on_register_success:
                self.on_register_success()
            # Clear fields
            self.username_var.set("")
            self.email_var.set("")
            self.password_var.set("")
            self.confirm_var.set("")
        else:
            # Show error message
            self.error_var.set(message)
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Clear fields
        if hasattr(self, 'username_var'):
            self.username_var.set("")
        if hasattr(self, 'email_var'):
            self.email_var.set("")
        if hasattr(self, 'password_var'):
            self.password_var.set("")
        if hasattr(self, 'confirm_var'):
            self.confirm_var.set("")
        if hasattr(self, 'error_var'):
            self.error_var.set("")

class ProfileScreen(BaseScreen):
    """Screen for user profile management"""
    
    def __init__(self, parent, user_manager, data_handler, **kwargs):
        # Extract callbacks before passing to super()
        self.on_save = kwargs.pop('on_save', None)
        
        # Initialize the base screen
        super().__init__(parent, data_handler, user_manager, **kwargs)
        
        # Set screen title
        self.set_title("Profile")
        
        # Initialize the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the profile screen UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get current user
        user = self.user_manager.get_current_user()
        if not user:
            # Show a message if not logged in
            not_logged_label = tk.Label(
                self.content_frame,
                text="You must be logged in to view your profile",
                font=("Helvetica", 14),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=50
            )
            not_logged_label.pack(expand=True)
            return
        
        # Create a scrollable frame for the profile content
        self.scroll_frame = ScrollableFrame(self.content_frame, bg=BG_COLOR)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main profile container
        profile_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR,
            padx=PADDING_LARGE,
            pady=PADDING_LARGE
        )
        profile_container.pack(fill=tk.BOTH, expand=True)
        
        # Profile header
        header_frame = tk.Frame(profile_container, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Profile picture placeholder
        avatar_size = 100
        avatar_frame, avatar_canvas = create_circular_frame(
            header_frame, 
            avatar_size, 
            PRIMARY_COLOR, 
            border_color=SECONDARY_COLOR, 
            border_width=2
        )
        avatar_frame.pack(side=tk.LEFT, padx=PADDING_MEDIUM)
        
        # Add a placeholder avatar text
        avatar_text = tk.Label(
            avatar_canvas,
            text=user.get('username', 'U')[0].upper(),
            font=("Helvetica", 36, "bold"),
            bg=PRIMARY_COLOR,
            fg="white"
        )
        avatar_text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # User info
        info_frame = tk.Frame(header_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        info_frame.pack(side=tk.LEFT, fill=tk.Y, padx=PADDING_MEDIUM)
        
        # Username
        username_label = tk.Label(
            info_frame,
            text=f"Username: {user.get('username', 'Unknown')}",
            font=("Helvetica", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w',
            justify=tk.LEFT
        )
        username_label.pack(anchor='w', pady=(0, PADDING_SMALL))
        
        # Email
        email_label = tk.Label(
            info_frame,
            text=f"Email: {user.get('email', 'Not provided')}",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w',
            justify=tk.LEFT
        )
        email_label.pack(anchor='w', pady=(0, PADDING_SMALL))
        
        # Member since
        created_at = user.get('created_at', '')
        if created_at:
            # Format date if it's available
            try:
                # Just take the date part
                date_part = created_at.split('T')[0]
                member_since = f"Member since: {date_part}"
            except:
                member_since = f"Member since: {created_at}"
        else:
            member_since = "Member since: Unknown"
            
        member_label = tk.Label(
            info_frame,
            text=member_since,
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT,
            anchor='w',
            justify=tk.LEFT
        )
        member_label.pack(anchor='w')
        
        # Separator
        separator = ttk.Separator(profile_container, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Edit profile section
        edit_label = tk.Label(
            profile_container,
            text="Edit Profile",
            font=("Helvetica", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        edit_label.pack(fill=tk.X, anchor='w', pady=PADDING_MEDIUM)
        
        # Profile form
        form_frame = tk.Frame(profile_container, bg=BG_COLOR)
        form_frame.pack(fill=tk.X, padx=PADDING_MEDIUM)
        
        # Display name field
        name_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        name_frame.pack(fill=tk.X)
        
        name_label = tk.Label(
            name_frame,
            text="Display Name:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=15,
            anchor='w'
        )
        name_label.pack(side=tk.LEFT)
        
        profile = user.get('profile', {})
        self.display_name_var = tk.StringVar(value=profile.get('display_name', user.get('username', '')))
        name_entry = tk.Entry(
            name_frame,
            textvariable=self.display_name_var,
            **ENTRY_STYLE,
            width=30
        )
        name_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Bio field
        bio_frame = tk.Frame(form_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        bio_frame.pack(fill=tk.X)
        
        bio_label = tk.Label(
            bio_frame,
            text="Bio:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=15,
            anchor='w'
        )
        bio_label.pack(side=tk.LEFT, anchor='n')
        
        self.bio_text = tk.Text(
            bio_frame,
            font=("Helvetica", 12),
            bd=1,
            relief=tk.SOLID,
            highlightthickness=1,
            highlightcolor=SECONDARY_COLOR,
            width=30,
            height=4
        )
        self.bio_text.pack(side=tk.LEFT, padx=PADDING_SMALL)
        self.bio_text.insert('1.0', profile.get('bio', ''))
        
        # Preferences section
        preferences_label = tk.Label(
            profile_container,
            text="Preferences",
            font=("Helvetica", 16, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        preferences_label.pack(fill=tk.X, anchor='w', pady=PADDING_MEDIUM)
        
        # Preferences form
        pref_frame = tk.Frame(profile_container, bg=BG_COLOR)
        pref_frame.pack(fill=tk.X, padx=PADDING_MEDIUM)
        
        # Get user preferences
        preferences = profile.get('preferences', {})
        
        # Favorite genres
        genres_frame = tk.Frame(pref_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        genres_frame.pack(fill=tk.X)
        
        genres_label = tk.Label(
            genres_frame,
            text="Favorite Genres:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=15,
            anchor='w'
        )
        genres_label.pack(side=tk.LEFT)
        
        fav_genres = preferences.get('favorite_genres', [])
        self.genres_var = tk.StringVar(value=', '.join(fav_genres))
        genres_entry = tk.Entry(
            genres_frame,
            textvariable=self.genres_var,
            **ENTRY_STYLE,
            width=30
        )
        genres_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Favorite directors
        directors_frame = tk.Frame(pref_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        directors_frame.pack(fill=tk.X)
        
        directors_label = tk.Label(
            directors_frame,
            text="Favorite Directors:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=15,
            anchor='w'
        )
        directors_label.pack(side=tk.LEFT)
        
        fav_directors = preferences.get('favorite_directors', [])
        self.directors_var = tk.StringVar(value=', '.join(fav_directors))
        directors_entry = tk.Entry(
            directors_frame,
            textvariable=self.directors_var,
            **ENTRY_STYLE,
            width=30
        )
        directors_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Favorite actors
        actors_frame = tk.Frame(pref_frame, bg=BG_COLOR, pady=PADDING_SMALL)
        actors_frame.pack(fill=tk.X)
        
        actors_label = tk.Label(
            actors_frame,
            text="Favorite Actors:",
            font=("Helvetica", 12),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            width=15,
            anchor='w'
        )
        actors_label.pack(side=tk.LEFT)
        
        fav_actors = preferences.get('favorite_actors', [])
        self.actors_var = tk.StringVar(value=', '.join(fav_actors))
        actors_entry = tk.Entry(
            actors_frame,
            textvariable=self.actors_var,
            **ENTRY_STYLE,
            width=30
        )
        actors_entry.pack(side=tk.LEFT, padx=PADDING_SMALL)
        
        # Format help
        format_label = tk.Label(
            pref_frame,
            text="Enter multiple values separated by commas",
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT,
            anchor='w'
        )
        format_label.pack(anchor='w', padx=(135, 0), pady=PADDING_SMALL)
        
        # Buttons frame
        buttons_frame = tk.Frame(profile_container, bg=BG_COLOR, pady=PADDING_MEDIUM)
        buttons_frame.pack(fill=tk.X, pady=PADDING_MEDIUM)
        
        # Save button
        save_button = HoverButton(
            buttons_frame,
            text="Save Changes",
            **BUTTON_STYLE,
            command=self._handle_save
        )
        save_button.pack(side=tk.LEFT, padx=(0, PADDING_SMALL))
        
        # Cancel button
        cancel_button = HoverButton(
            buttons_frame,
            text="Cancel",
            bg=TEXT_COLOR_LIGHT,
            fg="white",
            activebackground=TEXT_COLOR,
            activeforeground="white",
            font=("Helvetica", 12),
            padx=15,
            pady=5,
            bd=0,
            command=self.on_back
        )
        cancel_button.pack(side=tk.LEFT)
    
    def _handle_save(self):
        """Handle save button press"""
        # Get input values
        display_name = self.display_name_var.get().strip()
        bio = self.bio_text.get("1.0", tk.END).strip()
        
        # Parse comma-separated lists
        genres = [g.strip() for g in self.genres_var.get().split(',') if g.strip()]
        directors = [d.strip() for d in self.directors_var.get().split(',') if d.strip()]
        actors = [a.strip() for a in self.actors_var.get().split(',') if a.strip()]
        
        # Create profile data
        profile_data = {
            'display_name': display_name,
            'bio': bio,
            'preferences': {
                'favorite_genres': genres,
                'favorite_directors': directors,
                'favorite_actors': actors
            }
        }
        
        # Save profile
        if self.on_save:
            self.on_save(profile_data)
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Recreate UI to reflect any changes
        self._create_ui()

class WatchlistScreen(BaseScreen):
    """Screen for displaying and managing user's watchlist"""
    
    def __init__(self, parent, user_manager, data_handler, **kwargs):
        # Extract callbacks before passing to super()
        self.on_movie_click = kwargs.pop('on_movie_click', None)
        self.on_remove = kwargs.pop('on_remove', None)
        self.recommender = kwargs.pop('recommender', None)
        
        # Initialize the base screen
        super().__init__(parent, data_handler, user_manager, **kwargs)
        
        # Set screen title
        self.set_title("My Watchlist")
        
        # Initialize the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the watchlist screen UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get current user
        user = self.user_manager.get_current_user()
        if not user:
            # Show a more attractive message if not logged in
            login_frame = tk.Frame(self.content_frame, bg=BG_COLOR, padx=50, pady=50)
            login_frame.pack(expand=True)
            
            not_logged_label = tk.Label(
                login_frame,
                text="Please login to access your watchlist",
                font=("Helvetica", 18, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=20
            )
            not_logged_label.pack()
            
            message_label = tk.Label(
                login_frame,
                text="Your watchlist allows you to save movies you want to watch later\nand get personalized recommendations based on your preferences.",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                justify=tk.CENTER,
                pady=10
            )
            message_label.pack()
            
            login_button = HoverButton(
                login_frame,
                text="Login",
                font=("Helvetica", 14),
                bg=PRIMARY_COLOR,
                fg=TEXT_COLOR_INVERSE,
                hover_bg=SECONDARY_COLOR,
                activebackground=SECONDARY_COLOR,
                activeforeground=TEXT_COLOR_INVERSE,
                padx=30,
                pady=10,
                bd=0,
                command=lambda: self.on_back()
            )
            login_button.pack(pady=20)
            
            return
        
        # Create a main frame with two columns
        main_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column for watchlist (2/3 width)
        left_column = tk.Frame(main_frame, bg=BG_COLOR)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(PADDING_MEDIUM, PADDING_SMALL), pady=PADDING_MEDIUM)
        
        # Right column for recommendations and stats (1/3 width)
        right_column = tk.Frame(main_frame, bg=BG_COLOR, width=300)
        right_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING_MEDIUM), pady=PADDING_MEDIUM)
        right_column.pack_propagate(False)
        
        # Create scrollable frame for watchlist
        self.scroll_frame = ScrollableFrame(left_column, bg=BG_COLOR)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Watchlist header with count badge
        header_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, anchor='w', pady=(0, PADDING_MEDIUM))
        
        header_label = tk.Label(
            header_frame,
            text="My Watchlist",
            font=("Helvetica", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        header_label.pack(side=tk.LEFT)
        
        # Get watchlist
        watchlist = self.user_manager.get_watchlist()
        
        # Add count badge
        count_badge = tk.Label(
            header_frame,
            text=str(len(watchlist)),
            font=("Helvetica", 12, "bold"),
            bg=PRIMARY_COLOR,
            fg=TEXT_COLOR_INVERSE,
            padx=10,
            pady=2,
            borderwidth=0
        )
        count_badge.pack(side=tk.LEFT, padx=10)
        
        # Add sorting options
        sort_frame = tk.Frame(header_frame, bg=BG_COLOR)
        sort_frame.pack(side=tk.RIGHT)
        
        sort_label = tk.Label(
            sort_frame,
            text="Sort by:",
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT
        )
        sort_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Sort buttons
        self.sort_options = ["Date Added", "Title", "Rating"]
        self.active_sort = tk.StringVar(value=self.sort_options[0])
        
        for option in self.sort_options:
            sort_button = tk.Radiobutton(
                sort_frame,
                text=option,
                variable=self.active_sort,
                value=option,
                font=("Helvetica", 10),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                selectcolor=BG_COLOR,
                command=self._resort_watchlist,
                indicatoron=False,
                bd=0,
                padx=8,
                pady=2
            )
            sort_button.pack(side=tk.LEFT, padx=2)
        
        # Watchlist container
        self.watchlist_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        self.watchlist_container.pack(fill=tk.BOTH, expand=True)
        
        if not watchlist:
            # Show an empty state with suggestions
            empty_frame = tk.Frame(self.watchlist_container, bg=BG_COLOR, pady=30)
            empty_frame.pack(fill=tk.X)
            
            empty_icon = tk.Label(
                empty_frame,
                text="🎬",
                font=("Helvetica", 48),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT
            )
            empty_icon.pack(pady=10)
            
            empty_title = tk.Label(
                empty_frame,
                text="Your watchlist is empty",
                font=("Helvetica", 16, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=5
            )
            empty_title.pack()
            
            empty_desc = tk.Label(
                empty_frame,
                text="Add movies to your watchlist to keep track of what you want to watch next.",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                wraplength=400
            )
            empty_desc.pack(pady=5)
            
            # Add suggestions from popular movies
            suggestion_label = tk.Label(
                empty_frame,
                text="Try adding some popular movies:",
                font=("Helvetica", 14),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=15
            )
            suggestion_label.pack()
            
            # Get some popular movie suggestions
            popular_movies = self.data_handler.get_popular_movies(limit=3)
            suggestions_frame = tk.Frame(empty_frame, bg=BG_COLOR)
            suggestions_frame.pack(pady=10)
            
            for movie in popular_movies:
                suggestion = tk.Frame(
                    suggestions_frame,
                    bg=BG_COLOR,
                    padx=10,
                    pady=5,
                    bd=1,
                    relief=tk.SOLID
                )
                suggestion.pack(side=tk.LEFT, padx=10, pady=5)
                
                movie_title = tk.Label(
                    suggestion,
                    text=truncate_text(movie.get('title', 'Unknown'), 25),
                    font=("Helvetica", 12, "bold"),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR
                )
                movie_title.pack(pady=5)
                
                view_button = HoverButton(
                    suggestion,
                    text="View Details",
                    **BUTTON_STYLE,
                    command=lambda m=movie: self._handle_view(m)
                )
                view_button.pack(pady=5)
        else:
            # Sort the watchlist based on current criteria
            self._populate_watchlist(watchlist)
        
        # Now populate the right sidebar
        self._create_sidebar(right_column, watchlist)
        
        # Set status
        self.set_status(f"Watchlist: {len(watchlist)} movies")
    
    def _populate_watchlist(self, watchlist):
        """Populate the watchlist with movie items"""
        # Clear existing items
        for widget in self.watchlist_container.winfo_children():
            widget.destroy()
            
        # Sort watchlist based on selected option
        sort_option = self.active_sort.get()
        if sort_option == "Date Added":
            sorted_watchlist = sorted(watchlist, key=lambda m: m.get('added_at', ''), reverse=True)
        elif sort_option == "Title":
            sorted_watchlist = sorted(watchlist, key=lambda m: m.get('title', '').lower())
        elif sort_option == "Rating":
            sorted_watchlist = sorted(watchlist, key=lambda m: float(m.get('vote_average', 0)), reverse=True)
        else:
            sorted_watchlist = watchlist
            
        # Add each watchlist item with improved styling
        for i, movie in enumerate(sorted_watchlist):
            # Alternate background color for better readability
            bg_color = BG_COLOR if i % 2 == 0 else "#f0f0f5"
            
            # Create a frame for the movie item
            item_frame = tk.Frame(
                self.watchlist_container,
                bg=bg_color,
                padx=PADDING_MEDIUM,
                pady=PADDING_MEDIUM,
                bd=0
            )
            item_frame.pack(fill=tk.X, pady=1)
            
            # Left side with movie info
            info_frame = tk.Frame(item_frame, bg=bg_color)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor='w')
            
            # Movie title with genre icon
            title_frame = tk.Frame(info_frame, bg=bg_color)
            title_frame.pack(fill=tk.X, anchor='w')
            
            # Different icons based on genre if available
            icon_text = "🎬"
            genres = movie.get('genres', [])
            if genres:
                if isinstance(genres, str):
                    genres = [g.strip() for g in genres.split(',')]
                
                # Map genres to emojis
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
                        icon_text = genre_icons[genre]
                        break
            
            # Icon label
            icon_label = tk.Label(
                title_frame,
                text=icon_text,
                font=("Helvetica", 16),
                bg=bg_color,
                fg=PRIMARY_COLOR
            )
            icon_label.pack(side=tk.LEFT, padx=(0, 5))
            
            # Movie title
            title_label = tk.Label(
                title_frame,
                text=movie.get('title', 'Unknown Title'),
                font=("Helvetica", 14, "bold"),
                bg=bg_color,
                fg=TEXT_COLOR,
                anchor='w'
            )
            title_label.pack(side=tk.LEFT)
            
            # Details frame
            details_frame = tk.Frame(info_frame, bg=bg_color, pady=5)
            details_frame.pack(fill=tk.X, anchor='w')
            
            # Year if available
            year = movie.get('release_year', '')
            if year:
                year_label = tk.Label(
                    details_frame,
                    text=f"📅 {year}",
                    font=("Helvetica", 10),
                    bg=bg_color,
                    fg=TEXT_COLOR_LIGHT
                )
                year_label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Rating if available
            rating = movie.get('vote_average', None)
            if rating is not None:
                rating_label = tk.Label(
                    details_frame,
                    text=f"⭐ {rating}/10",
                    font=("Helvetica", 10),
                    bg=bg_color,
                    fg=TEXT_COLOR_LIGHT
                )
                rating_label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Added date
            added_date = movie.get('added_at', '')
            if added_date:
                try:
                    # Format the date nicely
                    date_obj = datetime.fromisoformat(added_date)
                    date_text = f"Added: {date_obj.strftime('%B %d, %Y')}"
                except:
                    # Just take the date part as fallback
                    try:
                        date_part = added_date.split('T')[0]
                        date_text = f"Added: {date_part}"
                    except:
                        date_text = f"Added: {added_date}"
                
                date_label = tk.Label(
                    details_frame,
                    text=date_text,
                    font=("Helvetica", 10),
                    bg=bg_color,
                    fg=TEXT_COLOR_LIGHT
                )
                date_label.pack(side=tk.LEFT)
            
            # Right side with buttons
            button_frame = tk.Frame(item_frame, bg=bg_color)
            button_frame.pack(side=tk.RIGHT, padx=(PADDING_MEDIUM, 0))
            
            # View button
            view_button = HoverButton(
                button_frame,
                text="View Details",
                **BUTTON_STYLE,
                command=lambda m=movie: self._handle_view(m)
            )
            view_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            
            # Mark as watched button (placeholder for future feature)
            watched_button = HoverButton(
                button_frame,
                text="✓ Watched",
                bg="#4CAF50",  # Green
                fg=TEXT_COLOR_INVERSE,
                hover_bg="#388E3C",
                activebackground="#388E3C",
                activeforeground=TEXT_COLOR_INVERSE,
                font=("Helvetica", 12),
                padx=10,
                pady=5,
                bd=0,
                command=lambda m=movie: self._handle_watched(m)
            )
            watched_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
            
            # Remove button
            remove_button = HoverButton(
                button_frame,
                text="Remove",
                **ACCENT_BUTTON_STYLE,
                command=lambda m=movie: self._handle_remove(m)
            )
            remove_button.pack(side=tk.LEFT, padx=PADDING_SMALL)
    
    def _create_sidebar(self, container, watchlist):
        """Create the sidebar with stats and recommendations"""
        # Stats section
        stats_frame = tk.Frame(container, bg=BG_COLOR, bd=1, relief=tk.SOLID, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        stats_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        stats_title = tk.Label(
            stats_frame,
            text="Watchlist Stats",
            font=("Helvetica", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        stats_title.pack(anchor='w', pady=(0, PADDING_MEDIUM))
        
        # Calculate stats
        genres_count = {}
        years_count = {}
        total_rating = 0
        rating_count = 0
        
        for movie in watchlist:
            # Genres
            movie_genres = movie.get('genres', [])
            if movie_genres:
                if isinstance(movie_genres, str):
                    movie_genres = [g.strip() for g in movie_genres.split(',')]
                for genre in movie_genres:
                    if genre:
                        genres_count[genre] = genres_count.get(genre, 0) + 1
            
            # Years
            year = movie.get('release_year', '')
            if year:
                years_count[year] = years_count.get(year, 0) + 1
            
            # Ratings
            rating = movie.get('vote_average', None)
            if rating is not None:
                try:
                    rating_value = float(rating)
                    total_rating += rating_value
                    rating_count += 1
                except:
                    pass
        
        # Display top genres
        if genres_count:
            top_genres = sorted(genres_count.items(), key=lambda x: x[1], reverse=True)[:3]
            
            genres_label = tk.Label(
                stats_frame,
                text="Top Genres:",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w'
            )
            genres_label.pack(fill=tk.X, pady=(0, 5))
            
            for genre, count in top_genres:
                genre_item = tk.Frame(stats_frame, bg=BG_COLOR)
                genre_item.pack(fill=tk.X, pady=2)
                
                genre_name = tk.Label(
                    genre_item,
                    text=genre,
                    font=("Helvetica", 10),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR,
                    anchor='w'
                )
                genre_name.pack(side=tk.LEFT)
                
                genre_count = tk.Label(
                    genre_item,
                    text=str(count),
                    font=("Helvetica", 10, "bold"),
                    bg=PRIMARY_COLOR,
                    fg=TEXT_COLOR_INVERSE,
                    padx=5
                )
                genre_count.pack(side=tk.RIGHT)
        
        # Display average rating
        if rating_count > 0:
            avg_rating = total_rating / rating_count
            
            rating_frame = tk.Frame(stats_frame, bg=BG_COLOR, pady=5)
            rating_frame.pack(fill=tk.X)
            
            rating_label = tk.Label(
                rating_frame,
                text="Average Rating:",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            )
            rating_label.pack(side=tk.LEFT)
            
            rating_value = tk.Label(
                rating_frame,
                text=f"⭐ {avg_rating:.1f}/10",
                font=("Helvetica", 12, "bold"),
                bg=BG_COLOR,
                fg=ACCENT_COLOR
            )
            rating_value.pack(side=tk.RIGHT)
        
        # Add distribution by decade if we have year data
        if years_count and len(years_count) > 1:
            decades = {}
            for year_str, count in years_count.items():
                try:
                    year = int(year_str)
                    decade = (year // 10) * 10
                    decade_name = f"{decade}s"
                    decades[decade_name] = decades.get(decade_name, 0) + count
                except:
                    pass
            
            if decades:
                decades_label = tk.Label(
                    stats_frame,
                    text="Movies by Decade:",
                    font=("Helvetica", 12),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR,
                    anchor='w'
                )
                decades_label.pack(fill=tk.X, pady=(10, 5))
                
                # Sort decades
                sorted_decades = sorted(decades.items(), key=lambda x: x[0])
                
                for decade, count in sorted_decades:
                    decade_item = tk.Frame(stats_frame, bg=BG_COLOR)
                    decade_item.pack(fill=tk.X, pady=2)
                    
                    decade_name = tk.Label(
                        decade_item,
                        text=decade,
                        font=("Helvetica", 10),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR,
                        anchor='w'
                    )
                    decade_name.pack(side=tk.LEFT)
                    
                    decade_count = tk.Label(
                        decade_item,
                        text=str(count),
                        font=("Helvetica", 10, "bold"),
                        bg=PRIMARY_COLOR,
                        fg=TEXT_COLOR_INVERSE,
                        padx=5
                    )
                    decade_count.pack(side=tk.RIGHT)
        
        # If we have a recommender and watchlist, show recommendations
        if self.recommender and watchlist and len(watchlist) > 0:
            rec_frame = tk.Frame(container, bg=BG_COLOR, bd=1, relief=tk.SOLID, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
            rec_frame.pack(fill=tk.X)
            
            rec_title = tk.Label(
                rec_frame,
                text="Recommended For You",
                font=("Helvetica", 14, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            )
            rec_title.pack(anchor='w', pady=(0, PADDING_MEDIUM))
            
            # Get recommendations based on watchlist
            try:
                recommendations = self.recommender.get_recommendations_for_watchlist(
                    watchlist, limit=3
                )
                
                if recommendations:
                    for rec in recommendations:
                        rec_item = tk.Frame(rec_frame, bg=BG_COLOR, pady=5)
                        rec_item.pack(fill=tk.X)
                        
                        title_label = tk.Label(
                            rec_item,
                            text=truncate_text(rec.get('title', 'Unknown'), 25),
                            font=("Helvetica", 12, "bold"),
                            bg=BG_COLOR,
                            fg=TEXT_COLOR,
                            anchor='w'
                        )
                        title_label.pack(anchor='w')
                        
                        # Details row
                        details_frame = tk.Frame(rec_item, bg=BG_COLOR)
                        details_frame.pack(fill=tk.X, pady=2)
                        
                        # Year if available
                        year = rec.get('release_year', '')
                        if not year and 'release_date' in rec:
                            year_match = re.search(r'(\d{4})', str(rec['release_date']))
                            if year_match:
                                year = year_match.group(1)
                        
                        if year:
                            year_label = tk.Label(
                                details_frame,
                                text=f"{year}",
                                font=("Helvetica", 10),
                                bg=BG_COLOR,
                                fg=TEXT_COLOR_LIGHT
                            )
                            year_label.pack(side=tk.LEFT, padx=(0, 10))
                        
                        # Rating if available
                        rating = rec.get('vote_average', 0)
                        if rating:
                            rating_label = tk.Label(
                                details_frame,
                                text=f"⭐ {rating}/10",
                                font=("Helvetica", 10),
                                bg=BG_COLOR,
                                fg=ACCENT_COLOR
                            )
                            rating_label.pack(side=tk.LEFT)
                        
                        # Button row
                        button_frame = tk.Frame(rec_item, bg=BG_COLOR, pady=5)
                        button_frame.pack(fill=tk.X)
                        
                        view_button = HoverButton(
                            button_frame,
                            text="View",
                            **BUTTON_STYLE,
                            command=lambda m=rec: self._handle_view(m)
                        )
                        view_button.pack(side=tk.LEFT, padx=(0, 5))
                else:
                    no_rec_label = tk.Label(
                        rec_frame,
                        text="Add more movies to your watchlist to get recommendations",
                        font=("Helvetica", 10),
                        bg=BG_COLOR,
                        fg=TEXT_COLOR_LIGHT,
                        wraplength=250,
                        justify=tk.LEFT
                    )
                    no_rec_label.pack()
            except:
                error_label = tk.Label(
                    rec_frame,
                    text="Unable to generate recommendations at this time",
                    font=("Helvetica", 10),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR_LIGHT,
                    wraplength=250
                )
                error_label.pack()
    
    def _resort_watchlist(self):
        """Resort the watchlist based on the selected criteria"""
        watchlist = self.user_manager.get_watchlist()
        self._populate_watchlist(watchlist)
    
    def _handle_view(self, movie):
        """Handle view button press"""
        if self.on_movie_click:
            self.on_movie_click(movie)
    
    def _handle_remove(self, movie):
        """Handle remove button press"""
        if self.on_remove:
            movie_id = movie.get('id')
            if movie_id:
                # Confirm removal
                if show_confirmation("Remove Movie", f"Are you sure you want to remove '{movie.get('title', 'this movie')}' from your watchlist?"):
                    self.on_remove(movie_id)
                    self.update_screen()
    
    def _handle_watched(self, movie):
        """Handle marking a movie as watched"""
        # This is a placeholder for future functionality
        movie_title = movie.get('title', 'this movie')
        show_info("Watched", f"You've marked '{movie_title}' as watched! This feature will be available soon.")
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Recreate UI to reflect any changes
        self._create_ui()

class BookmarkScreen(BaseScreen):
    """Screen for displaying and managing user's bookmarks"""
    
    def __init__(self, parent, user_manager, data_handler, **kwargs):
        # Extract callbacks before passing to super()
        self.on_movie_click = kwargs.pop('on_movie_click', None)
        self.on_remove = kwargs.pop('on_remove', None)
        self.recommender = kwargs.pop('recommender', None)
        
        # Initialize the base screen
        super().__init__(parent, data_handler, user_manager, **kwargs)
        
        # Set screen title
        self.set_title("My Bookmarks")
        
        # Initialize the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the bookmarks screen UI"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get current user
        user = self.user_manager.get_current_user()
        if not user:
            # Show a more attractive message if not logged in
            login_frame = tk.Frame(self.content_frame, bg=BG_COLOR, padx=50, pady=50)
            login_frame.pack(expand=True)
            
            not_logged_label = tk.Label(
                login_frame,
                text="Please login to access your bookmarks",
                font=("Helvetica", 18, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=20
            )
            not_logged_label.pack()
            
            message_label = tk.Label(
                login_frame,
                text="Your bookmarks allow you to save your favorite movies\nand get personalized recommendations based on your taste.",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                justify=tk.CENTER,
                pady=10
            )
            message_label.pack()
            
            login_button = HoverButton(
                login_frame,
                text="Login",
                font=("Helvetica", 14),
                bg=PRIMARY_COLOR,
                fg=TEXT_COLOR_INVERSE,
                hover_bg=SECONDARY_COLOR,
                activebackground=SECONDARY_COLOR,
                activeforeground=TEXT_COLOR_INVERSE,
                padx=30,
                pady=10,
                bd=0,
                command=lambda: self.on_back()
            )
            login_button.pack(pady=20)
            
            return
        
        # Create a main frame with two columns
        main_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column for bookmarks (2/3 width)
        left_column = tk.Frame(main_frame, bg=BG_COLOR)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(PADDING_MEDIUM, PADDING_SMALL), pady=PADDING_MEDIUM)
        
        # Right column for recommendations and stats (1/3 width)
        right_column = tk.Frame(main_frame, bg=BG_COLOR, width=300)
        right_column.pack(side=tk.LEFT, fill=tk.Y, padx=(0, PADDING_MEDIUM), pady=PADDING_MEDIUM)
        right_column.pack_propagate(False)
        
        # Create scrollable frame for bookmarks
        self.scroll_frame = ScrollableFrame(left_column, bg=BG_COLOR)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bookmarks header with count badge
        header_frame = tk.Frame(self.scroll_frame.scrollable_frame, bg=BG_COLOR)
        header_frame.pack(fill=tk.X, anchor='w', pady=(0, PADDING_MEDIUM))
        
        header_label = tk.Label(
            header_frame,
            text="My Bookmarks",
            font=("Helvetica", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            anchor='w'
        )
        header_label.pack(side=tk.LEFT)
        
        # Get bookmarks
        bookmarks = self.user_manager.get_bookmarks()
        
        # Add count badge
        count_badge = tk.Label(
            header_frame,
            text=str(len(bookmarks)),
            font=("Helvetica", 12, "bold"),
            bg=ACCENT_COLOR,  # Different color than watchlist
            fg=TEXT_COLOR_INVERSE,
            padx=10,
            pady=2,
            borderwidth=0
        )
        count_badge.pack(side=tk.LEFT, padx=10)
        
        # Add sorting options
        sort_frame = tk.Frame(header_frame, bg=BG_COLOR)
        sort_frame.pack(side=tk.RIGHT)
        
        sort_label = tk.Label(
            sort_frame,
            text="Sort by:",
            font=("Helvetica", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR_LIGHT
        )
        sort_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Sort buttons
        self.sort_options = ["Date Added", "Title", "Rating"]
        self.active_sort = tk.StringVar(value=self.sort_options[0])
        
        for option in self.sort_options:
            sort_button = tk.Radiobutton(
                sort_frame,
                text=option,
                variable=self.active_sort,
                value=option,
                font=("Helvetica", 10),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                selectcolor=BG_COLOR,
                command=self._resort_bookmarks,
                indicatoron=False,
                bd=0,
                padx=8,
                pady=2
            )
            sort_button.pack(side=tk.LEFT, padx=2)
        
        # Bookmarks container
        self.bookmarks_container = tk.Frame(
            self.scroll_frame.scrollable_frame,
            bg=BG_COLOR
        )
        self.bookmarks_container.pack(fill=tk.BOTH, expand=True)
        
        if not bookmarks:
            # Show an empty state with suggestions
            empty_frame = tk.Frame(self.bookmarks_container, bg=BG_COLOR, pady=30)
            empty_frame.pack(fill=tk.X)
            
            empty_icon = tk.Label(
                empty_frame,
                text="⭐",  # Star icon for bookmarks
                font=("Helvetica", 48),
                bg=BG_COLOR,
                fg=ACCENT_COLOR
            )
            empty_icon.pack(pady=10)
            
            empty_title = tk.Label(
                empty_frame,
                text="Your bookmarks are empty",
                font=("Helvetica", 16, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=5
            )
            empty_title.pack()
            
            empty_desc = tk.Label(
                empty_frame,
                text="Add movies to your bookmarks to save your favorite movies for easy access.",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR_LIGHT,
                wraplength=400
            )
            empty_desc.pack(pady=5)
            
            # Add suggestions from trending movies
            suggestion_label = tk.Label(
                empty_frame,
                text="Try adding some trending movies:",
                font=("Helvetica", 14),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                pady=15
            )
            suggestion_label.pack()
            
            # Get some trending movie suggestions
            trending_movies = self.data_handler.get_trending_movies(limit=3)
            suggestions_frame = tk.Frame(empty_frame, bg=BG_COLOR)
            suggestions_frame.pack(pady=10)
            
            for movie in trending_movies:
                suggestion = tk.Frame(
                    suggestions_frame,
                    bg=BG_COLOR,
                    padx=10,
                    pady=5,
                    bd=1,
                    relief=tk.SOLID
                )
                suggestion.pack(side=tk.LEFT, padx=10, pady=5)
                
                movie_title = tk.Label(
                    suggestion,
                    text=truncate_text(movie.get('title', 'Unknown'), 25),
                    font=("Helvetica", 12, "bold"),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR
                )
                movie_title.pack(pady=5)
                
                view_button = HoverButton(
                    suggestion,
                    text="View Details",
                    **BUTTON_STYLE,
                    command=lambda m=movie: self._handle_view(m)
                )
                view_button.pack(pady=5)
        else:
            # Sort the bookmarks based on current criteria
            self._populate_bookmarks(bookmarks)
        
        # Now populate the right sidebar
        self._create_sidebar(right_column, bookmarks)
        
        # Set status
        self.set_status(f"Bookmarks: {len(bookmarks)} movies")
    
    def _populate_bookmarks(self, bookmarks):
        """Populate the bookmarks with movie items"""
        # Clear existing items
        for widget in self.bookmarks_container.winfo_children():
            widget.destroy()
            
        # Sort bookmarks based on selected option
        sort_option = self.active_sort.get()
        if sort_option == "Date Added":
            sorted_bookmarks = sorted(bookmarks, key=lambda m: m.get('added_at', ''), reverse=True)
        elif sort_option == "Title":
            sorted_bookmarks = sorted(bookmarks, key=lambda m: m.get('title', '').lower())
        elif sort_option == "Rating":
            sorted_bookmarks = sorted(bookmarks, key=lambda m: float(m.get('vote_average', 0)), reverse=True)
        else:
            sorted_bookmarks = bookmarks
            
        # Use a grid layout for bookmarks for a different look from watchlist
        for i, movie in enumerate(sorted_bookmarks):
            # Create a card-style frame for each bookmark
            card_frame = tk.Frame(
                self.bookmarks_container,
                bg=BG_COLOR,
                padx=PADDING_MEDIUM,
                pady=PADDING_MEDIUM,
                bd=1,
                relief=tk.SOLID
            )
            
            # Arrange in a 2-column grid
            row = i // 2
            col = i % 2
            card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configure grid to expand correctly
            self.bookmarks_container.grid_columnconfigure(0, weight=1)
            self.bookmarks_container.grid_columnconfigure(1, weight=1)
            
            # Movie title with favorite star icon
            title_frame = tk.Frame(card_frame, bg=BG_COLOR)
            title_frame.pack(fill=tk.X, anchor='w', pady=(0, 10))
            
            star_label = tk.Label(
                title_frame,
                text="⭐",
                font=("Helvetica", 14),
                bg=BG_COLOR,
                fg=ACCENT_COLOR
            )
            star_label.pack(side=tk.LEFT, padx=(0, 5))
            
            title_label = tk.Label(
                title_frame,
                text=truncate_text(movie.get('title', 'Unknown Title'), 30),
                font=("Helvetica", 12, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w'
            )
            title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Details frame for year and rating
            details_frame = tk.Frame(card_frame, bg=BG_COLOR, pady=5)
            details_frame.pack(fill=tk.X)
            
            # Year if available
            year = movie.get('release_year', '')
            if year:
                year_label = tk.Label(
                    details_frame,
                    text=f"📅 {year}",
                    font=("Helvetica", 10),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR_LIGHT
                )
                year_label.pack(side=tk.LEFT, padx=(0, 15))
            
            # Rating if available
            rating = movie.get('vote_average', None)
            if rating is not None:
                rating_label = tk.Label(
                    details_frame,
                    text=f"⭐ {rating}/10",
                    font=("Helvetica", 10),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR_LIGHT
                )
                rating_label.pack(side=tk.LEFT)
            
            # Added date in a separate row
            added_date = movie.get('added_at', '')
            if added_date:
                try:
                    # Format the date nicely
                    date_obj = datetime.fromisoformat(added_date)
                    date_text = f"Added: {date_obj.strftime('%B %d, %Y')}"
                except:
                    # Just take the date part as fallback
                    try:
                        date_part = added_date.split('T')[0]
                        date_text = f"Added: {date_part}"
                    except:
                        date_text = f"Added: {added_date}"
                
                date_frame = tk.Frame(card_frame, bg=BG_COLOR)
                date_frame.pack(fill=tk.X, pady=5)
                
                date_label = tk.Label(
                    date_frame,
                    text=date_text,
                    font=("Helvetica", 9, "italic"),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR_LIGHT
                )
                date_label.pack(anchor='w')
            
            # Buttons frame
            button_frame = tk.Frame(card_frame, bg=BG_COLOR, pady=10)
            button_frame.pack(fill=tk.X)
            
            # View button
            view_button = HoverButton(
                button_frame,
                text="View",
                **BUTTON_STYLE,
                command=lambda m=movie: self._handle_view(m)
            )
            view_button.pack(side=tk.LEFT, padx=(0, 5))
            
            # Remove button
            remove_button = HoverButton(
                button_frame,
                text="Remove",
                **ACCENT_BUTTON_STYLE,
                command=lambda m=movie: self._handle_remove(m)
            )
            remove_button.pack(side=tk.LEFT)
    
    def _create_sidebar(self, container, bookmarks):
        """Create the sidebar with stats and similar recommendations"""
        # Stats section
        stats_frame = tk.Frame(container, bg=BG_COLOR, bd=1, relief=tk.SOLID, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
        stats_frame.pack(fill=tk.X, pady=(0, PADDING_MEDIUM))
        
        stats_title = tk.Label(
            stats_frame,
            text="Bookmarks Stats",
            font=("Helvetica", 14, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        stats_title.pack(anchor='w', pady=(0, PADDING_MEDIUM))
        
        # Calculate stats - similar to watchlist but with some differences
        genres_count = {}
        years_count = {}
        total_rating = 0
        rating_count = 0
        
        for movie in bookmarks:
            # Genres
            movie_genres = movie.get('genres', [])
            if movie_genres:
                if isinstance(movie_genres, str):
                    movie_genres = [g.strip() for g in movie_genres.split(',')]
                for genre in movie_genres:
                    if genre:
                        genres_count[genre] = genres_count.get(genre, 0) + 1
            
            # Years
            year = movie.get('release_year', '')
            if year:
                years_count[year] = years_count.get(year, 0) + 1
            
            # Ratings
            rating = movie.get('vote_average', None)
            if rating is not None:
                try:
                    rating_value = float(rating)
                    total_rating += rating_value
                    rating_count += 1
                except:
                    pass
        
        # Display favorite genres
        if genres_count:
            top_genres = sorted(genres_count.items(), key=lambda x: x[1], reverse=True)[:3]
            
            genres_label = tk.Label(
                stats_frame,
                text="Favorite Genres:",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR,
                anchor='w'
            )
            genres_label.pack(fill=tk.X, pady=(0, 5))
            
            for genre, count in top_genres:
                genre_item = tk.Frame(stats_frame, bg=BG_COLOR)
                genre_item.pack(fill=tk.X, pady=2)
                
                genre_name = tk.Label(
                    genre_item,
                    text=genre,
                    font=("Helvetica", 10),
                    bg=BG_COLOR,
                    fg=TEXT_COLOR,
                    anchor='w'
                )
                genre_name.pack(side=tk.LEFT)
                
                genre_count = tk.Label(
                    genre_item,
                    text=str(count),
                    font=("Helvetica", 10, "bold"),
                    bg=ACCENT_COLOR,  # Use accent color instead of primary
                    fg=TEXT_COLOR_INVERSE,
                    padx=5
                )
                genre_count.pack(side=tk.RIGHT)
        
        # Display average rating
        if rating_count > 0:
            avg_rating = total_rating / rating_count
            
            rating_frame = tk.Frame(stats_frame, bg=BG_COLOR, pady=5)
            rating_frame.pack(fill=tk.X)
            
            rating_label = tk.Label(
                rating_frame,
                text="Average Rating:",
                font=("Helvetica", 12),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            )
            rating_label.pack(side=tk.LEFT)
            
            rating_value = tk.Label(
                rating_frame,
                text=f"⭐ {avg_rating:.1f}/10",
                font=("Helvetica", 12, "bold"),
                bg=BG_COLOR,
                fg=ACCENT_COLOR
            )
            rating_value.pack(side=tk.RIGHT)
        
        # If we have a recommender and bookmarks, show similar movies
        if self.recommender and bookmarks and len(bookmarks) > 0:
            similar_frame = tk.Frame(container, bg=BG_COLOR, bd=1, relief=tk.SOLID, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
            similar_frame.pack(fill=tk.X)
            
            similar_title = tk.Label(
                similar_frame,
                text="You Might Also Like",
                font=("Helvetica", 14, "bold"),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            )
            similar_title.pack(anchor='w', pady=(0, PADDING_MEDIUM))
            
            # Pick a random movie from bookmarks to get similar movies
            if bookmarks:
                import random
                random_movie = random.choice(bookmarks)
                movie_id = random_movie.get('id')
                
                if movie_id:
                    try:
                        similar_movies = self.recommender.get_similar_movies(
                            movie_id, limit=3
                        )
                        
                        if similar_movies:
                            for movie in similar_movies:
                                movie_item = tk.Frame(similar_frame, bg=BG_COLOR, pady=5)
                                movie_item.pack(fill=tk.X)
                                
                                title_label = tk.Label(
                                    movie_item,
                                    text=truncate_text(movie.get('title', 'Unknown'), 25),
                                    font=("Helvetica", 12, "bold"),
                                    bg=BG_COLOR,
                                    fg=TEXT_COLOR,
                                    anchor='w'
                                )
                                title_label.pack(anchor='w')
                                
                                # Details row
                                details_frame = tk.Frame(movie_item, bg=BG_COLOR)
                                details_frame.pack(fill=tk.X, pady=2)
                                
                                # Year if available
                                year = movie.get('release_year', '')
                                if not year and 'release_date' in movie:
                                    year_match = re.search(r'(\d{4})', str(movie['release_date']))
                                    if year_match:
                                        year = year_match.group(1)
                                
                                if year:
                                    year_label = tk.Label(
                                        details_frame,
                                        text=f"{year}",
                                        font=("Helvetica", 10),
                                        bg=BG_COLOR,
                                        fg=TEXT_COLOR_LIGHT
                                    )
                                    year_label.pack(side=tk.LEFT, padx=(0, 10))
                                
                                # Rating if available
                                rating = movie.get('vote_average', 0)
                                if rating:
                                    rating_label = tk.Label(
                                        details_frame,
                                        text=f"⭐ {rating}/10",
                                        font=("Helvetica", 10),
                                        bg=BG_COLOR,
                                        fg=ACCENT_COLOR
                                    )
                                    rating_label.pack(side=tk.LEFT)
                                
                                # Button row
                                button_frame = tk.Frame(movie_item, bg=BG_COLOR, pady=5)
                                button_frame.pack(fill=tk.X)
                                
                                view_button = HoverButton(
                                    button_frame,
                                    text="View",
                                    **BUTTON_STYLE,
                                    command=lambda m=movie: self._handle_view(m)
                                )
                                view_button.pack(side=tk.LEFT)
                        else:
                            no_rec_label = tk.Label(
                                similar_frame,
                                text="No similar movies found",
                                font=("Helvetica", 10),
                                bg=BG_COLOR,
                                fg=TEXT_COLOR_LIGHT,
                                wraplength=250
                            )
                            no_rec_label.pack()
                    except Exception as e:
                        error_label = tk.Label(
                            similar_frame,
                            text=f"Unable to find similar movies",
                            font=("Helvetica", 10),
                            bg=BG_COLOR,
                            fg=TEXT_COLOR_LIGHT,
                            wraplength=250
                        )
                        error_label.pack()
    
    def _resort_bookmarks(self):
        """Resort the bookmarks based on the selected criteria"""
        bookmarks = self.user_manager.get_bookmarks()
        self._populate_bookmarks(bookmarks)
    
    def _handle_view(self, movie):
        """Handle view button press"""
        if self.on_movie_click:
            self.on_movie_click(movie)
    
    def _handle_remove(self, movie):
        """Handle remove button press"""
        if self.on_remove:
            movie_id = movie.get('id')
            if movie_id:
                # Confirm removal
                if show_confirmation("Remove Bookmark", f"Are you sure you want to remove '{movie.get('title', 'this movie')}' from your bookmarks?"):
                    self.on_remove(movie_id)
                    self.update_screen()
    
    def update_screen(self):
        """Update the screen content"""
        super().update_screen()
        # Recreate UI to reflect any changes
        self._create_ui()
