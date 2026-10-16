# 💊 PharmaGuard – Pharmaceutical Management System

**PharmaGuard** is a web-based application developed using Python and Django to simplify pharmaceutical information management. The project aims to provide an organized, user-friendly platform for managing pharmaceutical data through a web interface.

## 🚀 Project Overview

Managing pharmaceutical information efficiently is important for maintaining accurate records and improving accessibility. PharmaGuard aims to address this need through a centralized web application with a structured backend and database.

This project was developed as a hands-on learning experience to apply Python Full Stack Development concepts, database management, and web application development.

## ✨ Features

- 🖥️ User-friendly web interface
- ⚙️ Backend development using Django
- 🗄️ Database integration with MySQL
- 📱 Responsive interface using Bootstrap
- 🔧 Organized application structure
- 🧪 Application testing and debugging

> Note: Update this feature list to match the functionality actually implemented in your project.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web application framework |
| MySQL | Database management |
| HTML5 | Webpage structure |
| CSS3 | Styling and layout |
| Bootstrap | Responsive user interface |
| Git & GitHub | Version control and source code management |

## 📂 Project Structure

```text
PharmaGuard/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── project_name/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── app_name/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

*The structure above is an example. Replace `project_name` and `app_name` with the actual folder names in your repository.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SandeepKoviri/PharmaGuard.git
```

```bash
cd PharmaGuard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

- Install and start MySQL.
- Create a database for PharmaGuard.
- Update the database settings in Django's `settings.py`.
- Configure credentials using environment variables where possible.

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open the local development server in your browser:

```text
http://127.0.0.1:8000/
```

## 🎯 Learning Outcomes

Through this project, I gained practical experience in:

- Developing web applications using Python and Django.
- Connecting a web application to a MySQL database.
- Understanding the Model-View-Template (MVT) architecture.
- Organizing application code into reusable components.
- Debugging, testing, and troubleshooting application errors.
- Using Git and GitHub for version control.

## 🔮 Future Improvements

- Enhance data validation and error handling.
- Improve authentication and authorization.
- Add additional pharmaceutical management features.
- Strengthen security and database optimization.
- Deploy the application to a cloud platform.

## 👨‍💻 Developer

**Sandeep Koviri**

Python Full Stack Developer | Python | Django | MySQL | Bootstrap

- GitHub: [SandeepKoviri](https://github.com/SandeepKoviri)

## 📄 License

This project is intended for educational and portfolio purposes. A formal open-source license can be added if the project is intended for public reuse.

---

⭐ If you find this project interesting, feel free to explore the repository and share feedback.
