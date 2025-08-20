#!/bin/bash

# Peady Development Setup Script

echo "🐾 Setting up Peady Pet Adoption API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before running the application."
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👤 Do you want to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the development server:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📖 API Documentation will be available at:"
echo "   http://localhost:8000/swagger/ (Swagger UI)"
echo "   http://localhost:8000/redoc/ (ReDoc)"
echo "   http://localhost:8000/admin/ (Django Admin)"