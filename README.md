# Integrated Hospital Management System (IHMS)

## Overview
The **Integrated Hospital Management System (IHMS)** is a web-based platform built using Django that enables efficient management of multiple hospitals under one system. It allows users to register, book appointments, order medicines, request lab tests, and manage hospital operations seamlessly.

## Features
### For Patients:
- View available hospitals, doctors, laboratories, and pharmacies.
- Register and create a patient profile.
- Book and cancel doctor appointments.
- Order medicines from pharmacies.
- Request sample collection for lab tests.
- View test reports online.

### For Hospital Owners:
- Register their hospital in the system.
- Manage doctors, pharmacy, and laboratories.
- Assign and manage appointments.

### For Doctors:
- Register and create a profile.
- View and manage patient appointments.
- Upload patient test reports.

### For Riders:
- Accept and deliver medicine orders.
- Pick up and submit lab samples.

### For Admin:
- Manage all users, hospitals, and medical services.
- Assign riders for sample collection and medicine deliveries.

## Tech Stack
- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Django authentication system

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/IHMS.git
   ```
2. Navigate to the project directory:
   ```bash
   cd IHMS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Open your browser and visit:
   ```
   http://127.0.0.1:8000/
   ```

## Usage
1. **Sign up or log in** to access features.
2. **Explore available hospitals, doctors, labs, and pharmacies.**
3. **Book appointments, order medicines, or request lab tests.**
4. **Admin can manage users, hospitals, and system-wide operations.**

## Future Enhancements
- Implementing **payment gateway integration** for online payments.
- Adding **real-time notifications** for appointment reminders and order tracking.
- Expanding **user roles and permissions** for better access control.

