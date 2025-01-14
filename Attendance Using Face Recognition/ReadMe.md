                     Attendance System Using Face Recognition
This project is a Python-based attendance management system that uses facial recognition to mark attendance. It captures images via webcam, identifies registered faces, and maintains attendance records in an Excel file. Additionally, you can add new faces with associated details to the system.

Features
Face recognition using the face_recognition library.
Add new faces with details (e.g., name, roll number, course).
Mark attendance and store records in attendance.xlsx.
Store student details in student.xlsx.
User-friendly GUI created with Tkinter.
Requirements
Prerequisites
A functional webcam.
Python 3.7 or later.
Dependencies
Install the required Python libraries:

bash
Copy code
pip install -r requirements.txt
The requirements.txt includes:

opencv-python - For capturing and processing webcam images.
face-recognition - For facial recognition.
dlib - A prerequisite for face-recognition.
pandas - For working with Excel files.
openpyxl - To read and write Excel files.
tk - For GUI elements (typically pre-installed with Python).
Directory Structure
bash
Copy code
Attendance System/
│
├── main.py              # Main Python script
├── requirements.txt     # Dependencies
├── known_faces/         # Directory to store images of known faces
├── attendance.xlsx      # Excel file to store attendance records
└── student.xlsx         # Excel file to store student details
Setting Up the known_faces Directory
Create a folder named known_faces in the project directory.
Add images of known faces to this folder. Ensure the image filenames correspond to the names of the individuals (e.g., John_Doe.jpg).
Usage
Run the Program:

bash
Copy code
python main.py
Mark Attendance:

Click the Mark Attendance button.
The webcam will open. Press the spacebar to capture an image.
If the face matches a known individual, their attendance will be recorded in attendance.xlsx.
Add a New Face:

Click the Add Face button.
Capture the image of a new individual using the webcam.
Enter their details (name, roll number, course, etc.) in the form.
The image and details will be saved.
Excel Files:

attendance.xlsx contains attendance records.
student.xlsx stores details of registered students.
Troubleshooting
Common Issues
Face Not Recognized:

Ensure the known_faces directory contains clear images of the individual.
The captured image should be well-lit and face-oriented.
Permission Denied:

Close any open instances of attendance.xlsx or student.xlsx before running the program.
dlib Installation Errors:

Ensure C++ build tools are installed. Follow the dlib installation guide.
Future Improvements
Implement real-time face recognition for continuous attendance tracking.
Add support for multiple cameras.
Include a web-based interface for remote access.
