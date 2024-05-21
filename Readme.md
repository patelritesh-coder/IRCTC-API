# Railway Management System

This is a Flask application for managing railway operations, including user registration, login, seat availability, seat booking, and train management. It uses PostgreSQL as the database and includes features such as JWT-based authentication and API key protection for specific routes.

## Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- pip (Python package installer)

### Installation


1. **Create a virtual environment:**

    ```
    python3 -m venv venv
    source venv/bin/activate 
    ```

2. **Install the required packages:**

    ```
    pip install -r requirements.txt
    ```

3. **Set up the environment variables:**

    Create a `.env` file in the root directory of the project and add the following environment variables:

    ```plaintext
    SECRET_KEY=your_secret_key
    DATABASE_URL=postgresql://username:password@localhost/railway_management
    API_KEY=your_api_key
    ```

    Replace `your_secret_key`, `username`, `password`, and `your_api_key` with your actual values.

4. **Set up the PostgreSQL database:**

    Ensure PostgreSQL is installed and running. Then create a database:

    ```sql
    CREATE DATABASE railway_management;
    ```




## API Endpoints

- **User Registration:** `POST /api/register`
- **User Login:** `POST /api/login`
- **Get Seat Availability:** `GET /api/seat_availability?source={source}&destination={destination}`
- **Book a Seat:** `POST /api/book_seat`
- **Get Booking Details:** `GET /api/booking_details`
- **Add Train:** `POST /api/add_train` (requires API key and admin role)
