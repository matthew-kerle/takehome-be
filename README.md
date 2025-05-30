# Bungalow Take Home Project for Backend Developer Role

## To Do
- [ ] Fix "Load More" in frontend
- [ ] Finish filtering

## About This Project
This is a Django based assignment. We have created a base project for you to work from. 
You are free to vary from our original base if you would like to. We provide it with the intention of providing 
a common base for all candidates to work from and to hopefully save you a bit of time. 

If you need an introduction to Django, their docs are an excellent place to start: https://docs.djangoproject.com/en/3.2

We encourage you to use the Django Rest Framework for developing your API. This is a framework that we use extensively 
at Bungalow, and it provides some nice functionality out of the box. https://www.django-rest-framework.org/

## What to Build
We would like you to build an API that can be used to query some information about houses.
Sample data is provided in the `sample-data` folder.
We have provided the stub for a Django command to import the data. Finish writing this code.
You should use Django's ORM to model the data and store it in a local database.
Then, utilize the Django Rest Framework to provide an API to query the models.
A very basic API design here would simply return all of the data available.
You can choose to improve and refine this very basic API design, and we encourage you to do so.
This will give us an opportunity to see how you approach API design.
If you are running out of time, you can outline how you would have done things differently given more time.

## Setup Instructions

### Option 1: Local Setup
1. Fork this repository and clone to your local environment. If you make your fork private, please give access to the `bungalow-engineering` user. 
1. Install a version of Python 3 if you do not already have one. We recommend Python 3.8 or newer.
1. You can use the built-in virtual environment creation within Python to create a sandboxed set of package installs. 
   If you already have a preferred method of virtualenv creation, feel free to proceed with your own method. 
   `python -m venv env`    
1. You will need to activate your virtual environment each time you want to work on your project. 
   Run the `activate` script within the `env/bin` folder that was generated.
1. We have provided a `requirements.txt` file you can use to install the necessary packages.
   With your virtualenv activated run: `pip install -r requirements.txt`
1. To run the django server run `python manage.py runserver`
1. To run the data import command run `python manage.py import_house_data`
1. You are now setup and ready to start coding. 

### Option 2: Docker Setup
The project includes Docker configuration for easy setup and consistent development environment.

#### Prerequisites
- Docker and Docker Compose installed on your system
- Git for cloning the repository

#### Setup Steps
1. Fork and clone the repository
2. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```
3. Apply database migrations:
   ```bash
   docker-compose exec web python listings/manage.py migrate
   ```

#### Docker Commands
- Start containers: `docker-compose up -d`
- Stop containers: `docker-compose down`
- View logs: `docker-compose logs -f`
- Execute commands in container: `docker-compose exec web <command>`
- Rebuild containers: `docker-compose up -d --build`

### Development Tools and Linting

The project includes several development tools to ensure code quality and consistency:

#### Linting Tools
- **flake8**: Python code style checker
- **black**: Python code formatter
- **isort**: Python import sorter
- **mypy**: Static type checker for Python

#### Available Commands
You can run linting commands through Docker:

```bash
# Run all linting checks
docker-compose exec web lint

# Run type checking
docker-compose exec web type-check

# Format code
docker-compose exec web format

# Run all checks (linting and type checking)
docker-compose exec web check
```

The linters are configured to enforce:
- PEP 8 style guidelines
- Consistent code formatting
- Proper import ordering
- Type annotations where appropriate

### Database Setup
The project uses PostgreSQL as the database. You can connect to it using:

#### Connection Details
- Host: localhost
- Port: 5433
- Database: listings
- Username: postgres
- Password: postgres

#### Connection URI
```
postgresql://postgres:postgres@localhost:5433/listings
```

#### Database Management
- The database data is persisted in a Docker volume
- Migrations are automatically applied when starting the container
- You can manually run migrations with: `docker-compose exec web python listings/manage.py migrate`

### Seed Data
To import the sample listing data:
```bash
# Import seed data (preserves existing records)
docker-compose exec web python listings/manage.py import_listing_data

# Import seed data and reset existing records
docker-compose exec web python listings/manage.py import_listing_data --reset
```

## Time Spent
*Give us a rough estimate of the time you spent working on this. If you spent time learning in order to do this project please feel free to let us know that too.*
*This makes sure that we are evaluating your work fairly and in context. It also gives us the opportunity to learn and adjust our process if needed.*

## Assumptions
*Did you find yourself needing to make assumptions to finish this?*
*If so, what were they and how did they impact your design/code?*

### Improvements

#### Backend
- Caching mechanism for listings based on product requirements.

#### Frontend
- Add environment variables so it's actually production ready.
- Handle pre-fetching, loading states, caching, and error states better
- Spend more time on responsiveness
- Add real frontend tests
- Break things into more atomic components
- Add Prettier + ESLint into the frontend
- Wire up listing filtering
- Wire up "favorites"

### Features

### Testing

### Anything else needed to make this production ready?

## API Documentation

### Base URL
The API is available at `http://localhost:8000/api/`

### Endpoints

#### Listings
- **GET /api/listings/** - List all listings
- **GET /api/listings/{id}/** - Get a specific listing

### Query Parameters

#### Filtering
You can filter listings using the following parameters:
- `bedrooms` - Number of bedrooms
- `bathrooms` - Number of bathrooms
- `home_type` - Type of home
- `city` - City name (spaces should be URL encoded as %20)
- `state` - State code
- `zipcode` - ZIP code
- `year_built` - Year the home was built
- `tax_year` - Year of tax assessment

For price fields, you can filter using a range of values:
- `price` - Current listing price (in cents)
- `last_sold_price` - Last sold price (in cents)
- `rent_price` - Rental price (in cents)
- `rentzestimate_amount` - Zillow rent estimate (in cents)
- `tax_value` - Tax assessed value (in cents)
- `zestimate_amount` - Zillow home value estimate (in cents)

To filter within a range, use the `min` and `max` parameters for any price field. For example:
```
# Get listings priced between $1M and $2M (100000000 and 200000000 cents)
GET /api/listings/?price_min=100000000&price_max=200000000

# Get listings with rent estimates between $2K and $3K (200000 and 300000 cents)
GET /api/listings/?rentzestimate_amount_min=200000&rentzestimate_amount_max=300000
```

Example combining multiple filters:
```
# Get listings in San Francisco with 3 bedrooms priced between $1M and $2M
GET /api/listings/?bedrooms=3&city=San%20Francisco&price_min=100000000&price_max=200000000
```

#### Searching
You can search listings using the `search` parameter, which searches across:
- `address` (spaces should be URL encoded as %20)
- `city` (spaces should be URL encoded as %20)
- `state`
- `zipcode`

Example:
```
# URL encoded version
GET /api/listings/?search=San%20Francisco

# Non-encoded version (for reference only, use the encoded version above)
GET /api/listings/?search=San Francisco
```

#### Ordering
You can order listings using the `ordering` parameter with the following fields:
- `price` - Current listing price
- `last_sold_price` - Last sold price
- `rent_price` - Rental price
- `rentzestimate_amount` - Zillow rent estimate
- `tax_value` - Tax assessed value
- `zestimate_amount` - Zillow home value estimate
- `year_built` - Year built
- `home_size` - Size of the home
- `property_size` - Size of the property

Add a `-` prefix for descending order.

Example:
```
GET /api/listings/?ordering=-price
```

#### Pagination
All list endpoints are paginated with the following features:

- **Default Settings**
  - 10 items per page
  - Page numbers start at 1
  - Maximum page size of 100 items

- **Query Parameters**
  - `page` - Page number to retrieve (default: 1)
  - `page_size` - Number of items per page (default: 10, max: 100)

- **Response Format**
  ```json
  {
    "count": 448,           // Total number of items
    "next": "http://localhost:8000/api/listings/?page=2",  // URL for next page
    "previous": null,       // URL for previous page
    "results": [            // List of items for current page
      {
        // Listing data
      }
    ]
  }
  ```

Example API calls:
```
# Get first page with default page size (10 items)
GET /api/listings/

# Get second page with 20 items per page
GET /api/listings/?page=2&page_size=20

# Get last page (calculated from total count)
GET /api/listings/?page=45

# Get all items in a single page (up to max page size)
GET /api/listings/?page_size=100
```

Note: The `next` and `previous` URLs in the response will automatically include any filters, search terms, or ordering parameters from the original request.

### Example API Calls

Using curl:
```bash
# Get all listings
curl http://localhost:8000/api/listings/

# Get listings with 3 bedrooms in San Francisco (URL encoded)
curl "http://localhost:8000/api/listings/?bedrooms=3&city=San%20Francisco"

# Get listings priced between $1M and $2M
curl "http://localhost:8000/api/listings/?price_min=100000000&price_max=200000000"

# Search for listings in San Francisco and order by price (URL encoded)
curl "http://localhost:8000/api/listings/?search=San%20Francisco&ordering=-price"
```

Using Python requests:
```python
import requests

# Get all listings
response = requests.get('http://localhost:8000/api/listings/')
listings = response.json()

# Get listings with specific filters (requests handles URL encoding automatically)
params = {
    'bedrooms': 3,
    'city': 'San Francisco',  # requests will handle the URL encoding
    'ordering': '-price'
}
response = requests.get('http://localhost:8000/api/listings/', params=params)
listings = response.json()

# Get listings within a price range
params = {
    'price_min': 100000000,  # $1M
    'price_max': 200000000,  # $2M
    'city': 'San Francisco'
}
response = requests.get('http://localhost:8000/api/listings/', params=params)
listings = response.json()
```

### Response Format
The API returns JSON responses with the following structure:

```json
{
    "count": 448,
    "next": "http://localhost:8000/api/listings/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "zillow_id": "20023224",
            "area_unit": "SqFt",
            "bathrooms": 3.0,
            "bedrooms": 3,
            "home_size": 2000,
            "home_type": "Single Family",
            "last_sold_date": "2020-01-15",
            "last_sold_price": "$2.4M",
            "link": "https://www.zillow.com/homedetails/...",
            "price": "$2.4M",
            "property_size": 5000,
            "rent_price": null,
            "rentzestimate_amount": "$3,850",
            "rentzestimate_last_updated": "2024-01-01",
            "tax_value": "$95,860",
            "tax_year": 2023,
            "year_built": 1990,
            "zestimate_amount": "$1,003,906",
            "zestimate_last_updated": "2024-01-01",
            "address": "123 Main St",
            "city": "San Francisco",
            "state": "CA",
            "zipcode": "94105",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        // ... more listings
    ]
}
```

### Testing the API
You can test the API using any of the following methods:

1. **Browser**
   - Simply visit `http://localhost:8000/api/listings/` in your browser
   - Add query parameters directly in the URL

2. **curl**
   ```bash
   # Get all listings
   curl http://localhost:8000/api/listings/

   # Get listings with filters
   curl "http://localhost:8000/api/listings/?bedrooms=3&city=San%20Francisco"
   ```

3. **Postman**
   - Import the following collection:
   ```json
   {
     "info": {
       "name": "Bungalow Listings API",
       "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
     },
     "item": [
       {
         "name": "Get All Listings",
         "request": {
           "method": "GET",
           "url": "http://localhost:8000/api/listings/"
         }
       },
       {
         "name": "Get Filtered Listings",
         "request": {
           "method": "GET",
           "url": "http://localhost:8000/api/listings/",
           "query": [
             {"key": "bedrooms", "value": "3"},
             {"key": "city", "value": "San Francisco"},  // Postman handles URL encoding automatically
             {"key": "ordering", "value": "-price"}
           ]
         }
       },
       {
         "name": "Get Listings in Price Range",
         "request": {
           "method": "GET",
           "url": "http://localhost:8000/api/listings/",
           "query": [
             {"key": "price_min", "value": "100000000"},
             {"key": "price_max", "value": "200000000"},
             {"key": "city", "value": "San Francisco"}
           ]
         }
       }
     ]
   }
   ```

4. **Python Script**
   ```python
   import requests
   
   # Get all listings
   response = requests.get('http://localhost:8000/api/listings/')
   print(response.json())
   
   # Get filtered listings
   params = {
       'bedrooms': 3,
       'city': 'San Francisco',
       'ordering': '-price'
   }
   response = requests.get('http://localhost:8000/api/listings/', params=params)
   print(response.json())
   ```
5. **Django REST Framework Browsable API**
   - Visit `http://localhost:8000/api/listings/` in your browser
   - Use the built-in interface to test different filters and parameters
   - View the raw API response in JSON format

## Testing

### Running Tests
To run the test suite:

```bash
# Using Docker
docker-compose exec web python listings/manage.py test api

# Or locally (if you have Python and dependencies installed)
python listings/manage.py test api
```

### Test Coverage
The test suite includes comprehensive integration tests covering:

1. **Basic Endpoint Tests**
   - Get all listings
   - Get single listing
   - Get nonexistent listing (404 error)

2. **Filtering Tests**
   - By bedrooms
   - By city
   - By price range
   - By multiple criteria
   - By home type
   - By state
   - By zipcode
   - By tax year
   - By rent price range
   - By zestimate range

3. **Search Tests**
   - Search by address, city, state, or zipcode

4. **Ordering Tests**
   - By price (descending)
   - By year built

5. **Pagination Tests**
   - Basic pagination
   - Invalid page number
   - Invalid page size

6. **Combined Tests**
   - Filters with ordering
   - Multiple filters together

Each test case:
- Sets up test data with two sample listings
- Makes API requests with various parameters
- Verifies response status codes
- Checks response data structure and content
- Tests both successful and error cases

The test suite uses Django's test client and REST framework's test utilities to ensure reliable and maintainable tests.

### Available Scripts

The project includes several utility scripts located in the `scripts/` directory. These can be run within the Docker container using the following pattern:
```bash
docker-compose exec web ./scripts/<script_name>
```

#### Core Scripts
- **check**: Runs all code quality checks (linting, formatting, and type checking)
  ```bash
  docker-compose exec web ./scripts/check
  ```

- **lint**: Runs flake8 linting to check code style and find potential errors
  ```bash
  docker-compose exec web ./scripts/lint
  ```

- **type-check**: Runs mypy type checking to verify type annotations
  ```bash
  docker-compose exec web ./scripts/type-check
  ```

- **format**: Automatically formats code using black and isort
  ```bash
  docker-compose exec web ./scripts/format
  ```

#### Script Details

1. **check**
   - Combines lint and type-check scripts
   - Exits with non-zero status if any checks fail
   - Use this before committing code to ensure all quality checks pass

2. **lint**
   - Runs flake8 with project-specific configuration
   - Checks for PEP 8 compliance
   - Verifies maximum line length (88 characters)
   - Ensures proper import ordering

3. **type-check**
   - Runs mypy static type checker
   - Verifies type annotations are correct
   - Checks for type-related errors
   - Ensures type safety across the codebase

4. **format**
   - Runs black code formatter
   - Runs isort import sorter
   - Automatically fixes code style issues
   - Makes code consistent across the project

#### Best Practices
1. Run `./scripts/format` before committing changes to automatically fix style issues
2. Run `./scripts/check` to verify all checks pass before submitting code
3. If type checking fails, ensure all functions have proper type annotations
4. Use `./scripts/lint` to identify specific style issues that need fixing


