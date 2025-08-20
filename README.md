# Peady - Pet Adoption API

A comprehensive Django REST API for a pet adoption system built with Django REST Framework.

## 🐾 Features

- **User Management**: User registration, authentication, and profile management with JWT tokens
- **Pet Management**: CRUD operations for pets with categories, images, and reviews
- **Shopping Cart**: Add pets to cart and manage cart items
- **Order Management**: Process adoption orders and track order history
- **Payment Processing**: Handle payments and transaction history
- **API Documentation**: Interactive API docs with Swagger and ReDoc
- **Admin Interface**: Django admin for managing all entities

## 🛠️ Technology Stack

- **Backend**: Django 5.0.6, Django REST Framework 3.15.1
- **Authentication**: JWT via djoser 2.3.1
- **Database**: PostgreSQL (configurable via environment)
- **File Storage**: Cloudinary integration
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Deployment**: Vercel-ready configuration

## 📁 Project Structure

```
peady/
├── api/                 # Main API routing and configuration
├── users/              # User management and authentication
├── pet/                # Pet models, views, and management
├── order/              # Shopping cart and order processing
├── payment/            # Payment handling and transactions
├── peady/              # Django project settings and configuration
├── staticfiles/        # Static files for admin and API docs
├── requirements.txt    # Python dependencies
├── manage.py          # Django management script
└── vercel.json        # Vercel deployment configuration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or SQLite for development)
- Cloudinary account (for media storage)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ERROR-41/peady.git
   cd peady
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   # Database
   DATABASE_URL=postgresql://username:password@localhost:5432/peady_db
   
   # Cloudinary (for media storage)
   CLOUD_NAME=your_cloudinary_cloud_name
   API_KEY=your_cloudinary_api_key
   API_SECRET=your_cloudinary_api_secret
   
   # Django
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Interface**: http://localhost:8000/admin/

## 🔗 API Endpoints

### Authentication
- `POST /auth/users/` - User registration
- `POST /auth/jwt/create/` - Login (JWT token)
- `POST /auth/jwt/refresh/` - Refresh JWT token
- `POST /auth/users/activation/` - Account activation

### Pets
- `GET /api/v1/pets/` - List all pets
- `POST /api/v1/pets/` - Create a new pet (admin)
- `GET /api/v1/pets/{id}/` - Get pet details
- `PUT /api/v1/pets/{id}/` - Update pet (admin)
- `DELETE /api/v1/pets/{id}/` - Delete pet (admin)

### Pet Categories
- `GET /api/v1/categories/` - List pet categories
- `POST /api/v1/categories/` - Create category (admin)

### Pet Reviews & Images
- `GET /api/v1/pets/{id}/reviews/` - Get pet reviews
- `POST /api/v1/pets/{id}/reviews/` - Add review
- `GET /api/v1/pets/{id}/images/` - Get pet images
- `POST /api/v1/pets/{id}/images/` - Add image (admin)

### Shopping Cart
- `GET /api/v1/carts/` - Get user's cart
- `POST /api/v1/carts/` - Create cart
- `GET /api/v1/carts/{id}/items/` - Get cart items
- `POST /api/v1/carts/{id}/items/` - Add item to cart

### Orders
- `GET /api/v1/orders/` - List user orders
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/{id}/items/` - Get order items

### User Profile & Account
- `GET /api/v1/profile/` - Get user profile
- `PUT /api/v1/profile/` - Update profile
- `GET /api/v1/account_balance/` - Get account balance
- `POST /api/v1/account_balance/` - Add money to account

### Payment
- `GET /api/v1/payment_history/` - Get transaction history

## 🧪 Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows Django and PEP 8 coding standards.

### Database Migrations
When you make model changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🚀 Deployment

### Vercel Deployment
This project is configured for Vercel deployment:

1. Install Vercel CLI: `npm install -g vercel`
2. Run: `vercel --prod`

The `vercel.json` file contains the deployment configuration.

### Environment Variables for Production
Set these environment variables in your deployment platform:
- `DATABASE_URL`
- `CLOUD_NAME`
- `API_KEY`
- `API_SECRET`
- `SECRET_KEY`
- `DEBUG=False`

## 📝 Models Overview

### User Model
- Custom user model with email authentication
- Profile information and account balance

### Pet Model
- Pet information (name, breed, age, description)
- Category relationship
- Image management via Cloudinary
- Review system

### Order System
- Shopping cart functionality
- Order processing and tracking
- Payment integration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Authors

- **ERROR-41** - *Initial work* - [ERROR-41](https://github.com/ERROR-41)

## 📞 Support

For support and questions, please contact: mdomarsadek41@gmail.com

---

Made with ❤️ for pet adoption