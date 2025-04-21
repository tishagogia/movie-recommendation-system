"""
Manages user authentication, profiles, and user-related data
"""
import os
import json
import hashlib
import time
from datetime import datetime
import uuid
from config import USER_DATA_PATH, PASSWORD_MIN_LENGTH, USERNAME_MIN_LENGTH
from utils import create_directory_if_not_exists, save_json_data, load_json_data

class UserManager:
    def __init__(self):
        self.users_file = os.path.join(USER_DATA_PATH, "users.json")
        self.current_user = None
        self._load_users()
    
    def _load_users(self):
        """Load user data from JSON file"""
        create_directory_if_not_exists(USER_DATA_PATH)
        self.users = load_json_data(self.users_file, default={"users": []})
    
    def _save_users(self):
        """Save user data to JSON file"""
        save_json_data(self.users, self.users_file)
    
    def _hash_password(self, password):
        """Hash a password using SHA-256"""
        salt = "moviemaster_salt"  # In production, use a secure random salt per user
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register(self, username, password, email=""):
        """Register a new user"""
        # Validate inputs
        if not username or len(username) < USERNAME_MIN_LENGTH:
            return False, f"Username must be at least {USERNAME_MIN_LENGTH} characters"
        
        if not password or len(password) < PASSWORD_MIN_LENGTH:
            return False, f"Password must be at least {PASSWORD_MIN_LENGTH} characters"
        
        # Check if username already exists
        if any(user["username"].lower() == username.lower() for user in self.users["users"]):
            return False, "Username already exists"
        
        # Create user object
        user_id = str(uuid.uuid4())
        new_user = {
            "id": user_id,
            "username": username,
            "password_hash": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "profile": {
                "display_name": username,
                "bio": "",
                "preferences": {
                    "favorite_genres": [],
                    "favorite_directors": [],
                    "favorite_actors": []
                }
            }
        }
        
        # Add user and save
        self.users["users"].append(new_user)
        self._save_users()
        
        # Create user data directory and files
        user_dir = os.path.join(USER_DATA_PATH, user_id)
        create_directory_if_not_exists(user_dir)
        
        # Initialize watchlist and bookmarks
        watchlist_file = os.path.join(user_dir, "watchlist.json")
        bookmarks_file = os.path.join(user_dir, "bookmarks.json")
        
        save_json_data({"movies": []}, watchlist_file)
        save_json_data({"movies": []}, bookmarks_file)
        
        return True, "Registration successful"
    
    def login(self, username, password):
        """Log in a user"""
        if not username or not password:
            return False, "Username and password are required"
        
        # Find user
        user = None
        for u in self.users["users"]:
            if u["username"].lower() == username.lower():
                user = u
                break
        
        if not user:
            return False, "Invalid username or password"
        
        # Check password
        if user["password_hash"] != self._hash_password(password):
            return False, "Invalid username or password"
        
        # Update last login time
        user["last_login"] = datetime.now().isoformat()
        self._save_users()
        
        # Set current user
        self.current_user = user
        
        return True, "Login successful"
    
    def logout(self):
        """Log out the current user"""
        self.current_user = None
        return True, "Logout successful"
    
    def get_current_user(self):
        """Get the current logged-in user"""
        return self.current_user
    
    def update_profile(self, profile_data):
        """Update the current user's profile"""
        if not self.current_user:
            return False, "No user logged in"
        
        # Update profile fields
        self.current_user["profile"].update(profile_data)
        
        # Save changes
        self._save_users()
        
        return True, "Profile updated successfully"
    
    def get_watchlist(self):
        """Get the current user's watchlist"""
        if not self.current_user:
            return []
        
        user_id = self.current_user["id"]
        watchlist_file = os.path.join(USER_DATA_PATH, user_id, "watchlist.json")
        watchlist_data = load_json_data(watchlist_file, default={"movies": []})
        
        return watchlist_data["movies"]
    
    def add_to_watchlist(self, movie):
        """Add a movie to the current user's watchlist"""
        if not self.current_user or not movie:
            return False, "No user logged in or invalid movie"
        
        user_id = self.current_user["id"]
        watchlist_file = os.path.join(USER_DATA_PATH, user_id, "watchlist.json")
        watchlist_data = load_json_data(watchlist_file, default={"movies": []})
        
        # Check if movie is already in watchlist
        movie_id = movie.get("id")
        if any(m.get("id") == movie_id for m in watchlist_data["movies"]):
            return False, "Movie already in watchlist"
        
        # Add movie with timestamp
        watchlist_entry = {
            "id": movie_id,
            "title": movie.get("title", "Unknown Title"),
            "added_at": datetime.now().isoformat(),
            "poster_path": movie.get("poster_path", ""),
            "release_year": movie.get("release_year", ""),
            "vote_average": movie.get("vote_average", 0)
        }
        
        watchlist_data["movies"].append(watchlist_entry)
        save_json_data(watchlist_data, watchlist_file)
        
        return True, "Movie added to watchlist"
    
    def remove_from_watchlist(self, movie_id):
        """Remove a movie from the current user's watchlist"""
        if not self.current_user:
            return False, "No user logged in"
        
        user_id = self.current_user["id"]
        watchlist_file = os.path.join(USER_DATA_PATH, user_id, "watchlist.json")
        watchlist_data = load_json_data(watchlist_file, default={"movies": []})
        
        # Filter out the movie to remove
        original_count = len(watchlist_data["movies"])
        watchlist_data["movies"] = [m for m in watchlist_data["movies"] if m.get("id") != movie_id]
        
        if len(watchlist_data["movies"]) == original_count:
            return False, "Movie not found in watchlist"
        
        save_json_data(watchlist_data, watchlist_file)
        
        return True, "Movie removed from watchlist"
    
    def get_bookmarks(self):
        """Get the current user's bookmarked movies"""
        if not self.current_user:
            return []
        
        user_id = self.current_user["id"]
        bookmarks_file = os.path.join(USER_DATA_PATH, user_id, "bookmarks.json")
        bookmarks_data = load_json_data(bookmarks_file, default={"movies": []})
        
        return bookmarks_data["movies"]
    
    def add_bookmark(self, movie):
        """Add a movie to the current user's bookmarks"""
        if not self.current_user or not movie:
            return False, "No user logged in or invalid movie"
        
        user_id = self.current_user["id"]
        bookmarks_file = os.path.join(USER_DATA_PATH, user_id, "bookmarks.json")
        bookmarks_data = load_json_data(bookmarks_file, default={"movies": []})
        
        # Check if movie is already bookmarked
        movie_id = movie.get("id")
        if any(m.get("id") == movie_id for m in bookmarks_data["movies"]):
            return False, "Movie already bookmarked"
        
        # Add movie with timestamp
        bookmark_entry = {
            "id": movie_id,
            "title": movie.get("title", "Unknown Title"),
            "added_at": datetime.now().isoformat(),
            "poster_path": movie.get("poster_path", ""),
            "release_year": movie.get("release_year", ""),
            "vote_average": movie.get("vote_average", 0)
        }
        
        bookmarks_data["movies"].append(bookmark_entry)
        save_json_data(bookmarks_data, bookmarks_file)
        
        return True, "Movie bookmarked successfully"
    
    def remove_bookmark(self, movie_id):
        """Remove a movie from the current user's bookmarks"""
        if not self.current_user:
            return False, "No user logged in"
        
        user_id = self.current_user["id"]
        bookmarks_file = os.path.join(USER_DATA_PATH, user_id, "bookmarks.json")
        bookmarks_data = load_json_data(bookmarks_file, default={"movies": []})
        
        # Filter out the movie to remove
        original_count = len(bookmarks_data["movies"])
        bookmarks_data["movies"] = [m for m in bookmarks_data["movies"] if m.get("id") != movie_id]
        
        if len(bookmarks_data["movies"]) == original_count:
            return False, "Movie not found in bookmarks"
        
        save_json_data(bookmarks_data, bookmarks_file)
        
        return True, "Bookmark removed successfully"
