"""
Database configuration for different environments
"""
import os
from urllib.parse import urlparse

def get_database_config():
    """Get database configuration based on environment"""
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        # Parse DATABASE_URL (useful for Heroku or similar platforms)
        db_config = parse_database_url(db_url)
    else:
        # Use PostgreSQL if DATABASE_HOST is set, otherwise SQLite
        if os.getenv('DATABASE_HOST'):
            db_config = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DATABASE_NAME', 'postgres'),
                'USER': os.getenv('DATABASE_USER', 'postgres'),
                'PASSWORD': os.getenv('DATABASE_PASSWORD', ''),
                'HOST': os.getenv('DATABASE_HOST', 'localhost'),
                'PORT': os.getenv('DATABASE_PORT', '5432'),
            }
        else:
            # Default to SQLite
            from pathlib import Path
            BASE_DIR = Path(__file__).resolve().parent.parent
            db_config = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
    
    return {'default': db_config}

def parse_database_url(db_url):
    """Parse DATABASE_URL environment variable"""
    parsed = urlparse(db_url)
    
    if parsed.scheme == 'postgresql':
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed.path[1:],
            'USER': parsed.username,
            'PASSWORD': parsed.password,
            'HOST': parsed.hostname,
            'PORT': parsed.port or 5432,
        }
    elif parsed.scheme == 'sqlite':
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': parsed.path,
        }
    else:
        raise ValueError(f"Unsupported database scheme: {parsed.scheme}")
