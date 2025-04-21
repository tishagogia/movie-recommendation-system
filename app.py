"""
Movie Recommendation System - Main Application
This module contains the main application class that manages screens and controllers.
"""
import tkinter as tk
from tkinter import ttk

from data_handler import DataHandler
from user_manager import UserManager
from movie_recommender import MovieRecommender
from utils import show_error, show_info

from screens.home_screen import HomeScreen
from screens.movie_detail_screen import MovieDetailScreen
from screens.search_screen import SearchScreen
from screens.user_screens import (
    LoginScreen, RegisterScreen, ProfileScreen, 
    WatchlistScreen, BookmarkScreen
)

class MovieRecommendationApp:
    """Main application class for the Movie Recommendation System"""
    
    def __init__(self, root):
        """Initialize the application with root window"""
        self.root = root
        
        # Initialize data handlers and managers
        self.data_handler = DataHandler()
        self.user_manager = UserManager()
        self.recommender = MovieRecommender(self.data_handler)
        
        # Create a container frame for all screens
        self.container = tk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Dictionary to hold all screens
        self.screens = {}
        
        # Initialize screens
        self._init_screens()
        
        # Show the home screen initially
        self.show_screen('home')
    
    def _init_screens(self):
        """Initialize all application screens"""
        self.screens = {
            'home': HomeScreen(
                self.container, 
                self.data_handler,
                self.user_manager,
                self.recommender,
                on_movie_click=self.show_movie_detail,
                on_search=self.show_search,
                on_login=lambda: self.show_screen('login'),
                on_register=lambda: self.show_screen('register'),
                on_logout=self.handle_logout,
                on_profile=lambda: self.show_screen('profile'),
                on_watchlist=lambda: self.show_screen('watchlist'),
                on_bookmarks=lambda: self.show_screen('bookmarks')
            ),
            'search': SearchScreen(
                self.container,
                self.data_handler,
                self.user_manager,
                on_movie_click=self.show_movie_detail,
                on_home=lambda: self.show_screen('home')
            ),
            'movie_detail': MovieDetailScreen(
                self.container,
                self.data_handler,
                self.user_manager,
                self.recommender,
                on_back=lambda: self.show_screen('home'),
                on_add_watchlist=self.handle_add_watchlist,
                on_add_bookmark=self.handle_add_bookmark
            ),
            'login': LoginScreen(
                self.container,
                self.user_manager,
                on_login_success=self.handle_login_success,
                on_cancel=lambda: self.show_screen('home')
            ),
            'register': RegisterScreen(
                self.container,
                self.user_manager,
                on_register_success=self.handle_register_success,
                on_cancel=lambda: self.show_screen('home')
            ),
            'profile': ProfileScreen(
                self.container,
                self.user_manager,
                self.data_handler,
                on_save=self.handle_profile_update,
                on_back=lambda: self.show_screen('home')
            ),
            'watchlist': WatchlistScreen(
                self.container,
                self.user_manager,
                self.data_handler,
                recommender=self.recommender,
                on_movie_click=self.show_movie_detail,
                on_back=lambda: self.show_screen('home'),
                on_remove=self.handle_remove_watchlist
            ),
            'bookmarks': BookmarkScreen(
                self.container,
                self.user_manager,
                self.data_handler,
                recommender=self.recommender,
                on_movie_click=self.show_movie_detail,
                on_back=lambda: self.show_screen('home'),
                on_remove=self.handle_remove_bookmark
            )
        }
    
    def show_screen(self, screen_name):
        """Show a specific screen and hide others"""
        if screen_name not in self.screens:
            show_error("Error", f"Screen '{screen_name}' not found")
            return
        
        # Hide all screens
        for screen in self.screens.values():
            screen.pack_forget()
        
        # Show the requested screen
        screen = self.screens[screen_name]
        screen.update_screen()  # Refresh the screen data
        screen.pack(fill=tk.BOTH, expand=True)
    
    def show_movie_detail(self, movie):
        """Show the movie detail screen for a specific movie"""
        if movie and 'id' in movie:
            detail_screen = self.screens['movie_detail']
            detail_screen.set_movie(movie['id'])
            self.show_screen('movie_detail')
    
    def show_search(self, query='', filters=None):
        """Show the search screen with optional query and filters"""
        search_screen = self.screens['search']
        search_screen.set_search_params(query, filters)
        self.show_screen('search')
    
    def handle_login_success(self):
        """Handle successful login"""
        show_info("Login Successful", "You have successfully logged in!")
        # Refresh screens that need user data
        self.screens['home'].update_screen()
        self.show_screen('home')
    
    def handle_register_success(self):
        """Handle successful registration"""
        show_info("Registration Successful", "Your account has been created successfully! You can now log in.")
        self.show_screen('login')
    
    def handle_logout(self):
        """Handle user logout"""
        success, message = self.user_manager.logout()
        if success:
            show_info("Logout Successful", message)
            # Refresh screens that need user data
            self.screens['home'].update_screen()
            self.show_screen('home')
    
    def handle_profile_update(self, profile_data):
        """Handle profile update"""
        success, message = self.user_manager.update_profile(profile_data)
        if success:
            show_info("Profile Updated", message)
            # Refresh screens that need user data
            self.screens['home'].update_screen()
            self.show_screen('home')
        else:
            show_error("Profile Update Failed", message)
    
    def handle_add_watchlist(self, movie):
        """Handle adding a movie to watchlist"""
        success, message = self.user_manager.add_to_watchlist(movie)
        if success:
            show_info("Added to Watchlist", message)
        else:
            show_error("Watchlist Error", message)
    
    def handle_remove_watchlist(self, movie_id):
        """Handle removing a movie from watchlist"""
        success, message = self.user_manager.remove_from_watchlist(movie_id)
        if success:
            # Refresh the watchlist screen
            self.screens['watchlist'].update_screen()
            show_info("Removed from Watchlist", message)
    
    def handle_add_bookmark(self, movie):
        """Handle adding a movie to bookmarks"""
        success, message = self.user_manager.add_bookmark(movie)
        if success:
            show_info("Added to Bookmarks", message)
        else:
            show_error("Bookmark Error", message)
    
    def handle_remove_bookmark(self, movie_id):
        """Handle removing a movie from bookmarks"""
        success, message = self.user_manager.remove_bookmark(movie_id)
        if success:
            # Refresh the bookmarks screen
            self.screens['bookmarks'].update_screen()
            show_info("Removed from Bookmarks", message)
