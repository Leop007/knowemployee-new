# Microsoft OAuth Setup for Development Environments

This guide explains how to set up Microsoft OAuth authentication for local development environments that don't have a public domain.

## The Problem

Microsoft requires domain verification by accessing:
```
https://yourdomain.com/.well-known/microsoft-identity-association.json
```

Local development environments (localhost) don't have a public domain, so Microsoft can't verify the domain.

## Solutions

### Option 1: Use a Tunneling Service (Recommended for Testing)

Use a service like **ngrok** to expose your local server with a public HTTPS URL.

#### Setup with ngrok:

1. **Install ngrok**:
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/download
   ```

2. **Start your local server**:
   ```bash
   # Your app should be running on localhost:8001 (or your dev port)
   docker-compose -f docker-compose.dev.yml up
   ```

3. **Create an ngrok tunnel**:
   ```bash
   ngrok http 8001
   ```

4. **Get your public URL**:
   - ngrok will provide a URL like: `https://abc123.ngrok.io`
   - This URL is publicly accessible and uses HTTPS

5. **Update your Azure App Registration**:
   - Go to Azure Portal → App registrations → Your app
   - Add redirect URI: `https://abc123.ngrok.io/auth/microsoft/callback`
   - Update the domain verification file to be accessible at:
     `https://abc123.ngrok.io/.well-known/microsoft-identity-association.json`

6. **Update your .env.dev**:
   ```env
   DOMAIN=https://abc123.ngrok.io
   MICROSOFT_CLIENT_ID=your_client_id
   MICROSOFT_CLIENT_SECRET=your_client_secret
   ```

7. **Restart your application**

**Note**: Free ngrok URLs change each time you restart ngrok. For a stable URL, use ngrok's paid plan or set up a custom domain.

#### Alternative Tunneling Services:
- **Cloudflare Tunnel** (free, stable URLs)
- **localtunnel** (free, but URLs change)
- **serveo** (SSH-based, free)

### Option 2: Skip Domain Verification (Development Only)

For local development, you can skip domain verification if Microsoft allows it:

1. **In Azure App Registration**:
   - Go to "Branding & properties"
   - You may be able to skip publisher domain verification for development
   - Some Microsoft app types allow this

2. **Use a separate development app registration**:
   - Create a separate Azure App Registration for development
   - This app doesn't require domain verification
   - Use different `MICROSOFT_CLIENT_ID` and `MICROSOFT_CLIENT_SECRET` in `.env.dev`

### Option 3: Use a Development Domain

If you have access to a development subdomain:

1. **Set up DNS**:
   - Point `dev.knowemployee.com` to your development server
   - Or use a subdomain you control

2. **Set up SSL**:
   - Use Let's Encrypt or a development certificate
   - Ensure HTTPS is working

3. **Update Azure**:
   - Add the development domain to your app registration
   - Complete domain verification for the dev domain

4. **Update .env.dev**:
   ```env
   DOMAIN=https://dev.knowemployee.com
   ```

### Option 4: Use Microsoft Personal Accounts (Development)

For testing with personal Microsoft accounts:

1. **Use the `/common` endpoint** (already configured):
   - The app uses `https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration`
   - This supports both work/school and personal accounts

2. **Domain verification may not be required**:
   - Personal account logins might not require domain verification
   - Test if OAuth works without verification

## Current Implementation

The application already includes:

1. **Route for Microsoft identity association file**:
   - `/.well-known/microsoft-identity-association.json`
   - Serves the file from `static/.well-known/microsoft-identity-association.json`
   - Works in both development and production

2. **Environment-aware configuration**:
   - Development mode: `FLASK_ENV=development`
   - Production mode: `FLASK_ENV=production`
   - The route works in both environments

## Quick Start for Local Development

### Using ngrok (Easiest):

```bash
# 1. Start your app
docker-compose -f docker-compose.dev.yml up

# 2. In another terminal, start ngrok
ngrok http 8001

# 3. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)

# 4. Update .env.dev
echo "DOMAIN=https://abc123.ngrok.io" >> .env.dev

# 5. Update Azure redirect URI to: https://abc123.ngrok.io/auth/microsoft/callback

# 6. Restart your app
docker-compose -f docker-compose.dev.yml restart
```

### Testing the Verification File:

Once your app is accessible via the public URL:

```bash
# Test if the file is accessible
curl https://your-ngrok-url.ngrok.io/.well-known/microsoft-identity-association.json

# Should return:
# {
#   "associatedApplications": [
#     {
#       "applicationId": "your-client-id"
#     }
#   ]
# }
```

## Troubleshooting

### "Unable to connect to https://..."

- **Check if the URL is accessible**: Try accessing it in a browser
- **Check HTTPS**: Microsoft requires HTTPS (not HTTP)
- **Check file content**: Ensure the JSON file contains your actual `applicationId`
- **Check CORS**: The file should be publicly accessible (no authentication)

### OAuth Works But Domain Verification Fails

- Domain verification is **optional** for some app types
- OAuth login may still work without domain verification
- Check Azure portal for warnings (they may be non-blocking)

### ngrok URL Changes

- Free ngrok URLs change on restart
- Update Azure redirect URI each time
- Or use ngrok's paid plan for stable URLs
- Or use Cloudflare Tunnel (free, stable)

## Production vs Development

| Aspect | Development | Production |
|--------|-------------|------------|
| Domain | localhost or ngrok URL | knowemployee.com |
| HTTPS | ngrok provides it | Let's Encrypt |
| Domain Verification | Optional (may skip) | Required |
| Redirect URI | ngrok URL | Production domain |

## Additional Resources

- [Microsoft Identity Platform Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [ngrok Documentation](https://ngrok.com/docs)
- [Azure App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

