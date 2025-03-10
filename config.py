import os
from typing import Dict, List, Any, Optional


# Wheel configuration
class WheelConfig:
    # Names file path
    NAMES_FILE: str = os.environ.get('WHEEL_NAMES_FILE', 'options.txt')
    
    # Spin animation settings
    MIN_ROTATIONS: float = float(os.environ.get('WHEEL_MIN_ROTATIONS', '5'))
    MAX_ROTATIONS: float = float(os.environ.get('WHEEL_MAX_ROTATIONS', '8'))
    SPIN_DURATION: float = float(os.environ.get('WHEEL_SPIN_DURATION', '10.0'))
    DECELERATION: float = float(os.environ.get('WHEEL_DECELERATION', '3'))
    
    # Animation frame rate and speeds
    IDLE_ROTATION_SPEED: float = float(os.environ.get('WHEEL_IDLE_SPEED', '5'))
    FRAME_RATE: int = int(os.environ.get('WHEEL_FRAME_RATE', '60'))
    MAX_SPEED: float = float(os.environ.get('WHEEL_MAX_SPEED', '30'))
    
    # Color modes
    COLOR_MODE: str = os.environ.get('WHEEL_COLOR_MODE', 'RGB')  # RGB or CUSTOM
    
    # Custom color palette when COLOR_MODE is CUSTOM (comma-separated hex values)
    custom_colors_env = os.environ.get('WHEEL_CUSTOM_COLORS', '#4285F4,#EA4335,#FBBC05,#34A853')
    CUSTOM_COLORS: List[str] = custom_colors_env.split(',')
    
    # Wheel appearance
    TEXT_DISTANCE_FACTOR: float = float(os.environ.get('WHEEL_TEXT_DISTANCE', '0.9'))  # 0-1, 1 being edge
    SLICE_STROKE_COLOR: str = os.environ.get('WHEEL_SLICE_STROKE', 'white')
    SLICE_STROKE_WIDTH: float = float(os.environ.get('WHEEL_SLICE_STROKE_WIDTH', '0.5'))
    
    # Marker
    MARKER_COLOR: str = os.environ.get('WHEEL_MARKER_COLOR', 'red')
    MARKER_ICON: str = os.environ.get('WHEEL_MARKER_ICON', 'arrow_circle_right')
    MARKER_SIZE: str = os.environ.get('WHEEL_MARKER_SIZE', 'xl')
    
    # Text styling
    TEXT_COLOR: str = os.environ.get('WHEEL_TEXT_COLOR', 'black')
    TEXT_SIZE: float = float(os.environ.get('WHEEL_TEXT_SIZE', '3.5'))  # SVG font size
    TEXT_WEIGHT: str = os.environ.get('WHEEL_TEXT_WEIGHT', 'bold')


# Server configuration
class ServerConfig:
    PORT: int = int(os.environ.get('WHEEL_PORT', '8080'))
    TITLE: str = os.environ.get('WHEEL_TITLE', 'Name Spinner')


# Combine all configs
config: Dict[str, Any] = {
    'wheel': WheelConfig(),
    'server': ServerConfig(),
}