# Authentication Bypass for Development/Testing

## Overview

The FLASH API server now supports disabling authentication for development and testing purposes. This feature allows developers to access API endpoints without providing API keys or JWT tokens.

## ⚠️ WARNING

**NEVER use this feature in production!** The authentication bypass is only intended for development and testing environments.

## How to Enable

1. Ensure your environment is set to development:
   ```bash
   ENVIRONMENT=development
   ```

2. Set the `DISABLE_AUTH` environment variable to `true`:
   ```bash
   DISABLE_AUTH=true
   ```

3. You can set these in your `.env` file:
   ```env
   ENVIRONMENT=development
   DISABLE_AUTH=true
   ```

## What Happens When Enabled

When `DISABLE_AUTH=true` and `ENVIRONMENT=development`:

1. **API Key Authentication**: All API endpoints will accept requests without the `X-API-Key` header
2. **JWT Authentication**: All JWT-protected endpoints will work without a Bearer token
3. **User Context**: A default development user is provided with admin privileges:
   - Username: `development_user`
   - Email: `dev@flash.ai`
   - Roles: `["admin", "api_user", "developer"]`
   - Admin Access: Yes

## Usage Examples

### Without Authentication Bypass (Normal)
```bash
# Requires API key
curl -H "X-API-Key: your-api-key" http://localhost:8001/predict

# Or JWT token
curl -H "Authorization: Bearer your-jwt-token" http://localhost:8001/predict
```

### With Authentication Bypass (Development)
```bash
# No authentication headers needed!
curl http://localhost:8001/predict
```

## Security Checks

The system includes multiple safety checks:

1. **Environment Check**: Bypass only works when `ENVIRONMENT=development`
2. **Flag Check**: Must explicitly set `DISABLE_AUTH=true`
3. **Logging**: All bypassed authentication attempts are logged
4. **Production Safety**: In production, the system will reject the bypass even if enabled

## Configuration File Examples

### Development Configuration (.env.development)
```env
ENVIRONMENT=development
DISABLE_AUTH=true
API_PORT=8001
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Production Configuration (.env.production)
```env
ENVIRONMENT=production
DISABLE_AUTH=false  # Or remove this line entirely
API_KEYS=your-secure-api-keys
SECRET_KEY=your-secure-secret-key
```

## Testing the Bypass

1. Start the server with development configuration:
   ```bash
   cp .env.development .env
   python api_server_unified.py
   ```

2. Test an endpoint without authentication:
   ```bash
   curl http://localhost:8001/health
   ```

3. You should see a log message:
   ```
   Authentication disabled in development mode (DISABLE_AUTH=true)
   ```

## Affected Endpoints

All endpoints that use these authentication dependencies are affected:
- `get_current_user`
- `get_current_active_user`
- `get_current_user_flexible`
- `get_api_key`

This includes:
- `/predict`
- `/predict_enhanced`
- `/analyze`
- `/system_info`
- `/metrics`
- And all other protected endpoints

## Troubleshooting

If authentication bypass isn't working:

1. Check your environment variables:
   ```bash
   echo $ENVIRONMENT
   echo $DISABLE_AUTH
   ```

2. Verify the server logs show development mode
3. Ensure you're not accidentally in production mode
4. Check that both conditions are met: `ENVIRONMENT=development` AND `DISABLE_AUTH=true`

## Best Practices

1. **Use separate .env files**: Keep `.env.development` and `.env.production` separate
2. **Never commit**: Add `.env` to `.gitignore`
3. **CI/CD Safety**: Ensure your CI/CD pipeline doesn't accidentally use development settings
4. **Code Reviews**: Review any changes to authentication bypass logic carefully
5. **Monitoring**: Monitor logs for unexpected authentication bypasses

## Reverting to Normal Authentication

To re-enable authentication:

1. Set `DISABLE_AUTH=false` or remove the variable
2. Or set `ENVIRONMENT=production`
3. Restart the server

Authentication will be immediately enforced again.