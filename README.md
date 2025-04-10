# Inventory Management System

A simple and efficient inventory management system built with Django.

## Features
- User authentication and authorization
- Product management (CRUD operations)
- Stock tracking and management
- Low stock alerts
- REST API endpoints
- Basic reporting

## Setup Instructions

1. Create a virtual environment:
```bash
# On Windows: 
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

To access Django admin go to: http://127.0.0.1:8000/admin/

For report page: http://127.0.0.1:8000/admin/reports/

## How to Test APIs

1. Generate token:
```bash
Method: POST
URL: http://127.0.0.1:8000/api/token/
Headers: {
  "Content-Type": "application/json"
}
Body: {"username":"username", "password":"password"}
```


2. List products:
```bash
Method: GET
URL: http://127.0.0.1:8000/api/products/
Headers: {
  "Authorization": "Bearer <access_token>"
}
```

3. Manage stock (add/remove stock):
```bash
Method: POST
URL: http://127.0.0.1:8000/api/products/{product_id}/adjust_stock/
Headers: {
  "Authorization": "Bearer <access_token>",
  "Content-Type": "application/json"
}
Body: {
  "quantity_change": 10,
  "change_type": "add",
  "reason": "New stock received"
}
```

4. Add New Product:
```bash
Method: POST
URL: http://127.0.0.1:8000/api/products/
Headers: {
  "Authorization": "Bearer <access_token>",
  "Content-Type": "application/json"
}
Body: {
    "name": "Laptop",
    "sku": "LP-001",
    "price": 999.99,
    "quantity": 50,
    "description": "{description}",
    "catogary": catogary_id,
    "supplier": supplier_id
}
```

5. Update Product:
```bash
Method: PUT
URL: http://127.0.0.1:8000/api/products/{product_id}/
Headers: {
  "Authorization": "Bearer <access_token>",
  "Content-Type": "application/json"
}
Body: {
    "name": "Laptop",
    "sku": "LP-001",
    "price": 999.99,
    "quantity": 50,
    "description": "{description}",
    "catogary": catogary_id,
    "supplier": supplier_id
}
```

6. Delete Product:
```bash
Method: DELETE
URL: http://127.0.0.1:8000/api/products/{product_id}/
Headers: {
  "Authorization": "Bearer <access_token>"
}
```


7. View stock alerts:
```bash
Method: GET
URL: http://127.0.0.1:8000/api/products/stock_alerts/
Headers: {
  "Authorization": "Bearer <access_token>"
}
```

8. Total inventory value:
```bash
Method: GET
URL: http://127.0.0.1:8000/api/products/inventory_value/
Headers: {
  "Authorization": "Bearer <access_token>"
}
```

9. View stock logs:
```bash
Method: GET
URL: http://127.0.0.1:8000/api/stock-logs/
Headers: {
  "Authorization": "Bearer <access_token>"
}
```