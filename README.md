![alx-logo](alx.jpeg)
# Hostel Management System (Flask) - Final Project for ALX Software Engineering Specialization (Backend)

The Hostel Management System is the final project for ALX Software Engineering Specialization (Backend). This project aims to demonstrate proficiency in various backend concepts and technologies, including authentication, session management, file management, and multiple storage engines. Below are the key features and objectives of the project:

## Project Objectives

1. **Basic Authentication**: Implement basic authentication mechanisms to secure access to the backend system. This involves validating user credentials (username and password) before allowing access to protected resources.

2. **Session Authentication**: Utilize session-based authentication to manage user sessions and maintain stateful interactions between clients and the backend. Sessions should be securely managed to prevent unauthorized access and tampering.

3. **User Authentication**: Develop authentication functionalities to verify the identity of users accessing the system. This includes features such as user registration, login, logout, password management, and user role-based access control.

4. **File Management**: Implement file management capabilities to allow users to upload, download, delete, and manage files within the system. Ensure secure handling of files and enforce access controls based on user permissions.

## Technologies and Tools

- **Backend Framework**: Flask
- **Authentication Mechanisms**: Custom login mechanisms, 
- **Session Management**: Flask-Session
- **File Management**: Flask-Uploads, Flask-File-Storage
- **Database Integration**: SQLAlchemy
- **Version Control**: Git

## Usage

1. **Authentication Setup**: Configure basic authentication mechanisms and session management using Flask-Login and Flask-Session. Implement user authentication endpoints for registration, login, and logout.

2. **File Management Implementation**: Develop endpoints and functionalities for handling file uploads, downloads, and deletions. Ensure proper validation and secure storage of files.

3. **Database Integration**:  SQLAlchemy for ORM operations and data manipulation.
## Database Structure

The project uses SQLAlchemy ORM and follows this database structure:
- `blocks`: Table storing information about blocks in the hostel.
- `rooms`: Table representing individual rooms with details such as block association, room type, and occupancy.
- `room_types`: Table storing information about different types of rooms available in the hostel.
- `staff`: Table representing staff members managing the hostel.
- `students`: Table storing information about students, including personal details and bookings.
- `bookings`: Table representing student bookings, including details such as room, check-in and check-out dates, and booking status.
- `payment`: Table storing payment details for student bookings.
- `reservation`: Table storing reservation details for student bookings.




## Features

- **Block Management**: Add, edit, or delete blocks within a campus.
- **Room Type Management**: Define different types of rooms available in the hostel.
- **Room Management**: Manage individual rooms, including details such as room names, capacities, and occupancy status.
- **Staff Management**: Maintain records of staff members managing the hostel.
- **Student Management**: Manage student information, including personal details and bookings.
- **Student Bookings**: Enable students to book hostel rooms through the system.
- **Student View Booking Details**: Allow students to view details of their hostel bookings.
- **Student Cancel Booking**: Provide students with the ability to cancel their bookings.

## Installation

To run the Hostel Management System locally, follow these steps:

1. Clone the repository:
   git clone https://github.com/Akwesi-bonah/alx_final_project
<br>
2. change directory
```
cd alx_final_project
```
3. Ubuntu dependence
```
sudo apt install pkg-config -y
sudo apt-get install libmysqlclient-dev -y
```
4. Create a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

5. Install dependencies:
```bash
   pip install -r requirements.txt
```

6. Set up the database and environment variable:
   - Modify [env.sh](env.sh) to configure your environment variables.
   - ```bash
        export HMS_ENV='dev'
        export HMS_MYSQL_USER='hms_dev'
        export HMS_MYSQL_PWD='hms_dev_pwd'
        export HMS_MYSQL_HOST='localhost'
        export HMS_MYSQL_DB='hms_dev_db'
        export HMS_TYPE_STORAGE='db'
     ```
   - Modify [setup_db.sq](setup_db.sql) to configure your database.
   - ```bash
     -- prepares a MySQL server for the project

        CREATE DATABASE IF NOT EXISTS hms_dev_db;
        CREATE USER IF NOT EXISTS 'hms_dev'@'localhost' IDENTIFIED BY 'hms_dev_pwd';
        GRANT ALL PRIVILEGES ON `hms_dev_db`.* TO 'hms_dev'@'localhost';
        GRANT SELECT ON `performance_schema`.* TO 'hms_dev'@'localhost';
        FLUSH PRIVILEGES;



7. 
   - Run migrations to create the database schema:
     ```bash
      sudo mysql -u root -p < setup_db.sql
     ```

8. Run this setup dummy data for login
```bash
 HMS_MYSQL_USER=hms_dev HMS_MYSQL_PWD=hms_dev_pwd HMS_MYSQL_HOST=localhost HMS_MYSQL_DB=hms_dev_db HMS_TYPE_STORAGE=db python3 -m test
````

## Usage

To start the api run:
```bash
 HMS_MYSQL_USER=hms_dev HMS_MYSQL_PWD=hms_dev_pwd HMS_MYSQL_HOST=localhost HMS_MYSQL_DB=hms_dev_db HMS_TYPE_STORAGE=db AUTH_TYPE=basic_auth python3 -m api.v1.app

```

To start the web app run:
```bash
HMS_MYSQL_USER=hms_dev HMS_MYSQL_PWD=hms_dev_pwd HMS_MYSQL_HOST=localhost HMS_MYSQL_DB=hms_dev_db HMS_TYPE_STORAGE=db python3 -m web_flask.main

```
# Credentials
```
user_email = "user@gmail.com"
clear_user_pwd = "pwd"
```
staff
Access the application at `http://localhost:5000` in your web browser.

Student view of the application is available at `http://localhost:500/student/login`.

Staff view of the application is available at `http://localhost:5000/staff/login`.


## Contributing

Contributions are welcome! If you want to contribute to this project, please fork the repository and create a pull request.
- [George Arhin-Bonnah](https://github.com/Akwesi-bonah)
- [Godwin Dogbey](https://github.com/GodwinDogbey )
## Contact

For any inquiries or support regarding the Hostel Management System (Flask) project, please contact [George](arhinbonnah@gmail.com).