# Face Recognition System

This repository contains code for a face recognition system with two main components:
- `face_detection_system`: A module for detecting faces in images or video streams.
- `railway_passenger_monitoring`: A system for monitoring railway passengers using face recognition.

## Features

- Face detection and recognition using machine learning models.
- Encryption utilities for secure data handling.
- Database integration for storing known faces and related data.
- Real-time monitoring and alerting capabilities.

## Project Structure

- `face_detection_system/`: Contains the face detection modules and related utilities.
- `railway_passenger_monitoring/`: Contains the main application code, including face detection, encryption, database, and monitoring logic.
- `requirements.txt`: Python dependencies for the project.
- `known_faces/`: Directory containing sample known face images.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/advay77/Face-recognition-.git
   cd Face-recognition-
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r railway_passenger_monitoring/requirements.txt
   ```

## Usage

Run the main application:
```bash
python railway_passenger_monitoring/main.py
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
