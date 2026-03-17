# 🍋 Little Lemon Django RESTful API
**Meta Back-End Developer Professional Certificate: Capstone Project**

## 📖 Description
A fully functional RESTful API built with Django and Django REST Framework for the fictional Little Lemon restaurant. The system supports three user roles — **managers**, **customers**, and **delivery crew** — and implements user registration, token authentication, role assignment, menu management, cart workflows, order processing, delivery assignment, filtering, pagination, search, and API throttling.

This API serves as the engine for Little Lemon’s digital ecosystem. It handles complex workflows for three distinct user groups: **Managers**, **Customers**, and the **Delivery Crew**.

The database is uniquely populated with authentic Venezuelan cuisine, adding a personal touch to the implementation of categories like Arepas, Cachapas, and Patacones.

### Course Project
This project was created as the final assessment for **Module 6: APIs** in the **Meta Back-End Developer Professional Certificate** on **Coursera**. It demonstrates practical application of authentication, permissions, serializers, viewsets, filtering, pagination, and throttling.

## 🧭 Project Overview
The API provides:

- Token-based authentication (Djoser)
- Role management (Manager, Delivery Crew, Customer)
- CRUD operations for menu items (manager only)
- Category management
- Cart system with one active cart per customer
- Order creation that automatically empties the cart
- Manager assignment of delivery crew
- Delivery crew order updates
- Filtering, searching, sorting, and pagination
- Throttling (5 requests per minute)
- Proper HTTP methods and status codes

## 📁 Project Folder Structure

```plaintext
littlelemon-django-rest-api/
│
├── LittleLemon/
│   ├── LittleLemon/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── LittleLemonAPI/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── db.sqlite3
│   ├── Important_notes.txt
│   ├── manage.py
│   ├── Pipfile
│   └── Pipfile.lock
│
├── Insomnia_2024-10-18.json
├── README.md
└── assets/
```

---

# **Insomnia Collection**

## 🧪 Testing with Insomnia (Recommended)
To make reviewing this project as easy as possible, I have included a pre-configured Insomnia workspace.

- **File:** ```Insomnia_2024-10-18.json``` (located in the root directory).
- **How to use:** Import this file into [Insomnia](https://insomnia.rest/) to access all endpoints pre-filled with the correct methods, headers, and body payloads.

```markdown
## 🧪 Insomnia Collection (Recommended for Testing)

The repository includes **Insomnia_2024-10-18.json**, which contains **all API endpoints**, fully organized into folders:

1. Djoser endpoints
    1.1. Any user Signup: Create new user
    1.2. Any user: List current user
    1.3. Any user login: Generate access token
    1.4. Any logged in user logout: Destroy access token
2. User group management endpoints
    2.1. Manager: List all Managers
    2.2. Manager: Assign user to Manager group
    2.3. Manager: Remove user from Manager group
    2.4. Manager: List all Delivery crews
    2.5. Manager: Assign user to Delivery crew group
    2.6. Manager: Remove user from Delivery crew group
3. Category endpoints
    3.1. Any user: List all Categories
    3.2. Manager: Create new Category
    3.3. Any user: List single Category
    3.4. Manager: Edit single Category
    3.5. Manager: Delete single Category
4. Menu-items endpoints
    4.1. Any user: List all MenuItems
    4.2. Manager: Create new MenuItem
    4.3. Manager: Create new MenuItem(s) from JSON payload
    4.4. Any user: List single MenuItem
    4.5. Manager: Edit single MenuItem
    4.6. Manager: Delete single MenuItem
    4.7. Any user: List MenuItem(s) of the day
    4.8. Manager: Update MenuItem of the day
5. Cart management endpoints
    5.1. Customer: List current items in the cart
    5.2. Customer: Add MenuItem to the cart
    5.3. Customer: Delete MenuItems from own cart
6. Order management endpoints
    6.1. Customer: List all Orders from this User
    6.2. Delivery crew: List all Orders assigned to them
    6.3. Manager: List all Orders from all Users
    6.4. Customer: Create a new Order for this User
    6.5. Manager: Delete single Order
    6.6. Manager: Update single Order status and delivery_crew
    6.7. Customer: List single Order
    6.8. Delivery crew: Update single Order status
7. Additional endpoints
    7.1. Manager: List all users

Each request already includes:

- Correct HTTP method  
- Correct URL  
- Correct headers  
- Correct body format  
- Preconfigured tokens (for demonstration only)

**Import this file into Insomnia to test the entire API quickly and efficiently.**
```

---

## 1. Djoser Endpoints

### 1.1. Create new user — POST `/api/users/`
![Create a new user](assets/Screenshot_01_create_new_user.png)

### 1.2. List current user — GET `/api/users/me/`
![List current user](assets/Screenshot_02_list_current_user.png)

### 1.3. Generate access token — POST `/api/token/login/`
![Generate access token](assets/Screenshot_03_generate_access_token.png)

### 1.4. Logout — POST `/api/token/logout/`
(No screenshot)

---

## 2. User Group Management Endpoints

### 2.1. List all Managers — GET `/api/groups/manager/users`
![List all managers](assets/Screenshot_04_list_all_managers.png)

### 2.4. List all Delivery Crew — GET `/api/groups/delivery-crew/users`
![List all delivery crew](assets/Screenshot_05_list_all_delivery_crews.png)

---

## 3. Category Endpoints

### 3.1. List all Categories — GET `/api/category`
![List all categories](assets/Screenshot_06_list_all_categories.png)

### 3.3. List single Category — GET `/api/category/{categoryId}`
![List single category](assets/Screenshot_07_list_single_category.png)

---

## 4. Menu-Items Endpoints

### 4.1. List all MenuItems — GET `/api/menu-items`
![List all MenuItems](assets/Screenshot_08_list_all_menu_items.png)

### 4.4. List single MenuItem — GET `/api/menu-items/{menuItem}`
![List single MenuItem](assets/Screenshot_09_list_single_menu_item.png)

### 4.5. Edit single MenuItem — PUT `/api/menu-items/{menuItem}`
![Edit single MenuItem](assets/Screenshot_10_edit_single_menu_item.png)

### 4.7. List MenuItem(s) of the day — GET `/api/menu-items/item-of-the-day`
![List MenuItem of the day](assets/Screenshot_11_list_menu_item_of_the_day.png)

---

## 5. Cart Management Endpoints
(No screenshots provided.)

---

## 6. Order Management Endpoints

### 6.3. Manager: List all Orders — GET `/api/orders`
![List all orders](assets/Screenshot_12_list_all_order_from_all_users.png)

### 6.7. Customer: List single Order — GET `/api/orders/{orderId}`
![List single order](assets/Screenshot_13_list_single_order.png)

---

## 7. Additional Endpoints

### 7.1. Manager: List all users
![List all users](assets/Screenshot_14_list_all_users.png)

# 🔐 Authentication and Permissions

- **Token Authentication** required for protected endpoints  
- **Managers**: menu CRUD, assign roles, assign orders  
- **Delivery Crew**: view assigned orders, update status  
- **Customers**: browse menu, manage cart, place orders  

---

# 📋 HTTP Status Codes

- **200 OK** — successful GET/PUT/PATCH/DELETE  
- **201 Created** — successful POST  
- **400 Bad Request** — invalid data  
- **401 Unauthorized** — authentication required  
- **403 Forbidden** — insufficient permissions  
- **404 Not Found** — resource does not exist  

---

# ⏱️ Throttling

All authenticated and anonymous users are limited to **5 requests per minute**.

# ▶️ Setup and Run

## Install and activate virtual environment (pipenv)

```bash
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

pipenv shell                # Activates the Virtual Environment
pipenv install              # Installs dependencies from Pipfile
pipenv install django       # Installs Django

python manage.py migrate
python manage.py runserver
```

---

# 📬 Author
Fausto Gonzalez

