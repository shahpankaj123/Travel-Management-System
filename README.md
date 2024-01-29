# Travel Management System - Django

## Overview

The Travel Management System is a web-based application built with Django, Celery, and Redis, offering a comprehensive solution for managing travel-related activities within an organization. This project was developed by Anuj Bhattarai and Pankaj Shah.

## Technologies Used

- **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Celery:** An asynchronous task queue/job queue based on distributed message passing.
- **Redis:** An open-source, in-memory data structure store used as a message broker for Celery.
- **Signals:** An open-source, signals provide a way to allow certain senders to notify a set of receivers when certain actions occur.
  
## Features

1. **User Management:**
   - Create and manage user profiles for employees.
   - Define roles and permissions using Django's built-in authentication system.

2. **Trip Planning:**
   - Plan and schedule business trips for employees.
   - Specify travel details such as destination, duration, and purpose.

3. **Expense Management:**
   - Capture and track travel-related expenses.
   - Support for uploading and attaching receipts.
   - Automated calculation of per diems and reimbursements.

4. **Approval Workflow:**
   - Implement a multi-level approval process for trip requests and expenses.
   - Utilize Celery for handling asynchronous tasks related to approval notifications.

5. **Travel Itinerary:**
   - Generate detailed travel itineraries for employees.
   - Include flight details, hotel reservations, meeting schedules, etc.

6. **Integration with Booking Platforms:**
   - Integrate with external platforms for booking flights, hotels, and rental cars.
   - Retrieve and display real-time availability and pricing information.

7. **Reporting and Analytics:**
   - Generate reports on travel expenses, employee travel history, and more.
   - Utilize Django's ORM for efficient database querying.

8. **Mobile Accessibility:**
   - Leverage Django's responsive design capabilities for mobile-friendly interfaces.

## Installation

1. **Prerequisites:**
   - Install Python and set up a virtual environment.
   - Install Django, Celery, and Redis.

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/anuj-pankaj/travel-management-system.git
   cd travel-management-system
   ```

3. **Database Setup:**
   - Configure your database settings in the Django settings file.
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

4. **Celery Configuration:**
   - Configure Celery to use Redis as the message broker.
   - Start Celery:
     ```bash
     celery -A your_project_name worker -l info
     ```

5. **Run the Application:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   - Open your web browser and navigate to `http://localhost:8000`.

## Contributors

- Anuj Bhattarai ([GitHub](https://github.com/anuj66283))
- Pankaj Shah ([GitHub](https://github.com/shahpankaj123))

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Support

For any issues or inquiries, please contact the project maintainers:

- Anuj Bhattarai: anuj@example.com
- Pankaj Shah: pankaj@example.com

## Acknowledgments

- Special thanks to the Django, Celery, and Redis communities for their excellent documentation and support.
- Icons used in this project are provided by [FontAwesome](https://fontawesome.com).

---

Feel free to customize this README file based on your project's specific details and requirements.
