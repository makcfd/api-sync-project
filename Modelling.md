1. DB schema.

- User:

Attributes: UserID, Name, Email, Password, AccountType (e.g., 'small package'), Credits
Relationships: related many Patients

- Patient:

Attributes: PatientID, FullName, DateOfBirth, Height, Weight, Indication, Complaints, ComplaintIntensity, Comments
Relationships: related to User, related to many Videos

- Video:

Attributes: VideoID, Timestamp, FilePath, AnalysisStatus (e.g., 'in progress', 'completed', 'failed', etc)
Relationships: related to Patient, related to many AnalysisResult

- AnalysisResults:

Attributes: WalkingSpeed, GaitSymmetry, StepCount, DoubleSupport, Type, Version
Relationships: many AnalysisResults related to one Video


2. Required API Endpoints.
Potential API endpoints needed for the app, along with brief descriptions:

- User Management:
POST /users/register - Register a new user.
POST /users/login - Authenticate a user and start a session.
GET /users/{userID} - Retrieve user details.
PUT /users/{userID} - Update user details.

- Patient Management:
POST /patients - Create a new patient record.
GET /patients/{patientID} - Retrieve patient details.
PUT /patients/{patientID} - Update patient details.
GET /users/{userID}/patients - List all patients for a user.

- Video Management:
POST /{patientID}/videos - Submit a video for analysis.
GET /{patientID}/videos/{videoID} - Retrieve video details.
PUT /{patientID}/videos/{videoID} - Update video details (e.g., after analysis).

- Analysis Management:
GET /analysis/{patientID}/{videoID} - Retrieve analysis results for a video.
