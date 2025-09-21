#!/usr/bin/env python3
"""
Database initialization script for Neon PostgreSQL
Run this once after setting up your Neon database on Vercel

Usage:
    python init_prod_db.py
    # OR
    python init_prod_db.py "postgresql://user:pass@host/db?sslmode=require"
"""

import os
import sys

try:
    import psycopg2
    PSYCOPG_VERSION = 2
except ImportError:
    try:
        import psycopg
        PSYCOPG_VERSION = 3
    except ImportError:
        print("❌ Neither psycopg2 nor psycopg is available!")
        print("Please install one of them:")
        print("  pip install psycopg2-binary")
        print("  OR")
        print("  pip install psycopg[binary]")
        sys.exit(1)


def init_production_db():
    """Initialize Neon PostgreSQL database for production"""
    
    # Get database URL from environment or command line
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found!")
        print("Please set your Neon PostgreSQL connection string:")
        print("export DATABASE_URL='postgresql://user:pass@host/db?sslmode=require'")
        print("\nOr run with: python init_prod_db.py 'your_neon_connection_string'")
        return False
    
    try:
        print("🔗 Connecting to Neon PostgreSQL database...")
        print(f"📡 Host: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'Hidden'}")
        conn = psycopg2.connect(database_url) if PSYCOPG_VERSION == 2 else psycopg.connect(database_url)
        cursor = conn.cursor()
        
        print("📋 Creating users table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
               id SERIAL PRIMARY KEY, 
               username VARCHAR(255) NOT NULL, 
               email VARCHAR(255) UNIQUE NOT NULL, 
               password VARCHAR(255) NOT NULL
            )
        ''')
        
        print("📋 Creating user_preferences table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                user_name VARCHAR(255) NOT NULL,
                role VARCHAR(255) NOT NULL,
                target_company VARCHAR(255) NOT NULL,
                position VARCHAR(255) NOT NULL,
                previous_skills TEXT NOT NULL,
                specialization VARCHAR(255) NOT NULL,
                skill_focus VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        print("📋 Creating test_results table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                user_name VARCHAR(255) NOT NULL,
                python_score INTEGER DEFAULT 0,
                cpp_score INTEGER DEFAULT 0,
                total_score INTEGER NOT NULL,
                percentage REAL NOT NULL,
                test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        print("📋 Creating user_roadmaps table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_roadmaps (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                roadmap_data TEXT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        print("✅ All tables created successfully!")
        
        # Test with a simple query
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"📊 Current users in database: {user_count}")
        
        conn.close()
        print("🎉 Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    # Allow DATABASE_URL to be passed as command line argument
    if len(sys.argv) > 1:
        os.environ['DATABASE_URL'] = sys.argv[1]
    
    success = init_production_db()
    sys.exit(0 if success else 1)