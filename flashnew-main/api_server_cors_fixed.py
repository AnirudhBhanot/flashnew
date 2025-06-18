#!/usr/bin/env python3
"""
Temporary API server with CORS fully open for development
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from api_server_unified import *
from fastapi.middleware.cors import CORSMiddleware

# Remove existing CORS middleware
for i, middleware in enumerate(app.user_middleware):
    if middleware.cls == CORSMiddleware:
        app.user_middleware.pop(i)
        break

# Add completely open CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
    max_age=3600,
)

print("⚠️  WARNING: CORS is fully open - development only!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
