import os
import cv2
import time
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from face_detector import FaceDetector
from database import MongoDBHandler
from encryption import EncryptionHandler

def main():
    # Load environment variables
    load_dotenv()
    video_source = os.getenv("VIDEO_SOURCE", 0)  # Default to webcam if not specified
    
    # Initialize components
    face_detector = FaceDetector(known_faces_dir="known_faces")
    encryption_handler = EncryptionHandler()
    db_handler = MongoDBHandler()
    
    # Initialize video capture
    if video_source.isdigit():
        video_source = int(video_source)
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    print("Face detection system started. Press 'q' to quit.")
    
    try:
        while True:
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            
            # Detect and recognize faces
            face_locations, face_names = face_detector.detect_and_recognize(frame)
            
            # Process each detected face
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Determine if authorized
                is_authorized = name != "Unknown"
                
                # Set rectangle color based on authorization
                color = (0, 255, 0) if is_authorized else (0, 0, 255)
                
                # Draw rectangle and name
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
                
                # Create detection event
                timestamp = datetime.now().isoformat()
                event = {
                    "name": name,
                    "status": "authorized" if is_authorized else "unauthorized",
                    "timestamp": timestamp
                }
                
                # Encrypt and store event
                encrypted_event = encryption_handler.encrypt_data(event)
                db_handler.store_detection(encrypted_event)
                
                # Log unknown passengers separately (bonus requirement)
                if not is_authorized:
                    print(f"Unknown passenger detected at {timestamp}")
            
            # Display the frame
            cv2.imshow('Railway Passenger Monitoring System', frame)
            
            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
        db_handler.close()

if __name__ == "__main__":
    main()