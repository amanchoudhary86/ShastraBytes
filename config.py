import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the Flask application"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - Check if we're on Vercel
    if os.environ.get('VERCEL'):
        # On Vercel - use Neon PostgreSQL connection string
        DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')
        USE_SQLITE = False
        
        # Neon-specific optimizations
        DATABASE_POOL_SIZE = int(os.environ.get('DATABASE_POOL_SIZE', '5'))
        DATABASE_MAX_OVERFLOW = int(os.environ.get('DATABASE_MAX_OVERFLOW', '10'))
    else:
        # Local development - use SQLite
        DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')
        USE_SQLITE = True
    
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


