# 🗨️ Django Chat Application

![Django](https://img.shields.io/badge/Django-5.1.6-green.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![HTMX](https://img.shields.io/badge/HTMX-Enabled-orange.svg)

A **real-time chat application** built with **Django, HTMX, and WebSockets**, supporting **public and private chatrooms** with file sharing capabilities. 📩

---

## 🌟 Features

✅ **User Authentication** (Login, Registration, Email Verification)
✅ **Real-Time Messaging** with WebSockets
✅ **Public & Private Chatrooms**
✅ **File Upload Support** (Images, Documents)
✅ **HTMX for Smooth UX**
✅ **Admin Dashboard for Chatroom Management**
✅ **Secure with CSRF & Authentication Middleware**

---

## 📌 Installation Guide

### 1️⃣ Clone the Repository
```sh
$ git clone https://github.com/mehdidinari/chat-app.git
$ cd chat-app
```

### 2️⃣ Create a Virtual Environment
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
$ pip install -r requirements.txt
```

### 4️⃣ Apply Migrations
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### 5️⃣ Create a Superuser (For Admin Panel)
```sh
$ python manage.py createsuperuser
```

### 6️⃣ Run the Development Server
```sh
$ python manage.py runserver
```
🔗 Visit: `http://127.0.0.1:8000/`

---

## 🖥️ Tech Stack

- **Django 5.1.6** (Backend)
- **HTMX** (Lightweight frontend interactivity)
- **Channels** (WebSockets for real-time communication)
- **SQLite / PostgreSQL** (Database support)
- **Bootstrap / Tailwind CSS** (Styling)

---

## 🚀 How to Use

### 💬 Chatrooms
1. Login/Register to access the chatrooms.
2. Create a new **public or private** chatroom.
3. Start **real-time conversations**.

### 📂 File Uploads
- Upload images and documents directly in the chat.
- Shared files appear within the chat conversation.

### 🔧 Admin Panel
- Manage chatrooms & users: `http://127.0.0.1:8000/admin/`

---

## 🛠️ Contributing

Want to contribute? Follow these steps:
1. Fork the repository 🚀
2. Create a new branch: `git checkout -b feature-branch`
3. Make your changes & commit: `git commit -m 'Added a new feature'`
4. Push to your fork: `git push origin feature-branch`
5. Open a **Pull Request** 🎉

---

## 📜 License
This project is licensed under the **MIT License**. Feel free to modify and use it.

---

## 🌎 Connect with Me
🔹 GitHub: [@yourusername](https://github.com/mehdidinari)  
🔹 LinkedIn: [Your LinkedIn](https://www.linkedin.com/in/mehdi-dinari-b0487a2a9/)  


