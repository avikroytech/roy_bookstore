# Roy Bookstore

An e-commerce web application for browsing, purchasing, and managing a digital bookstore. Users can register, log in, browse books by category, add items to their cart, and complete purchases using Stripe payment integration.

## Purpose

Roy Bookstore is a full-featured online bookstore application that provides:
- **User Authentication**: Register, login, and password recovery functionality
- **Book Browsing**: Browse books by topic/category with detailed information
- **Shopping Cart**: Add/remove books from a persistent shopping cart
- **Secure Payments**: Stripe integration for safe payment processing
- **User Accounts**: Manage user profiles and purchase history

## Repository Contents

### Project Structure

```
roy_bookstore/
├── app.py                          # Application entry point
├── config.py                       # Configuration settings
├── application/
│   ├── __init__.py                # Flask app factory
│   ├── models.py                  # Database models (User, Book, Cart)
│   ├── forms.py                   # WTForms for validation
│   ├── bookinfo.py                # Book data/catalog
│   ├── main_routes.py             # Main pages & payment routes
│   ├── book_routes.py             # Book browsing & cart management
│   ├── login_routes.py            # Authentication routes
│   ├── static/
│   │   ├── navbar.css             # Navigation styling
│   │   └── main.js                # Client-side logic
│   └── templates/                 # HTML templates
│       ├── base.html              # Base template
│       ├── home.html              # Homepage
│       ├── books.html             # Books list page
│       ├── book_info.html         # Book detail page
│       ├── cart.html              # Shopping cart
│       ├── payment.html           # Checkout page
│       ├── login.html             # Login page
│       ├── register.html          # Registration page
│       ├── account.html           # User account page
│       ├── forgot.html            # Password recovery
│       ├── forgot_confirm.html    # Recovery confirmation
│       ├── welcome.html           # Welcome page (authenticated)
│       ├── complete.html          # Order completion page
│       └── 404error.html          # Error page
```

### Key Files

- **app.py**: Entry point that creates and runs the Flask application
- **config.py**: Configuration management for database, email, and Stripe settings
- **models.py**: Database models for User, Book, and Cart entities
- **main_routes.py**: Routes for homepage, 404 error handling, and Stripe payment processing
- **book_routes.py**: Routes for viewing books, book details, and cart management
- **login_routes.py**: Routes for user registration, login, logout, and password recovery

## Technologies Used

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-SQLAlchemy** - ORM for database management
- **Flask-Login** - User session management
- **Flask-Mail** - Email functionality for account notifications

### Frontend
- **HTML/CSS** - Template rendering with Jinja2
- **JavaScript** - Client-side interactions
- **Bootstrap** (implied from templates) - Responsive design

### Database
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite/PostgreSQL** - Database (configurable via environment variables)

### Payment
- **Stripe API** - Secure payment processing

### Authentication & Security
- **Werkzeug** - Password hashing and security utilities
- **WTForms** - Form validation and CSRF protection

## Application Flow

```mermaid
sequenceDiagram
    participant User
    participant Client as Client Browser
    participant Server as Flask Server
    participant DB as Database
    participant Mail as Mail Server
    participant Stripe as Stripe API

    User->>Client: Visit Homepage
    Client->>Server: GET /
    Server->>DB: Load books catalog
    DB-->>Server: Book data
    Server-->>Client: Render home.html
    Client-->>User: Display homepage

    User->>Client: Click Register
    Client->>Server: POST /register (form data)
    Server->>DB: Check email/username uniqueness
    DB-->>Server: Validation result
    alt Email/Username Valid
        Server->>DB: Create new user
        DB-->>Server: User created
        Server->>Mail: Send confirmation email
        Mail-->>Server: Email sent
        Server-->>Client: Redirect to login
        Client-->>User: Show login page
    else Duplicate Email/Username
        Server-->>Client: Show error message
        Client-->>User: Display error
    end

    User->>Client: Login
    Client->>Server: POST /login (credentials)
    Server->>DB: Query user by username
    DB-->>Server: User record
    Server->>Server: Verify password
    alt Password Correct
        Server->>Server: Create session
        Server-->>Client: Set session cookie
        Client-->>User: Redirect to welcome
    else Password Incorrect
        Server-->>Client: Show error
        Client-->>User: Display error
    end

    User->>Client: Browse Books by Topic
    Client->>Server: GET /books/topic_name
    Server->>DB: Query books by topic
    DB-->>Server: Book list
    Server-->>Client: Render books.html
    Client-->>User: Display book catalog

    User->>Client: View Book Details
    Client->>Server: GET /book_info/book_name
    Server->>DB: Query book details
    DB-->>Server: Book information
    Server-->>Client: Render book_info.html
    Client-->>User: Display book details

    User->>Client: Add to Cart
    Client->>Server: GET /add_to_cart/book_id
    Server->>Server: Update cart cookie
    Server-->>Client: Set cart cookie
    Client-->>User: Show cart updated

    User->>Client: View Cart
    Client->>Server: GET /cart/username
    Server->>DB: Fetch book details from cart
    DB-->>Server: Book prices and info
    Server-->>Client: Render cart.html
    Client-->>User: Display cart items

    User->>Client: Checkout
    Client->>Server: GET /create-checkout-session
    Server->>Stripe: Create checkout session
    Stripe-->>Server: Session ID
    Server-->>Client: Return session ID
    Client->>Stripe: Redirect to Stripe checkout
    Stripe-->>User: Display payment form

    User->>Stripe: Enter Payment Info
    Stripe->>Stripe: Process payment
    alt Payment Successful
        Stripe-->>Client: Redirect to success
        Client->>Server: Confirm order
        Server->>DB: Update order status
        DB-->>Server: Confirmed
        Server-->>Client: Render complete.html
        Client-->>User: Show order confirmation
    else Payment Failed
        Stripe-->>Client: Show error
        Client-->>User: Display error message
    end
```

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd roy_bookstore
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-mail python-dotenv stripe
   ```

4. **Configure environment variables** (create `.env` file)
   ```
   SECRET_KEY=your-secret-key
   FLASK_APP=app.py
   FLASK_ENV=development
   SQLALCHEMY_DATABASE_URI=sqlite:///books.db
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_USE_TLS=True
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   ```
   http://127.0.0.1:5000/
   ```

## Features

- ✅ User registration and authentication
- ✅ Secure password storage
- ✅ Browse books by category
- ✅ View detailed book information
- ✅ Add/remove items from shopping cart
- ✅ Persistent cart using cookies
- ✅ Stripe payment integration
- ✅ Email notifications for registration
- ✅ Password recovery functionality
- ✅ Responsive web design