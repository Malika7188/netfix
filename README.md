# Netfix - Service Management Platform

**Netfix** is a Django-based platform that connects service providers with customers, offering user authentication, service listings, and request management.

---

## 🚀 Features

### 🔐 User Authentication

- **Dual Registration:**
  - **Customers** can sign up using email, username, and birth date.
  - **Companies** register with a specified service field specialization.
- **Validation:**
  - Age verification (minimum 18+ years).
  - Unique email enforcement.
  - Secure password handling.

### 🛠️ Service Management

- **Service CRUD Operations:**
  - Companies can create, update, and manage their services.
  - Service creation is field-specific (except for "All-in-One" companies).
- **Dynamic Filtering:**
  - Browse services by category (e.g., Plumbing, Electricity).
  - URL-slug-based filtering (e.g., `/services/plumbing/`).

### 📩 Request System

- **Customers can:**
  - Submit service requests.
  - Specify address and duration.
  - View request history.

---

## ⚙️ Installation

### 1. Clone the repository:

```bash
git clone https://learn.zone01kisumu.ke/git/masman/netfix.git
cd netfix
````

### 2. Set up the environment:

**Create the virtual environment:**

```bash
python3 -m virtualenv env
```

**Activate the virtual environment:**

```bash
source env/bin/activate
```

**Install the dependencies:**

```bash
pip install -r requirements.txt
```

### 3. Apply migrations:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 4. Start the server:

```bash
python3 manage.py runserver
```

---

## 👥 Authors

[Malika Asman](https://github.com/Malika7188)

[Andrew Osindo](https://github.com/andyosyndoh)

