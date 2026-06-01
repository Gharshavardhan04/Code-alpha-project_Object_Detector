"""
Configuration file for the Object Detection and Tracking system
"""

# Model Configuration
MODEL_CONFIG = {
    'model_name': 'yolov8n.pt',  # Options: yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
    'conf_threshold': 0.5,  # Confidence threshold (0-1)
}

# Tracking Configuration
TRACKING_CONFIG = {
    'max_age': 30,  # Maximum frames to keep a track alive
    'min_hits': 3,  # Minimum detections to start a new track
    'iou_threshold': 0.3,  # IOU threshold for association
}

# Video Processing Configuration
VIDEO_CONFIG = {
    'display': True,  # Display video during processing
    'resize': True,  # Resize frames for faster processing
    'max_width': 1280,  # Maximum frame width when resizing
    'max_height': 720,  # Maximum frame height when resizing
}

# Visualization Configuration
VISUALIZATION_CONFIG = {
    'max_track_history': 30,  # Number of previous positions to show
    'line_thickness': 2,  # Bounding box line thickness
    'font_scale': 0.5,  # Font size for labels
}

# Input/Output Paths
PATHS = {
    'models_dir': 'models',
    'videos_dir': 'videos',
    'output_dir': 'output',
}

# Model Size Descriptions
MODEL_DESCRIPTIONS = {
    'yolov8n.pt': 'Nano - Fastest, lowest accuracy',
    'yolov8s.pt': 'Small - Fast, good balance',
    'yolov8m.pt': 'Medium - Slower, better accuracy',
    'yolov8l.pt': 'Large - Slow, high accuracy',
    'yolov8x.pt': 'XLarge - Slowest, highest accuracy',
}


def get_config():
    """Get complete configuration dictionary"""
    return {
        'model': MODEL_CONFIG,
        'tracking': TRACKING_CONFIG,
        'video': VIDEO_CONFIG,
        'visualization': VISUALIZATION_CONFIG,
        'paths': PATHS,
    }


def print_config():
    """Print current configuration"""
    config = get_config()
    
    print("\n" + "="*60)
    print("OBJECT DETECTION AND TRACKING CONFIGURATION")
    print("="*60)
    
    print("\nModel Configuration:")
    for key, value in config['model'].items():
        print(f"  {key}: {value}")
    
    print("\nTracking Configuration:")
    for key, value in config['tracking'].items():
        print(f"  {key}: {value}")
    
    print("\nVideo Processing Configuration:")
    for key, value in config['video'].items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60 + "\n")
