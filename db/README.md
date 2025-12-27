# Database Setup Guide

This project uses PostgreSQL for both development and production environments to ensure consistency.

## Quick Start

### Development Environment

1. **Set up environment variables** in your `.env` file:
   ```bash
   POSTGRES_USER=knowemployee
   POSTGRES_PASSWORD=knowemployee_password
   POSTGRES_DB=knowemployee_db
   POSTGRES_PORT=5433
   ```

2. **Start the services**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **Run database migrations**:
   ```bash
   docker exec -it knowemployee-app-dev flask db upgrade
   ```

### Production Environment

1. **Set up environment variables** in your `.env` file:
   ```bash
   POSTGRES_USER=knowemployee
   POSTGRES_PASSWORD=<strong_password_here>
   POSTGRES_DB=knowemployee_db
   POSTGRES_PORT=5432
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Run database migrations**:
   ```bash
   docker exec -it knowemployee-app flask db upgrade
   ```

## Database Connection

The application automatically constructs the PostgreSQL connection string from environment variables:
- `POSTGRES_HOST` - Database host (default: `postgres` in Docker)
- `POSTGRES_PORT` - Database port (default: `5432`)
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB` - Database name

Alternatively, you can set `SQLALCHEMY_DATABASE_URI` directly to override the automatic construction.

## Database Initialization

The `init.sql` script runs automatically when the PostgreSQL container is first created. It:
- Creates necessary PostgreSQL extensions (e.g., `uuid-ossp`)
- Sets up the database structure

**Note:** Tables are created by Flask-Migrate/Alembic migrations, not by the init script.

## Migrations

### Creating a new migration:
```bash
docker exec -it knowemployee-app-dev flask db migrate -m "Description of changes"
```

### Applying migrations:
```bash
docker exec -it knowemployee-app-dev flask db upgrade
```

### Rolling back:
```bash
docker exec -it knowemployee-app-dev flask db downgrade
```

## Data Persistence

Database data is stored in Docker volumes:
- **Development**: `postgres_data_dev`
- **Production**: `postgres_data`

To remove all data and start fresh:
```bash
# Development
docker-compose -f docker-compose.dev.yml down -v

# Production
docker-compose down -v
```

## Accessing the Database

### Using psql (from host):
```bash
# Development
docker exec -it knowemployee-postgres-dev psql -U knowemployee -d knowemployee_db

# Production
docker exec -it knowemployee-postgres psql -U knowemployee -d knowemployee_db
```

### Using connection string:
```bash
postgresql://knowemployee:knowemployee_password@localhost:5433/knowemployee_db
```

## Troubleshooting

### Database not ready
If you see connection errors, wait for the health check to pass:
```bash
docker-compose ps
```

### Reset database
```bash
# Stop containers
docker-compose -f docker-compose.dev.yml down

# Remove volume
docker volume rm knowemployee-new_postgres_data_dev

# Start again
docker-compose -f docker-compose.dev.yml up -d
```

### Check database logs
```bash
docker logs knowemployee-postgres-dev
```

## Migration from SQLite

If you're migrating from SQLite:

1. **Export SQLite data** (if needed):
   ```bash
   sqlite3 instance/service.db .dump > backup.sql
   ```

2. **Start PostgreSQL**:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d postgres
   ```

3. **Run migrations** to create tables:
   ```bash
   docker exec -it knowemployee-app-dev flask db upgrade
   ```

4. **Import data** (if needed, using custom scripts)

## Security Notes

- **Never commit** `.env` files with real passwords
- Use strong passwords in production
- Consider using Docker secrets or environment variable management tools for production
- The default credentials are for development only

