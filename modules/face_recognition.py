import face_recognition
from PIL import Image, ImageDraw

def detect_faces(image_path):  # ✅ Fix: Correct function name
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return "No faces detected."

    return f"{len(face_locations)} face(s) detected."
