# SQLTools Connection Settings for PostgreSQL

## Connection Configuration for SQLTools Extension

Use these settings in SQLTools to connect to the PostgreSQL database:

### Development Environment

**Connection Name:** `KnowEmployee Dev`

**Connection Settings:**
```json
{
  "name": "KnowEmployee Dev",
  "driver": "PostgreSQL",
  "server": "localhost",
  "port": 5433,
  "database": "knowemployee_db",
  "username": "knowemployee",
  "password": "knowemployee_password",
  "connectionTimeout": 10000,
  "requestTimeout": 30000,
  "ssl": false,
  "connectionMethod": "Standard"
}
```

### Important Settings:

1. **Host/Server:** `localhost` (or `127.0.0.1`)
2. **Port:** `5433` (development) or `5432` (production)
3. **Database:** `knowemployee_db`
4. **Username:** `knowemployee` (or from your `.env` file)
5. **Password:** `knowemployee_password` (or from your `.env` file)
6. **SSL:** Set to `false` (Docker PostgreSQL doesn't require SSL by default)
7. **Connection Timeout:** `10000` (10 seconds)
8. **Request Timeout:** `30000` (30 seconds)

### Common Issues and Solutions:

#### Issue: Connection timeout or "Connection refused"
**Solution:** 
- Make sure the PostgreSQL container is running: `docker ps | grep postgres`
- Verify the port is correct (5433 for dev)
- Check firewall settings

#### Issue: Authentication failed
**Solution:**
- Verify username and password match your `.env` file
- Default dev credentials: `knowemployee` / `knowemployee_password`

#### Issue: SSL/TLS error
**Solution:**
- Set `"ssl": false` in connection settings
- Or set `"ssl": { "rejectUnauthorized": false }` if SSL is required

#### Issue: Database doesn't exist
**Solution:**
- Verify database name: `knowemployee_db`
- Check that database was created: `docker exec knowemployee-postgres-dev psql -U knowemployee -l`

### Testing Connection from Command Line:

```bash
# Test connection
psql -h localhost -p 5433 -U knowemployee -d knowemployee_db -c "SELECT version();"
```

If this works, SQLTools should work with the same settings.

