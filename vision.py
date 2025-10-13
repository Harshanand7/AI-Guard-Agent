import face_recognition
import cv2
import numpy as np
import os

class FaceRecognizer:
    def __init__(self, face_dir='data/faces'):
        self.known_face_encodings, self.known_face_names = self._load_known_faces(face_dir)
        print("Face Recognizer Initialized and Faces Enrolled")

    def _load_known_faces(self, known_faces_dir):
        encodings = []
        names = []
        print("Enrolling known faces")
        for person_name in os.listdir(known_faces_dir):
            person_dir = os.path.join(known_faces_dir, person_name)
            if not os.path.isdir(person_dir):
                continue
            for filename in os.listdir(person_dir):
                image_path = os.path.join(person_dir, filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings_list = face_recognition.face_encodings(image)
                if face_encodings_list:
                    encodings.append(face_encodings_list[0])
                    names.append(person_name)
                    print(f"Enrolled {person_name} from {filename}")
        return encodings, names

    def recognize_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        detected_names = []
        if not face_encodings:
            return []
        
        for face_encoding in face_encodings:
            name = "Unknown"

            if self.known_face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance = 0.6)
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            detected_names.append(name)

        print(detected_names)    

        return detected_names

# just for testing the module
if __name__ == "__main__":
    print("Testing the Face Recognizer Module")
    face_recognizer = FaceRecognizer()

    video_capture = cv2.VideoCapture(0)
    print("Starting video stream. Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break

        names = face_recognizer.recognize_faces(frame)
        if names:
            print("Detected faces:", names)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
