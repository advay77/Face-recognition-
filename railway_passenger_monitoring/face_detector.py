import os
import cv2
import face_recognition
from pymongo import MongoClient
from datetime import datetime

class FaceDetector:
    def __init__(self, known_faces_dir):
        """Initialize the face detector."""
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces(known_faces_dir)

        # Connect to MongoDB
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(mongo_uri)
        self.db = self.client["railway_monitoring"]
        self.collection = self.db["detections"]
        print(f"Connected to MongoDB: {self.db.name}.{self.collection.name}")

    def load_known_faces(self, known_faces_dir):
        """Load known faces from the specified directory."""
        print(f"Loading known faces from {known_faces_dir}...")
        for filename in os.listdir(known_faces_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(known_faces_dir, filename)
                try:
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)[0]
                    self.known_face_encodings.append(encoding)
                    self.known_face_names.append(os.path.splitext(filename)[0])
                    print(f"Loaded face: {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        print(f"Loaded {len(self.known_face_names)} known faces.")

    def save_detection(self, name, timestamp):
        """Save detection to MongoDB."""
        detection = {
            "name": name,
            "timestamp": timestamp,
        }
        self.collection.insert_one(detection)
        print(f"Saved detection: {detection}")

    def detect_and_recognize(self, frame):
        """Detect and recognize faces in the given frame."""
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the closest match
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = face_distances.argmin()
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

            face_names.append(name)

        # Scale face locations back to the original frame size
        scaled_face_locations = [(top * 4, right * 4, bottom * 4, left * 4) for (top, right, bottom, left) in face_locations]

        return scaled_face_locations, face_names

    def run(self, video_source):
        """Run the face detection system."""
        print("Starting video capture...")
        video_capture = cv2.VideoCapture(video_source)

        if not video_capture.isOpened():
            raise ValueError(f"Could not open video source {video_source}")

        print("Face detection system started. Press 'q' to quit.")
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to grab frame. Exiting...")
                break

            # Detect and recognize faces
            face_locations, face_names = self.detect_and_recognize(frame)

            # Annotate frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

                # Save detection to MongoDB
                if name != "Unknown":
                    self.save_detection(name, datetime.now())

            # Display the frame
            cv2.imshow("Railway Passenger Monitoring", frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting...")
                break

        video_capture.release()
        cv2.destroyAllWindows()