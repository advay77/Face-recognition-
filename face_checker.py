import cv2
import face_recognition
import os

# Load known faces from the folder
def load_known_faces(folder_path):
    known_encodings = []
    known_names = []
    known_encodings, known_names = load_known_faces("auth_faces")
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
            else:
                print(f"[WARNING] No face found in {filename}")
    return known_encodings, known_names

# Initialize webcam and known faces
known_encodings, known_names = load_known_faces("authorized_faces")
video_capture = cv2.VideoCapture(0)

print("[INFO] Scanning started. Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("[ERROR] Unable to access camera.")
        break

    # Resize for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Detect face locations and encodings
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unauthorized"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]

        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        color = (0, 255, 0) if name != "Unauthorized" else (0, 0, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)

    cv2.imshow("Face Authorization System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
