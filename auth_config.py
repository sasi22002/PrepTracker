# This file is deprecated - use auth_db.py for database-based authentication
# Keeping this file for backward compatibility only

class AuthConfig:
    """Deprecated: Use auth_db.py instead"""
    
    def __init__(self):
        raise NotImplementedError("Use auth_db.py for database-based authentication")

# Initialize auth database
from auth_db import auth_db
