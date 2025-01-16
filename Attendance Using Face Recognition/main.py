import cv2
import face_recognition
import pandas as pd
from datetime import datetime
import os
import zipfile
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox


# Directory containing known face images
# known_faces_dir = r'C:\\Users\\rm710\\OneDrive\\Desktop\\Attendance Using Face Recognition\\known_faces'

import os

known_faces_dir = r'C:\\Users\\rm710\\OneDrive\\Desktop\\Attendance Using Face Recognition\\known_faces'

# Ensure the directory exists
if not os.path.exists(known_faces_dir):
    os.makedirs(known_faces_dir)
    print(f"Created directory: {known_faces_dir}")
else:
    print(f"Directory already exists: {known_faces_dir}")

# Load known faces
def load_known_faces():
    global known_faces, known_names
    known_faces = []
    known_names = []
    
    if not os.path.isdir(known_faces_dir):
        print(f"Error: Directory does not exist: {known_faces_dir}")
        return
    
    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image = face_recognition.load_image_file(f"{known_faces_dir}\\{filename}")
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces.append(encodings[0])
                known_names.append(filename.split('.')[0])

load_known_faces()


# Function to capture image
# def capture_image():
#     cam = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cam.read()
#         if not ret:
#             print("Failed to grab frame")
#             break
#         cv2.imshow('Press Space to capture', frame)
#         if cv2.waitKey(1) & 0xFF == ord(' '):
#             break
#     cam.release()
#     cv2.destroyAllWindows()
#     return frame if ret else None

# Function to capture image automatically when a face is detected
def capture_image():
    cam = cv2.VideoCapture(0)
    face_detected = False
    captured_frame = None

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert frame to RGB for face_recognition compatibility
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Check for face(s) in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        # If a face is detected, save the frame and break
        if face_locations:
            face_detected = True
            captured_frame = frame
            cv2.putText(frame, "Face Detected. Capturing...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Face Detection', frame)
            cv2.waitKey(1000)  # Pause for a moment to show detection message
            break

        # Display the video feed with no detection message
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

    if face_detected:
        return captured_frame
    else:
        print("No face detected.")
        return None


# Function to recognize face
def recognize_face(captured_image):
    face_encodings = face_recognition.face_encodings(captured_image)
    if len(face_encodings) == 0:
        print("No faces detected in the image.")
        return None
    captured_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(known_faces, captured_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        return known_names[first_match_index]
    return None

# Function to mark attendance
def mark_attendance(student_name, file='attendance.xlsx'):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    try:
        df = pd.read_excel(file, engine='openpyxl')
    except (FileNotFoundError, zipfile.BadZipFile):
        df = pd.DataFrame(columns=["Name", "Date", "Time"])
    
    # Check if the student has already marked attendance for today
    if not df[(df['Name'] == student_name) & (df['Date'] == current_date)].empty:
        messagebox.showinfo("Info", f"Attendance already marked for {student_name}")
        return
    
    new_record_df = pd.DataFrame({"Name": [student_name], "Date": [current_date], "Time": [current_time]})
    df = pd.concat([df, new_record_df], ignore_index=True)
    df.to_excel(file, index=False)
    messagebox.showinfo("Success", f"Attendance marked for {student_name}")

# Function to handle the capture and recognition process
def handle_capture():
    image = capture_image()
    if image is None:
        messagebox.showerror("Error", "Failed to capture image.")
        return
    student_name = recognize_face(image)
    if student_name is None:
        messagebox.showerror("Error", "Student not recognized!")
        return
    mark_attendance(student_name)

# Function to add a new face
def add_face():
    image = capture_image()
    if image is None:
        messagebox.showerror("Error", "Failed to capture image.")
        return
    
    # Validate that the captured image contains a human face
    face_encodings = face_recognition.face_encodings(image)
    if len(face_encodings) == 0:
        messagebox.showerror("Error", "No human face detected in the image.")
        return
    
    def save_face():
        name = name_entry.get()
        roll_number = roll_number_entry.get()
        course = course_entry.get()
        branch = branch_entry.get()
        year = year_entry.get()
        
        if not name or not roll_number or not course or not branch or not year:
            messagebox.showerror("Error", "All fields are required.")
            return
        
        # Save the captured image with the name only
        file_path = os.path.join(known_faces_dir, f"{name}.jpg")
        cv2.imwrite(file_path, image)
        load_known_faces()
        
        # Save the student details in the Excel file
        student_file = 'student.xlsx'
        try:
            student_df = pd.read_excel(student_file, engine='openpyxl')
        except (FileNotFoundError, zipfile.BadZipFile):
            student_df = pd.DataFrame(columns=["Name", "Roll Number", "Course", "Branch", "Year"])
        
        new_student_df = pd.DataFrame({"Name": [name], "Roll Number": [roll_number], "Course": [course], "Branch": [branch], "Year": [year]})
        student_df = pd.concat([student_df, new_student_df], ignore_index=True)
        
        try:
            student_df.to_excel(student_file, index=False)
        except PermissionError:
            messagebox.showerror("Error", f"Permission denied: '{student_file}'. Please close the file if it is open and try again.")
            return
        
        messagebox.showinfo("Success", f"Face and details added for {name}")
        add_face_window.destroy()
    
    add_face_window = tk.Toplevel(root)
    add_face_window.title("Add New Face")
    add_face_window.geometry("400x400")
    
    ttk.Label(add_face_window, text="Name:").pack(pady=5)
    name_entry = ttk.Entry(add_face_window)
    name_entry.pack(pady=5)
    
    ttk.Label(add_face_window, text="Roll Number:").pack(pady=5)
    roll_number_entry = ttk.Entry(add_face_window)
    roll_number_entry.pack(pady=5)
    
    ttk.Label(add_face_window, text="Course:").pack(pady=5)
    course_entry = ttk.Entry(add_face_window)
    course_entry.pack(pady=5)
    
    ttk.Label(add_face_window, text="Branch:").pack(pady=5)
    branch_entry = ttk.Entry(add_face_window)
    branch_entry.pack(pady=5)
    
    ttk.Label(add_face_window, text="Year:").pack(pady=5)
    year_entry = ttk.Entry(add_face_window)
    year_entry.pack(pady=5)
    
    ttk.Button(add_face_window, text="Submit", command=save_face).pack(pady=5)
    ttk.Label(add_face_window, text="Click 'Submit' to save the details:").pack(pady=5)

# Create the GUI
root = tk.Tk()
root.title("Attendance System")
root.geometry("600x500")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 14))

frame = ttk.Frame(root, padding="20")
frame.pack(fill=tk.BOTH, expand=True)

label = ttk.Label(frame, text="Attendance System", anchor="center")
label.pack(pady=10)

capture_button = ttk.Button(frame, text="Mark Attendance", command=handle_capture)
capture_button.pack(pady=10)

add_face_button = ttk.Button(frame, text="Add Face", command=add_face)
add_face_button.pack(pady=10)

root.mainloop()