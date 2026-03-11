# 🚗 Smart Parking Boshqaruv Tizimi

Smart Parking Boshqaruv Tizimi — bu parking hududidagi mashinalarni boshqarish uchun yaratilgan backend tizimdir.

Tizim mashinalarning parkingga kirishi va chiqishini nazorat qiladi, parking joylarini boshqaradi va parking uchun to‘lovni avtomatik hisoblaydi.

Loyiha **Python, FastAPI va PostgreSQL** yordamida ishlab chiqiladi.

---

# 🎯 Loyiha maqsadi

Ushbu loyiha quyidagilarni amalga oshirish uchun yaratilgan:

* parkingga kirgan mashinalarni ro‘yxatga olish
* bo‘sh parking joylarini aniqlash
* mashina kirish vaqtini saqlash
* mashina chiqish vaqtini saqlash
* parkingda qancha vaqt turganini hisoblash
* avtomatik to‘lov hisoblash
* parking statistikalarini ko‘rsatish

---

# ⚙️ Texnologiyalar

Backend:

* Python
* FastAPI
* SQLAlchemy

Database:

* PostgreSQL

Tools:

* Git
* GitHub
* VS Code

---

# 🧠 Tizim arxitekturasi

```text
Frontend
   ↓
FastAPI (API)
   ↓
SQLAlchemy (ORM)
   ↓
PostgreSQL (Database)
```

---

# 🗄 Ma'lumotlar bazasi modeli

Tizim quyidagi asosiy jadvallardan tashkil topadi:

* users
* cars
* parking_slots
* parking_sessions
* payments
* pricing

---

# 🔗 ER Diagram

```
Car
 └── ParkingSession
        └── ParkingSlot

ParkingSession
 └── Payment

User
 └── ParkingSession

Pricing
 └── ParkingSession
```

---

# 🅿️ Tizim ishlash jarayoni

### Mashina kirishi

1. Mashina parkingga keladi
2. Operator mashina raqamini tizimga kiritadi
3. Tizim bo‘sh parking joyini topadi
4. Parking sessiya yaratiladi
5. Kirish vaqti yoziladi
6. Parking joy holati **occupied** bo‘ladi

---

### Mashina chiqishi

1. Operator mashina raqamini qidiradi
2. Chiqish vaqti yoziladi
3. Parking davomiyligi hisoblanadi
4. To‘lov miqdori hisoblanadi
5. To‘lov yozuvi yaratiladi
6. Parking joy yana **free** bo‘ladi

---

# 📊 Dashboard

Tizim quyidagi statistikalarni ko‘rsatadi:

* jami parking joylari
* band joylar
* bo‘sh joylar
* parkingdagi mashinalar
* kunlik daromad

Misol:

```
Jami joylar: 50
Band joylar: 32
Bo‘sh joylar: 18
Bugungi daromad: 240000 so‘m
```

---

# 📂 Loyiha strukturasi

```
smart_parking
│
├── app
│   ├── database
│   │   ├── config.py
│   │   └── db.py
│   │
│   ├── models
│   │   ├── user.py
│   │   ├── car.py
│   │   ├── parking_slot.py
│   │   ├── parking_session.py
│   │   ├── payment.py
│   │   └── pricing.py
│   │
│   ├── services
│   │   ├── parking_service.py
│   │   └── payment_service.py
│   │
│   ├── api
│   │   ├── cars.py
│   │   └── parking.py
│   │
│   └── main.py
│
├── requirements.txt
└── README.md
```

---

# ⚡ O‘rnatish (Installation)

Loyihani ishga tushirish uchun:

### 1. Repository ni yuklab oling

```
git clone https://github.com/username/smart-parking-system.git
```

### 2. Virtual environment yarating

```
python -m venv venv
```

### 3. Kutubxonalarni o‘rnating

```
pip install -r requirements.txt
```

---

# ▶ Loyihani ishga tushirish

```
uvicorn app.main:app --reload
```

Server ishga tushgandan so‘ng:

```
http://127.0.0.1:8000
```

manzil orqali API ishlaydi.

---

# 🚀 Kelajakdagi imkoniyatlar

Keyinchalik quyidagi funksiyalar qo‘shilishi mumkin:

* parking xaritasi (visual map)
* kamera orqali mashina raqamini aniqlash
* mobil ilova
* QR parking ticket
* real vaqt statistikasi

---

# 👨‍💻 Muallif

Berdimurodov Nodirbek
TATU Samarqand Filiali
Computer Engineering yo‘nalishi
