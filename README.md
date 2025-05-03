# 🏡 Aqar - Real Estate Backend (Django REST Framework)

This is the backend API for the **Aqar** real estate platform, built using Django and Django REST Framework.  
It handles user authentication, property listings (villas and apartments), facilities, and inquiries.

---

## 🔗 Frontend Repository  
[👉 Aqar Frontend GitHub Repo](https://github.com/huda-asaad/realestate_frontend)

---

## 🌐 Live Site  
[🌍 Deployed Site - Coming Soon](#)

---

## 🧠 Tech Stack

- Python 3
- Django 5
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Docker

---

## 🧩 Models

- **Property**: Represents a real estate listing (villa or apartment).
- **Facility**: Facilities related to each property (e.g., pool, garden).
- **Inquiry**: Inquiry submitted by a logged-in user regarding a property.

> 🚫 **User model does not count as one of the 3 required models.**

---


## 🔄 API Routing Table

| Method | Endpoint             | Description                    |
|--------|----------------------|--------------------------------|
| GET    | `/properties/`       | List all properties            |
| GET    | `/properties/<id>/`  | View specific property         |
| POST   | `/properties/`       | Create property (Admin only)   |
| PUT    | `/properties/<id>/`  | Update property (Admin only)   |
| DELETE | `/properties/<id>/`  | Delete property (Admin only)   |
| GET    | `/inquiries/`        | Admin view of all inquiries    |
| POST   | `/inquiries/`        | Submit inquiry (User only)     |
| POST   | `/login/`            | User login (JWT)               |
| POST   | `/signup/`           | User signup                    |
| POST   | `/logout/`           | Logout user                    |


---

## 🛠 Installation Instructions


## 📊 ERD Diagram

![ERD](./erd-diagram.png)


```bash
# Clone the backend repo
git clone https://github.com/huda-asaad/realestate_backend.git
cd realestate_backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the server
python manage.py runserver
