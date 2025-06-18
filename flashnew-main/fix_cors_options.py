#!/usr/bin/env python3
"""
Fix for CORS OPTIONS handling in the API
Add this to api_server_unified.py
"""

# Add this after the CORS middleware configuration

from fastapi import Response

# Generic OPTIONS handler for all endpoints
@app.options("/{full_path:path}")
async def options_handler(full_path: str, response: Response):
    """Handle OPTIONS requests for CORS preflight"""
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key, Authorization"
    response.headers["Access-Control-Max-Age"] = "3600"
    return {"message": "OK"}

# Also add specific OPTIONS handler for predict endpoint
@app.options("/predict")
async def predict_options(response: Response):
    """Handle OPTIONS request for /predict endpoint"""
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return {"message": "OK"}

print("""
To fix CORS in your API:

1. Add the above OPTIONS handlers to api_server_unified.py
2. Place them after the CORS middleware configuration
3. Restart the API server

This will properly handle preflight requests from the frontend.
""")