import json
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Firebase Configuration - Check if we're on Vercel
    if os.environ.get('VERCEL'):
        # On Vercel - use Firebase
        FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
        FIREBASE_PRIVATE_KEY = os.environ.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
        FIREBASE_CLIENT_EMAIL = os.environ.get('FIREBASE_CLIENT_EMAIL')
        USE_FIREBASE = True
        USE_SQLITE = False
    else:
        # Local development - can use SQLite or Firebase
        DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')
        USE_SQLITE = True
        USE_FIREBASE = False
    
    # Application settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Set DATABASE_URL for production
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_eCI7HuNS8gsZ@ep-bitter-surf-adwhxu0u-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'


