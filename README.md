# AlphaShop - Simple E-Commerce Store

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.1%2B-green)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)

A complete, responsive, full-stack **E-Commerce Web Application** built with **Python Django**, **SQLite**, and **modern HTML5/CSS3/JavaScript**.

---

## 🌟 Key Features

1. **Modern Homepage & Showcase**: Attractive hero section, live inventory metrics, curated product listings, and category showcase.
2. **Product Catalog & Filtering**:
   - Filter by categories (*Electronics, Audio, Wearables, Accessories, Home & Office*).
   - Instant search keyword query across product names and descriptions.
   - Dynamic sorting: Price (Low to High, High to Low), Top Rated, and Latest Arrivals.
3. **Product Details Page**:
   - High-resolution gallery view.
   - Live real-time stock availability badge (*In Stock, Low Stock alert, Out of Stock*).
   - Quantity selector with stock clamping.
   - Related products recommendation slider.
4. **Session-Based Shopping Cart**:
   - Persistent across page reloads using Django sessions.
   - Interactive quantity controls (`+` and `-` steppers).
   - One-click item removal with confirmation.
   - Dynamic subtotal, 8% tax calculation, and free shipping progress bar (Free for orders over $50).
5. **Simulated Secure Checkout**:
   - Customer shipping information form (Full name, email, phone, street address, city, postal code).
   - Form field validation and error messaging.
   - Simulated payment selection (*Cash on Delivery, Simulated Card, Demo UPI*).
   - No real payments or credit card processing required.
6. **Order Processing & Inventory Deduction**:
   - Atomically records `Order` and associated `OrderItem` database records.
   - Automatically decrements product stock in SQLite.
   - Empties cart upon successful placement.
   - Generates dedicated confirmation receipt page with order tracking code (`#ORD-XXXXX`).
7. **User Authentication**:
   - Customer registration with validation (username uniqueness, email check, password matching).
   - Login and secure logout using Django's built-in authentication system.
   - Pre-configured demo accounts.
8. **My Orders Dashboard**:
   - View past order history, line items, order timestamps, and fulfillment status (`Pending`, `Processing`, `Shipped`, `Delivered`).
9. **Django Admin Dashboard (`/admin/`)**:
   - Full CRUD control over **Products** (edit prices, stock, categories, image links).
   - Management of **Orders** and **OrderItems** (change status from Pending to Shipped/Delivered).
   - User account inspection and staff permission control.
10. **Responsive UI**:
    - Mobile-first responsive layout tested across mobile smartphones, tablets, and desktop displays.

---

## 📁 Project Directory Structure

```text
django_ecommerce/
├── ecommerce_site/              # Django Project Root
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # App settings, session engine, DB configs
│   ├── urls.py                  # Master routing (Admin & Store URLs)
│   └── wsgi.py
├── store/                       # Main Store App
│   ├── migrations/
│   │   ├── 0001_initial.py      # Database migration schemas
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                 # Django admin models & inlines
│   ├── apps.py
│   ├── context_processors.py    # Cart item count processor
│   ├── forms.py                 # User registration & checkout forms
│   ├── models.py                # Product, Order, OrderItem models
│   ├── urls.py                  # Store routes
│   └── views.py                 # E-commerce business logic
├── templates/                   # HTML5 Templates
│   ├── base.html                # Base layout with header & footer
│   └── store/
│       ├── cart.html            # Cart view
│       ├── checkout.html        # Checkout form
│       ├── home.html            # Homepage product listing
│       ├── login.html           # Authentication sign-in
│       ├── my_orders.html       # Customer order history
│       ├── order_success.html   # Order confirmation receipt
│       ├── product_detail.html  # Product details view
│       └── register.html        # New user registration
├── static/                      # Static Assets
│   ├── css/
│   │   └── style.css            # Custom CSS3 stylesheet
│   └── js/
│       └── main.js              # Vanilla JavaScript interactions
├── manage.py                    # Django CLI management script
├── requirements.txt             # Python package dependencies
├── seed_data.py                 # One-click sample data & superuser loader
└── README.md                    # Project documentation
```

---

## 🪟 Windows 11 Setup & Run Instructions

Follow these exact steps in **Visual Studio Code** on **Windows 11**:

### Step 1: Open the Project in VS Code
1. Extract the downloaded `codealpha_ecommerce_django.zip` to a folder (for example: `C:\Projects\django_ecommerce`).
2. Open **Visual Studio Code**.
3. Click **File** > **Open Folder...** and select the `django_ecommerce` folder.
4. Open the integrated terminal by pressing <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick) or going to **Terminal** > **New Terminal**.

---

### Step 2: Create and Activate a Python Virtual Environment

In the VS Code terminal (PowerShell or Command Prompt):

```powershell
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment on Windows PowerShell:
.\venv\Scripts\Activate.ps1

# (If using Windows Command Prompt CMD instead):
# venv\Scripts\activate.bat
```

> *Tip: If PowerShell displays an Execution Policy error, run:*
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

---

### Step 3: Install Required Dependencies

Ensure `pip` is up to date and install the packages from `requirements.txt`:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Run Database Migrations

Apply migrations to initialize the SQLite database (`db.sqlite3`):

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

### Step 5: Seed Sample Products & Pre-configured Accounts

Run the included automated seeding script. This loads 12 realistic tech products and creates default login credentials:

```powershell
python seed_data.py
```

Output:
```text
-> Starting database seeding for AlphaShop E-Commerce Store...
  [+] Superuser created: username='admin' | password='admin123'
  [+] Demo Customer created: username='demo_user' | password='password123'
  [+] Seeding complete! 12 products created.
```

*(Alternatively, to create your own custom administrator account, run: `python manage.py createsuperuser`)*

---

### Step 6: Start the Django Development Server

Run the development server:

```powershell
python manage.py runserver
```

---

### Step 7: Open the Website

Open your browser and navigate to:
👉 **`http://127.0.0.1:8000/`**

---

## 🔑 Default Test Credentials

| Role | Username | Password | Access Area |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Django Admin (`http://127.0.0.1:8000/admin/`) & Storefront |
| **Customer** | `demo_user` | `password123` | Storefront, Cart, Checkout & My Orders |

---

## 🧪 Evaluation & Testing Checklist

Use this step-by-step checklist to test and demonstrate all requirements:

1. **Product Browsing**:
   - Visit `http://127.0.0.1:8000/`.
   - Verify product cards display high-resolution images, ratings, prices, and stock statuses.
   - Click category filter pills (*Audio*, *Electronics*, *Wearables*, etc.).
   - Type in the search bar (e.g., `"keyboard"` or `"headphones"`) and verify filtered output.
   - Test the sorting dropdown (*Price: Low to High*, *Top Rated*).

2. **Product Details**:
   - Click the **"View Details"** or eye button on any product card.
   - Check description, highlighted features, and quantity adjuster.
   - Click **"Add to Cart"** and verify the green success toast notification.

3. **Shopping Cart**:
   - Open the **Cart** (`http://127.0.0.1:8000/cart/`).
   - Use `+` and `-` buttons to modify quantities. Notice how subtotal, tax, and total update.
   - Notice the Free Shipping banner dynamically updating.
   - Click the trash icon to remove an item and verify the cart updates.

4. **User Registration & Login**:
   - Click **Register** (`http://127.0.0.1:8000/register/`) and register a new test user.
   - Log in via `http://127.0.0.1:8000/login/` or sign in as `demo_user` (`password123`).

5. **Checkout & Order Processing**:
   - Click **"Proceed to Checkout"** from the cart.
   - Fill in customer details (Name, Address, Phone, City, Postal Code).
   - Select a payment method (*Cash on Delivery* or *Demo Card*).
   - Click **"Place Order"**.
   - Verify redirection to the **Order Confirmation** page with generated `#ORD-XXXXX` and receipt table.
   - Note that product stock was deducted in the database.

6. **Order History**:
   - Navigate to **"My Orders"** (`http://127.0.0.1:8000/my-orders/`) to verify your newly placed order appears with timestamp, items, and `Pending` status.

7. **Django Admin Dashboard**:
   - Visit `http://127.0.0.1:8000/admin/` and sign in with `admin` / `admin123`.
   - Open **Products**: edit a price, change stock quantity, or add a brand new product.
   - Open **Orders**: inspect customer addresses, click into an order, and update the status from `Pending` to `Shipped` or `Delivered`.
   - Return to the customer storefront and observe the live changes!

---

## 🛡️ Security Notes
- `SECRET_KEY` in `settings.py` reads from environment variables (`os.environ.get('DJANGO_SECRET_KEY')`) with a secure fallback for local development.
- CSRF tokens (`{% csrf_token %}`) protect all forms (login, registration, cart additions, checkout).
- Sensitive passwords are never stored in plaintext; Django's cryptographic PBKDF2 hashing algorithm is utilized.
