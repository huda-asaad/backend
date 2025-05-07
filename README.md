# 🏡 Aqar - Real Estate Backend (Django REST Framework)

This is the backend API for the **Aqar** real estate platform, built using Django and Django REST Framework.  
It handles user authentication, property listings (villas and apartments), facilities, and inquiries.

---

## 🔗 Frontend Repository  
[👉 Aqar Frontend GitHub Repo](https://github.com/huda-asaad/realestate_frontend)

---

## 🌐 Live Site  
[🌍 (http://localhost:5173/)](#)

---

## 🧠 Tech Stack

- Python 
- Django 
- PostgreSQL
- JWT Authentication
- Docker

---

## 🧩 Models

- **Property**: Represents a real estate listing (villa or apartment).
- **Amenity**: Facilities related to each property (e.g., pool, garden).
- **Inquiry**: Inquiry submitted by a logged-in user regarding a property.


---

## 🔄 API Routing Table

## 🔄 API Routing Table

| Method | Endpoint             | Description                              |
|--------|----------------------|------------------------------------------|
| GET    | `/properties/`       | List all properties                      |
| GET    | `/properties/<id>/`  | View specific property                   |
| POST   | `/properties/<id>/`  | Create property                          |
| PUT    | `/properties/<id>/`  | Update property                          |
| DELETE | `/properties/<id>/`  | Delete property                          |
| GET    | `/inquiries/`        | View all submitted inquiries (admin only)|
| POST   | `/login/`            | User login (JWT)                         |
| POST   | `/signup/`           | User signup                              |
| POST   | `/logout/`           | Logout user                              |

---

## 👩🏻‍💻 IceBox Features
- Notification system for inquiries
- Property rating and review system

---

## 📊 ERD Diagram

![ERD Diagram](/real-estate/backend/erd.png)

---

## 🛠 Installation Instructions

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
