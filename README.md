Secure File Sharing System
A Python Flask application to securely share files between Ops Users and Client Users, ensuring role-based access and secure file handling.

API Endpoints
Ops User Actions:-

Login (/ops/login):
Authenticates Ops Users to enable file uploads.

Upload File (/ops/upload):
Allows only Ops Users to upload .pptx, .docx, and .xlsx files.

Client User Actions:-

Sign Up (/client/signup):
Registers a Client User and generates an encrypted file access URL.

Email Verify (/client/verify):
Verifies a Client User's email for account activation.

Login (/client/login):
Authenticates Client Users for accessing files.

List Files (/client/files):
Displays all uploaded files for Client Users.

Download File (/client/download/<encrypted_url>):
Provides secure file access via an encrypted URL.

Security Features:-
Encrypted URLs: Restrict file access to authenticated Client Users.
Role-Based Access: Limits Ops Users to uploads and Client Users to downloads.
Email Verification: Ensures only verified users access the system.

Setup Instructions:-
Start the Flask server:
python index.py

Use the above endpoints to interact with the system.
