# Django API Project

  This is a simple Django-based API for managing products and categories in a store. This API uses Redis for caching frequently accessed data to optimize database queries.

## Table of Contents
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
  - [Running The Project](#running-the-project)
  - [API Endpoints](#api-endpoints)

## Prerequisites

  Before setting up the project, ensure you have the following installed:
  
  - python 3.8 or higher
  - django
  - djangorestframework
  - environs
  - django-redis
  - django_filters
  - debug_toolbar

## Configuration

  Make sure to create a .env file and configurate the REDIS_URL variable based on your own redis server.

## Running The Project

  1. Move to store-API directory:
  
     ```bash
     cd django-api-project
     
  2. Set up the database (If not yet):
     
     ```bash
     python manage.py migrate
     
  3. Start the Django development server:
     
     ```bash
     python manage.py runserver
     
  4. Run test (Optional):
     
     ```bash
     python manage.py test  

## API Endpoints
### 1. **Category Endpoints**

- **GET /api/categories/**
  - **Description:** List all categories.
  - **Response:** A list of all categories.

- **POST /api/categories/**
  - **Description:** Create a new category.
  - **Request Body:**
    ```json
    {
      "name": "Category Name",
      "description": "Description of the category"
    }
    ```
  - **Response:** The newly created category.

- **GET /api/categories/{id}/**
  - **Description:** Retrieve a category by ID.
  - **Response:** The details of the specified category.

- **PUT /api/categories/{id}/**
  - **Description:** Update a category.
  - **Request Body:**
    ```json
    {
      "name": "Updated Category Name",
      "description": "Updated description"
    }
    ```
  - **Response:** The updated category.

- **DELETE /api/categories/{id}/**
  - **Description:** Delete a category.
  - **Response:** Confirmation of the category deletion.

---

### 2. **Product Endpoints**

- **GET /api/products/**
  - **Description:** List all products with optional filtering.
  - **Optional Filters:**
    - `category`: Filter products by category name.
    - `price_min` and `price_max`: Filter products within a price range.
  - **Response:** A list of products matching the filters (if any).

- **POST /api/products/**
  - **Description:** Create a new product.
  - **Request Body:**
    ```json
    {
      "name": "Product Name",
      "description": "Product description",
      "price": 99.99,
      "category": "Category ID"
    }
    ```
  - **Response:** The newly created product.

- **GET /api/products/{id}/**
  - **Description:** Retrieve a product by ID.
  - **Response:** The details of the specified product.

- **PUT /api/products/{id}/**
  - **Description:** Update a product.
  - **Request Body:**
    ```json
    {
      "name": "Updated Product Name",
      "description": "Updated description",
      "price": 89.99,
      "category": "Updated Category ID"
    }
    ```
  - **Response:** The updated product.

- **DELETE /api/products/{id}/**
  - **Description:** Delete a product.
  - **Response:** Confirmation of the product deletion.
