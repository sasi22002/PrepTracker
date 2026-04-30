import sqlite3
import bcrypt
import os

class AuthDB:
    """Database handler for authentication data"""
    
    def __init__(self, db_path='prod.sqlite3'):
        self.db_path = db_path
        self.init_auth_table()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_auth_table(self):
        """Initialize authentication table if it doesn't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                pin_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize PIN if not exists
        self.init_pin()
    
    def init_pin(self):
        """Initialize PIN in database if not exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if PIN already exists
        cursor.execute('SELECT pin_hash, salt FROM auth_config WHERE id = 1')
        result = cursor.fetchone()
        
        if not result:
            # Generate salt and hash PIN
            salt = bcrypt.gensalt()
            pin_hash = bcrypt.hashpw(b'269900', salt)
            
            # Insert hashed PIN
            cursor.execute('''
                INSERT INTO auth_config (id, pin_hash, salt)
                VALUES (1, ?, ?)
            ''', (pin_hash.decode('utf-8'), salt.decode('utf-8')))
            
            conn.commit()
            print("PIN initialized in database")
        else:
            print("PIN already exists in database")
        
        conn.close()
    
    def verify_pin(self, input_pin):
        """Verify input PIN against database hash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT pin_hash, salt FROM auth_config WHERE id = 1')
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        stored_hash, salt = result
        try:
            # Convert stored hash back to bytes
            stored_hash_bytes = stored_hash.encode('utf-8')
            input_bytes = input_pin.encode('utf-8')
            
            # Verify PIN
            return bcrypt.checkpw(input_bytes, stored_hash_bytes)
        except Exception as e:
            print(f"Error verifying PIN: {e}")
            return False
    
    def update_pin(self, new_pin):
        """Update PIN in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate new salt and hash
        salt = bcrypt.gensalt()
        pin_hash = bcrypt.hashpw(new_pin.encode('utf-8'), salt)
        
        # Update PIN
        cursor.execute('''
            UPDATE auth_config 
            SET pin_hash = ?, salt = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (pin_hash.decode('utf-8'), salt.decode('utf-8')))
        
        conn.commit()
        conn.close()
        print("PIN updated in database")

# Initialize auth database
auth_db = AuthDB()
