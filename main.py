"""
Movie Recommendation System - Main Entry Point
This file initializes the application and starts the UI.
"""
import os
import tkinter as tk
from tkinter import ttk
from app import MovieRecommendationApp
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, APP_MIN_WIDTH, APP_MIN_HEIGHT
from assets.styles import apply_styles

def center_window(window, width, height):
    """Center a tkinter window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    """Initialize and run the application"""
    # Create the Tkinter root window
    root = tk.Tk()
    root.title(APP_TITLE)
    root.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
    
    # Center the window on screen
    center_window(root, APP_WIDTH, APP_HEIGHT)
    
    # Set icon if available
    # Note: We can't use actual image files, so we'll skip the icon
    
    # Configure ttk styles
    style = ttk.Style()
    apply_styles(style)
    
    # Create and start the application
    app = MovieRecommendationApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    # Ensure user_data directory exists
    os.makedirs("user_data", exist_ok=True)
    main()
