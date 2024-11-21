# OTA Shop Project

This project is a basic implementation of an Online Travel Agency (OTA) shop built with Django. The platform allows users to browse and book various travel-related services like hotel reservations, flights, and tours. Admins can manage the available services and track user bookings.

## Features

- **User Registration & Authentication**
  - Users can sign up and log in to the platform.
  - Authentication via email and password (JWT or session-based).

- **Travel Service Listings**
  - Display available travel services such as hotels, flights, and tours.
  - Filter services based on location, dates, and other preferences.

- **Booking & Payment**
  - Users can book travel services.
  - Payment gateway integration (e.g., Stripe, PayPal).

- **Admin Panel**
  - Admins can manage travel service listings.
  - Create, update, or delete services.

- **Order Management**
  - Track user bookings and orders.
  - View booking history for users and service providers.

## Technologies Used

- **Backend**: 
  - Django
  - Django REST Framework (for API endpoints)
  - PostgreSQL/MySQL (Database)

- **Frontend**: 
  - Optional: React.js/Vue.js or use Django Templates for frontend

- **Authentication**:
  - JWT (JSON Web Tokens) or session-based authentication

- **Payment Integration**: 
  - Stripe/PayPal (optional, depending on your implementation)

## Setup

### Prerequisites

Ensure you have the following installed:

- Python (>= 3.7)
- PostgreSQL/MySQL (Database)

### Install Dependencies

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ota-shop.git
   cd ota-shop
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database (PostgreSQL or MySQL):
   - Create the database for the project.
   - Update the database connection settings in `settings.py`.
   - Run Django migrations:
     ```bash
     python manage.py migrate
     ```

4. Create a superuser to access the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

### Running the Project

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

   This will run the backend at `http://127.0.0.1:8000/`.

2. If you have a frontend (React/Vue.js):
   - Navigate to the frontend directory:
     ```bash
     cd frontend
     npm install
     npm start
     ```

### Environment Variables

Create a `.env` file in the root directory and define the following environment variables:

- `DATABASE_URL`: Connection string for your database.
- `SECRET_KEY`: Secret key for your Django project.
- `DEBUG`: Set to `True` in development and `False` in production.
- `PAYMENT_API_KEY`: (Optional) For Stripe or PayPal integration.
- `ALLOWED_HOSTS`: Set allowed hosts for production deployment.

### Running Tests

To run tests for the backend:

```bash
python manage.py test
```

### Deployment

To deploy this application, you can use the following platforms:

- **Heroku**, **AWS**, **DigitalOcean** for hosting.
- **Docker** for containerization.

For deploying with Docker, follow these steps:

1. Build the Docker image:
   ```bash
   docker build -t ota-shop .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 ota-shop
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
