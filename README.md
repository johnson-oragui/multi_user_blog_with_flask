
# Multi-User Blog Application

# Overview

The Multi-User Blog Application is a web-based platform where users can register, create, read, update, and delete blog posts. Each user can manage their own blogs and comments, while admins can manage users and their content. The application also supports archiving of users and their associated data before deletion, ensuring data integrity and compliance.

# Features

- User Registration and Authentication
- Create, Read, Update, and Delete (CRUD) operations for Blogs
- Comment on Blogs
- Admin User Management
- Archiving of Users, Blogs, and Comments before deletion
- Flask Blueprints for modular code organization
- SQLAlchemy for database interactions
- Foreign Key constraints to maintain data integrity

# Setup Instructions

# Prerequisites

- Python 3.10 or higher
- MySQL
- Virtual Environment (optional but recommended)

# Installation

1. # Clone the repository
  
   git clone https://github.com/yourusername/multi-user-blog-application.git
   cd multi-user-blog-application


2. # Create and activate a virtual environment:

   python3 -m venv myvenv
   source myvenv/bin/activate  # On Windows use `myvenv\Scripts\activate`


3. # Install the dependencies:

   pip install -r requirements.txt


4. # Set up the MySQL database:
   - Create a MySQL database named `multi_user_blog`.
   - Update the database configuration in `config.py`:
  python
     SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@localhost/multi_user_blog'


# Running the Application

1. Start the Flask development server:

   python3 -m app


2. Open your web browser and navigate to:

   http://127.0.0.1:5000/


# Project Structure


multi-user-blog-application/
│
├── 
│   ├── __init__.py
│___models/
│      ├── __init__.py
│      ├── base_model.py
│      ├── blog.py
│      ├── comment.py
│      ├── user.py
│      ├── archived_blog.py
│      ├── archived_comment.py
│      ├── archived_user.py
│      └── db_engine
|          |_______ db_storage.py
│___ templates/
│      ├── base.html
│      ├── index.html
│      ├── dashboard.html
│      └── delete_user.html
│____ static/
│      ├── css/
│      └── js/
│_____ views/
│      ├── __init__.py
│      ├── auth.py
│      ├── dashboard.py
│      └── users.py
│      └── config.py
├── tests/
│   └── test_app.py
|   |__ test_models
|       |__________
|       |__________test_db_engine
|                  |________ test_db_storage.py
├── .myvenv
├── README.md
├── requirements.txt
└── app.py


# Usage

# User Registration and Authentication

- Users can register by providing their first name, last name, username, email, and password.
- Users can log in using their email or username and password.

# Creating and Managing Blogs

- Authenticated users can create new blog posts.
- Users can view, update, and delete their own blog posts.
- Users can comment on blog posts.

# Admin User Management

- Admins can view the list of users.
- Admins can delete users, triggering the archival process.

### Archiving

- When a user is deleted, their data (blogs and comments) is archived before deletion.
- The `before_delete` event listener in SQLAlchemy handles the archiving process.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

---

# AUTHOR:

Johnson Oragui <johnson.oragui@gmail.com>
