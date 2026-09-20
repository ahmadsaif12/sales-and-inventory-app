# InventoryMS

InventoryMS is a Django-based sales and inventory workspace for teams that need to manage products, purchase orders, sales, deliveries, invoices, bills, customers, vendors, and staff from one dashboard.

It provides a responsive operations dashboard, role-aware account tools, spreadsheet exports, and a PostgreSQL-ready deployment path while remaining simple to run locally with SQLite.

## Highlights

- Product catalogue with categories, stock levels, vendors, expiry dates, and search.
- Sales and purchase order workflows with inventory-aware transaction records.
- Delivery tracking for customer orders and fulfilment status.
- Invoice and bill management with Excel export support.
- Customer, vendor, staff, profile, and authentication management.
- Responsive dashboard UI with shared form, table, notification, and navigation styling.
- Login protection for operational pages and rate limiting on registration and login requests.

## Technology

| Area | Tools |
| --- | --- |
| Backend | Python 3.12, Django 5.1 |
| Database | SQLite for local development; PostgreSQL supported through `DATABASE_URL` |
| UI | Bootstrap 5, Font Awesome, crispy-bootstrap5 |
| Tables and exports | django-tables2, Tablib, OpenPyXL |
| Media and validation | django-imagekit, django-phonenumber-field |
| Deployment helpers | Docker Compose, Gunicorn, WhiteNoise |

## Project structure

```text
InventoryMS/        Project settings, root URLs, WSGI configuration
accounts/           Users, profiles, staff, customers, and vendors
store/              Dashboard, products, categories, and deliveries
transactions/       Sales, purchase orders, and transaction exports
invoice/            Customer invoices
bills/              Supplier and operational bills
static/             Shared CSS, JavaScript, and image assets
```

## Quick start

### Prerequisites

- Python 3.12 or newer
- `pip`
- PostgreSQL 16 and Docker Compose are optional for containerized development

### 1. Create an environment and install dependencies

```bash
git clone <your-repository-url>
cd Sales-Enventory-Management

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Configure environment variables

Create a `.env` file in the project root. SQLite is used automatically when `DATABASE_URL` is absent.

```dotenv
DEBUG=True
SECRET_KEY=replace-with-a-long-unique-development-secret
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: use PostgreSQL instead of SQLite
# DATABASE_URL=postgresql://username:password@localhost:5432/sales_inventory
```

For Docker Compose, also provide the PostgreSQL values used by the database service:

```dotenv
POSTGRES_DB=sales_inventory
POSTGRES_USER=postgres
POSTGRES_PASSWORD=choose-a-local-password
```

### 3. Prepare the database and run the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). The root URL redirects to the dashboard; sign in to access operational pages.

## Docker Compose

Docker Compose starts PostgreSQL and the Django web service. The container entrypoint applies migrations and collects static files before starting the application.

```bash
docker compose up --build
```

The application is available at [http://localhost:8000/](http://localhost:8000/). To stop the stack:

```bash
docker compose down
```

Use `docker compose down -v` only when you intentionally want to remove the local PostgreSQL volume and its data.

## Main areas and routes

| Area | Primary route | What it provides |
| --- | --- | --- |
| Dashboard | `/store/` | Stock, staff, delivery, sales, and chart summaries |
| Products | `/store/products/` | Product catalogue, search, CRUD actions, and exports |
| Categories | `/store/categories/` | Product category management |
| Deliveries | `/store/deliveries/` | Delivery records and fulfilment status |
| Sales | `/transactions/sales/` | Sales orders, receipts, and export |
| Purchases | `/transactions/purchases/` | Purchase orders and export |
| Invoices | `/invoice/invoices/` | Customer invoice lifecycle |
| Bills | `/bills/bills/` | Operational bill tracking |
| Accounts | `/accounts/` | Authentication, profiles, staff, customers, and vendors |

## Development commands

The included `Makefile` provides shortcuts for routine tasks:

```bash
make install       # Install Python dependencies
make migrate       # Apply migrations
make makemigrations
make run           # Start the Django development server
make test          # Run the test suite
make check         # Run Django system checks
make collectstatic # Build static files
make help          # Show every available target
```

The equivalent core Django commands are:

```bash
python manage.py test
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

## Testing

The test suite covers authentication boundaries, essential model behavior, transaction route availability, invoice totals, billing behavior, and the shared dashboard presentation layer.

```bash
python manage.py test
```

Run a single app while working on it:

```bash
python manage.py test store
python manage.py test transactions
```

## Production checklist

Before deployment:

1. Set `DEBUG=False`.
2. Use a strong, private `SECRET_KEY` supplied through the host environment.
3. Set `ALLOWED_HOSTS` to the production hostnames.
4. Configure a managed PostgreSQL database through `DATABASE_URL`.
5. Run `python manage.py migrate` and `python manage.py collectstatic --noinput`.
6. Serve the WSGI application with a production process manager, for example `gunicorn InventoryMS.wsgi:application`, behind HTTPS.

## Contributing

1. Create a focused branch for the change.
2. Keep migrations, forms, templates, and tests in sync when changing a model or user workflow.
3. Run `python manage.py test` and `python manage.py check` before opening a pull request.
4. Describe any user-facing changes and configuration requirements in the pull request.
