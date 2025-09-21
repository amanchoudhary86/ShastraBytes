import os

import firebase_admin
from firebase_admin import credentials, firestore

from config import Config


# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        if Config.USE_FIREBASE:
            # Create credentials from environment variables
            cred_dict = {
                "type": "service_account",
                "project_id": Config.FIREBASE_PROJECT_ID,
                "private_key": Config.FIREBASE_PRIVATE_KEY,
                "client_email": Config.FIREBASE_CLIENT_EMAIL,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'projectId': Config.FIREBASE_PROJECT_ID
            })
        else:
            print("Firebase not configured - using local SQLite")
    
    return firestore.client() if Config.USE_FIREBASE else None

# Get Firestore client
def get_db():
    """Get Firestore database client"""
    try:
        if Config.USE_FIREBASE:
            return firestore.client()
        else:
            return None
    except Exception as e:
        print(f"Firebase connection error: {e}")
        return None

# Firestore helper functions
class FirebaseDB:
    def __init__(self):
        self.db = get_db()
    
    def create_user(self, user_data):
        """Create a new user in Firestore"""
        try:
            doc_ref = self.db.collection('users').document()
            user_data['created_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(user_data)
            return doc_ref.id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        try:
            users_ref = self.db.collection('users')
            query = users_ref.where('email', '==', email).limit(1)
            docs = query.get()
            
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            doc_ref = self.db.collection('users').document(user_id)
            doc = doc_ref.get()
            if doc.exists:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return user_data
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
    
    def create_user_preferences(self, user_id, preferences_data):
        """Create user preferences"""
        try:
            doc_ref = self.db.collection('user_preferences').document()
            preferences_data['user_id'] = user_id
            preferences_data['created_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(preferences_data)
            return doc_ref.id
        except Exception as e:
            print(f"Error creating user preferences: {e}")
            return None
    
    def get_user_preferences(self, user_id):
        """Get user preferences by user ID"""
        try:
            prefs_ref = self.db.collection('user_preferences')
            query = prefs_ref.where('user_id', '==', user_id).limit(1)
            docs = query.get()
            
            for doc in docs:
                prefs_data = doc.to_dict()
                prefs_data['id'] = doc.id
                return prefs_data
            return None
        except Exception as e:
            print(f"Error getting user preferences: {e}")
            return None