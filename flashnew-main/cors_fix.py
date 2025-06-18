#!/usr/bin/env python3
"""
CORS fix for API server
Add this to api_server_unified.py after the CORS middleware
"""

from fastapi import Request, Response

# Add this after the CORS middleware in api_server_unified.py

@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    """Handle CORS preflight requests"""
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, X-API-Key'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response

# Also update the CORS middleware to:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)