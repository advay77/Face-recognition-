import os
import cv2
import numpy as np
from datetime import datetime

def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def resize_frame(frame, scale=0.25):
    """Resize frame for faster processing."""
    return cv2.resize(frame, (0, 0), fx=scale, fy=scale)

def draw_face_box(frame, location, name, is_authorized=True):
    """
    Draw a box around a face with name label.
    
    Args:
        frame: Video frame
        location: (top, right, bottom, left) coordinates
        name: Name to display
        is_authorized: Whether the person is authorized
    """
    top, right, bottom, left = location
    
    # Set color based on authorization (green for authorized, red for unauthorized)
    color = (0, 255, 0) if is_authorized else (0, 0, 255)
    
    # Draw rectangle around face
    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
    
    # Draw filled rectangle for name background
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
    
    # Add name text
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)