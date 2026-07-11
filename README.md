# Kala Mandir - Premium Handcrafted eCommerce Platform

A complete, modern, responsive, and production-ready eCommerce website built with Django and SQLite for a brand selling traditional Indian crafts, Ganpati idols, pooja items, handmade jewellery, and customized gifts.

## 🌟 Key Features

- **Premium & Elegant UI/UX**: Traditional Indian color palette (Saffron, Gold, White, Beige), modern typography, sticky glassmorphic navbar, floating cart, and micro-interactions.
- **Robust Catalog & Shop**: Features categories, multi-image product galleries, SKU tracking, stock management, related products, and search with multi-criteria filters.
- **Session-Based Cart**: Allows users to build carts without logging in, with dynamic totals and real-time updates.
- **Seamless Checkout**: Address auto-population, promotional coupon support, shipping summaries, and Cash on Delivery (COD) payment methods.
- **Order Tracking & Invoice Download**: Personalized dashboards tracking order states (Pending, Shipped, Delivered) with download/print-ready HTML invoices.
- **Accounts & Address Management**: Django custom user profile configuration with address CRUD support.
- **Content & Marketing**: Seeding banners, handcrafted blog articles for SEO, newsletter subscriptions, contact forms, and FAQs.

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2 (Latest version)
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS (via customizable CDN)
- **Database**: SQLite (default `db.sqlite3` included)
- **Authentication**: Django built-in auth system

---

## 🚀 Setup & Execution Instructions

Follow these commands to configure and run the application locally:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate and Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Load Sample Data & Create Default Superuser
Run the custom management command to seed categories, products, blog stories, coupons, and create the default admin account:
```bash
python manage.py load_sample_data
```

**Seeded Credentials:**
- **Admin Dashboard**: Username `admin` / Password `adminpass`
- **Promo Coupon**: Code `WELCOME10` (gives 10% discount at checkout)

### 4. Start the Server
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to view the store. Access the admin dashboard at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).
