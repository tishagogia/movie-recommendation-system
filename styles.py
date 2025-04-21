"""
Style definitions for the Movie Recommendation System
"""

# Color scheme
PRIMARY_COLOR = "#2c3e50"  # Dark blue/slate
SECONDARY_COLOR = "#3498db"  # Bright blue
ACCENT_COLOR = "#e74c3c"  # Red
SUCCESS_COLOR = "#2ecc71"  # Green
WARNING_COLOR = "#f39c12"  # Orange
ERROR_COLOR = "#c0392b"  # Dark red
INFO_COLOR = "#9b59b6"  # Purple

# Background and text colors
BG_COLOR = "#ecf0f1"  # Light gray
BG_COLOR_DARK = "#bdc3c7"  # Darker gray
TEXT_COLOR = "#2c3e50"  # Dark blue/slate
TEXT_COLOR_LIGHT = "#7f8c8d"  # Medium gray
TEXT_COLOR_INVERSE = "#ffffff"  # White

# Font styles
FONT_FAMILY = "Helvetica"
FONT_SIZE_SMALL = 10
FONT_SIZE_MEDIUM = 12
FONT_SIZE_LARGE = 14
FONT_SIZE_EXTRA_LARGE = 18
FONT_SIZE_TITLE = 24

# Padding and spacing
PADDING_TINY = 2
PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 20
PADDING_EXTRA_LARGE = 30

# Border styles
BORDER_WIDTH = 1
BORDER_COLOR = "#bdc3c7"
BORDER_RADIUS = 5  # Note: Tkinter doesn't support border radius directly

# Button styles
BUTTON_PADDING = (10, 5)
BUTTON_SMALL_PADDING = (5, 2)
BUTTON_LARGE_PADDING = (15, 8)

# Input field styles
INPUT_PADDING = 5
INPUT_HEIGHT = 25
INPUT_BORDER_COLOR = "#bdc3c7"
INPUT_FOCUS_BORDER_COLOR = "#3498db"

# Card styles
CARD_BG_COLOR = "#ffffff"
CARD_BORDER_COLOR = "#bdc3c7"
CARD_SHADOW_COLOR = "#95a5a6"
CARD_PADDING = 10
CARD_MARGIN = 10

# Animation timing (milliseconds)
ANIMATION_FAST = 150
ANIMATION_MEDIUM = 300
ANIMATION_SLOW = 500

# Define ttk style configurations
TTK_STYLE = {
    "TButton": {
        "configure": {
            "background": SECONDARY_COLOR,
            "foreground": TEXT_COLOR_INVERSE,
            "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
            "padding": BUTTON_PADDING,
            "relief": "flat"
        },
        "map": {
            "background": [("active", PRIMARY_COLOR), ("disabled", BG_COLOR_DARK)],
            "foreground": [("disabled", TEXT_COLOR_LIGHT)]
        }
    },
    "TEntry": {
        "configure": {
            "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
            "padding": INPUT_PADDING,
            "fieldbackground": "#ffffff"
        }
    },
    "TFrame": {
        "configure": {
            "background": BG_COLOR
        }
    },
    "TLabel": {
        "configure": {
            "background": BG_COLOR,
            "foreground": TEXT_COLOR,
            "font": (FONT_FAMILY, FONT_SIZE_MEDIUM)
        }
    },
    "TCheckbutton": {
        "configure": {
            "background": BG_COLOR,
            "foreground": TEXT_COLOR,
            "font": (FONT_FAMILY, FONT_SIZE_MEDIUM)
        }
    },
    "TRadiobutton": {
        "configure": {
            "background": BG_COLOR,
            "foreground": TEXT_COLOR,
            "font": (FONT_FAMILY, FONT_SIZE_MEDIUM)
        }
    }
}

# Widget-specific styles
HEADER_STYLE = {
    "bg": PRIMARY_COLOR,
    "fg": TEXT_COLOR_INVERSE,
    "font": (FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
    "pady": PADDING_MEDIUM,
    "padx": PADDING_LARGE
}

SUBHEADER_STYLE = {
    "bg": BG_COLOR,
    "fg": PRIMARY_COLOR,
    "font": (FONT_FAMILY, FONT_SIZE_EXTRA_LARGE, "bold"),
    "pady": PADDING_SMALL,
    "padx": PADDING_MEDIUM
}

LABEL_STYLE = {
    "bg": BG_COLOR,
    "fg": TEXT_COLOR,
    "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
    "pady": PADDING_SMALL
}

BUTTON_STYLE = {
    "bg": SECONDARY_COLOR,
    "fg": TEXT_COLOR_INVERSE,
    "activebackground": PRIMARY_COLOR,
    "activeforeground": TEXT_COLOR_INVERSE,
    "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
    "padx": BUTTON_PADDING[0],
    "pady": BUTTON_PADDING[1],
    "bd": 0
}

ACCENT_BUTTON_STYLE = {
    "bg": ACCENT_COLOR,
    "fg": TEXT_COLOR_INVERSE,
    "activebackground": ERROR_COLOR,
    "activeforeground": TEXT_COLOR_INVERSE,
    "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
    "padx": BUTTON_PADDING[0],
    "pady": BUTTON_PADDING[1],
    "bd": 0
}

SUCCESS_BUTTON_STYLE = {
    "bg": SUCCESS_COLOR,
    "fg": TEXT_COLOR_INVERSE,
    "activebackground": "#27ae60",
    "activeforeground": TEXT_COLOR_INVERSE,
    "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
    "padx": BUTTON_PADDING[0],
    "pady": BUTTON_PADDING[1],
    "bd": 0
}

ENTRY_STYLE = {
    "font": (FONT_FAMILY, FONT_SIZE_MEDIUM),
    "bd": 1,
    "relief": "solid",
    "highlightthickness": 1,
    "highlightcolor": SECONDARY_COLOR
}

# Function to apply ttk styles
def apply_styles(style):
    """Apply the defined styles to a ttk.Style object"""
    for name, settings in TTK_STYLE.items():
        if "configure" in settings:
            style.configure(name, **settings["configure"])
        if "map" in settings:
            style.map(name, **settings["map"])
