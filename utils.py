"""
Utility functions for the Movie Recommendation System
"""
import os
import json
import re
import ast
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def create_directory_if_not_exists(directory_path):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return True
    return False

def save_json_data(data, file_path):
    """Save data to a JSON file"""
    directory = os.path.dirname(file_path)
    create_directory_if_not_exists(directory)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_json_data(file_path, default=None):
    """Load data from a JSON file"""
    if default is None:
        default = {}
    
    if not os.path.exists(file_path):
        return default
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def convert_to_year(date_str):
    """Extract year from a date string"""
    if not isinstance(date_str, str) or not date_str:
        return None
    
    # Try different date formats
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%Y"]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).year
        except ValueError:
            continue
    
    # If all formats fail, try to extract year using regex
    year_match = re.search(r'(\d{4})', date_str)
    if year_match:
        return int(year_match.group(1))
    
    return None

def safe_eval_list(list_str):
    """Safely evaluate a string representation of a list"""
    if not isinstance(list_str, str):
        return []
    
    try:
        result = ast.literal_eval(list_str)
        if isinstance(result, list):
            return result
        return []
    except (SyntaxError, ValueError):
        return []

def extract_names_from_dict_list(dict_list_str):
    """Extract names from a string representation of a list of dictionaries"""
    dict_list = safe_eval_list(dict_list_str)
    names = []
    
    for item in dict_list:
        if isinstance(item, dict) and 'name' in item:
            names.append(item['name'])
    
    return names

def show_error(title, message):
    """Display an error message box"""
    messagebox.showerror(title, message)

def show_info(title, message):
    """Display an information message box"""
    messagebox.showinfo(title, message)

def show_warning(title, message):
    """Display a warning message box"""
    messagebox.showwarning(title, message)

def show_confirmation(title, message):
    """Display a confirmation message box"""
    return messagebox.askyesno(title, message)

def create_circular_frame(parent, size, bg_color="#ffffff", border_color=None, border_width=0):
    """Create a circular frame for avatars"""
    frame = tk.Frame(parent, width=size, height=size, bg=border_color if border_color else bg_color)
    
    # Create a canvas for the circular shape
    canvas = tk.Canvas(frame, width=size, height=size, bg=parent['bg'], 
                     highlightthickness=0)
    canvas.pack()
    
    # Draw the circle
    offset = border_width if border_width > 0 else 0
    if border_width > 0 and border_color:
        canvas.create_oval(0, 0, size, size, fill=border_color, outline="")
    
    canvas.create_oval(offset, offset, size-offset, size-offset, fill=bg_color, outline="")
    
    return frame, canvas

def truncate_text(text, max_length=30):
    """Truncate text to a maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def extract_person_name(person_data):
    """Extract a person's name from different data formats"""
    if isinstance(person_data, dict) and 'name' in person_data:
        return person_data['name']
    if isinstance(person_data, str):
        # Attempt to parse JSON string
        try:
            data = json.loads(person_data)
            if isinstance(data, dict) and 'name' in data:
                return data['name']
        except (json.JSONDecodeError, TypeError):
            pass
    return str(person_data)

def parse_list_string(list_string):
    """Parse a string representation of a list into an actual list"""
    if not list_string or not isinstance(list_string, str):
        return []
        
    # Clean the string
    list_string = list_string.strip()
    if list_string.startswith('[') and list_string.endswith(']'):
        # Try using ast.literal_eval for safety
        try:
            return ast.literal_eval(list_string)
        except (SyntaxError, ValueError):
            pass
    
    # Fallback to simple string splitting
    return [item.strip() for item in list_string.split(',') if item.strip()]
