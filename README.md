# Django & Keycloak SSO Integration

A robust, secure, and production-ready Single Sign-On (SSO) integration using **Django** and **Keycloak** (OpenID Connect). This project was designed and implemented following an Agile/Scrum roadmap across multiple sprints.

---

## Project Roadmap

This project was developed following a structured 5-stage event path:

1. **Setup**: Initialize the development environment, virtual env, and database.
2. **Identity**: Configure Keycloak (IdP), realms, clients, and protocols (OIDC).
3. **Users**: Design user models and establish secure communication between Django and Keycloak.
4. **Integration**: Set up user attribute mapping (e.g., `phone_number`), role mapping (Admin/Staff), and automated profile synchronization.
5. **Deployment**: Establish session management, secure SSO logouts, and production-ready configurations.

---

## Prerequisites

Before running this project, ensure you have the following installed on your system:

* **Python** (3.10 or higher)
* **Java JDK** (17 or higher - *Required to run Keycloak locally*)
* **Keycloak** (Latest stable release)

---

## Step-by-Step Setup Guide

Follow these steps to set up and run the project locally.

### Step 1: Set Up Keycloak (Identity Provider)

1. **Install Java**: Ensure Java is installed and added to your system's PATH.

```bash
   java -version
   
Download & Start Keycloak:
Download Keycloak from official website.
Extract the ZIP file, navigate to the bin directory, and run:
bash
# On Linux/macOS:
./kc.sh start-dev
# On Windows (cmd):
kc.bat start-dev

Configure Keycloak Admin:
Open http://localhost:8080 in your browser and create your Admin credentials.
Configure Realm & Client:
Create a new Realm (e.g., my-realm).
Create a Client (e.g., django-client) with Client Protocol set to openid-connect.
Set Valid Redirect URIs to http://127.0.0.1:8000/* (or your Django local port).
In Client Scopes, add a User Attribute Mapper for phone_number to ensure it is sent within the ID Token.
(Optional) Add a custom Regex Validator (^98\d{10}$) for the phone_number user attribute in Keycloak.
####  Step 2: Set Up Django (Backend)
1. ** Clone the Repository**:
bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   
Create a Virtual Environment:
bash
   python -m venv venv
   # Activate on Windows:
   venv\Scripts\activate
   # Activate on macOS/Linux:
   source venv/bin/activate
   
Install Dependencies:
bash
   pip install -r requirements.txt
   
Environment Variables:Create a .env file in the root directory (or update settings.py) with your Keycloak credentials:
env
   KEYCLOAK_SERVER_URL=http://localhost:8080
   KEYCLOAK_REALM=my-realm
   KEYCLOAK_CLIENT_ID=django-client
   KEYCLOAK_CLIENT_SECRET=your-client-secret
   
Run Migrations:
bash
   python manage.py makemigrations
   python manage.py migrate
   
Start the Django Server:
bash
   python manage.py runserver
   
 Key Features Implemented
Single Sign-On (SSO): Users authenticate securely via Keycloak without ever exposing passwords to the Django app.
Auto-Profile Synchronization (sync_profile): Automatically fetches custom attributes like phone_number from the Keycloak Token and updates the Django local database upon login.
Role Mapping: Dynamically maps Keycloak Roles to Django is_staff and is_superuser privileges.
SSO Logout: Fully terminates both the local Django session and the Keycloak SSO session via standardized OIDC logout.
 Project Structure Highlights
auth_backends.py: Implements custom OIDC backend to handle authentication, role mapping, and sync_profile.
models.py: Custom User Profile extension supporting a CharField(max_length=15) to prevent truncation of international phone numbers.
text
