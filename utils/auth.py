import sqlite3
import bcrypt
from cryptography.fernet import Fernet
import os

# --- Constants ---
DB_PATH = "users.db"
KEY_PATH = "secret.key"

# --- Key Management ---
def load_or_create_key():
    """Loads the encryption key from KEY_PATH or creates it if it doesn't exist."""
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as key_file:
            key_file.write(key)
        return key

KEY = load_or_create_key()
CIPHER_SUITE = Fernet(KEY)

# --- Database Setup ---
def setup_database():
    """Initializes the database and creates/alters the users table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key_encrypted BLOB
        )
    """)
    # Add new columns for Vbee credentials, ignoring errors if they already exist
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN vbee_token_encrypted BLOB")
    except sqlite3.OperationalError:
        pass # Column likely already exists
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN vbee_app_id_encrypted BLOB")
    except sqlite3.OperationalError:
        pass # Column likely already exists

    conn.commit()
    conn.close()

# --- User and Password Management ---
def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash, provided_password):
    """Verifies a provided password against a stored hash."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

def add_user(username, password):
    """Adds a new user to the database. Returns True on success, False if user exists."""
    if get_user(username):
        return False  # User already exists
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Should be caught by get_user, but as a safeguard
    finally:
        conn.close()

def get_user(username):
    """Retrieves a user's data from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user(username, password):
    """Verifies a user's credentials. Returns True if valid, False otherwise."""
    user = get_user(username)
    if user:
        password_hash = user[2]
        return verify_password(password_hash, password)
    return False

# --- API Key & Credentials Management ---
def encrypt_value(value):
    """Encrypts a string value."""
    return CIPHER_SUITE.encrypt(value.encode('utf-8'))

def decrypt_value(encrypted_value):
    """Decrypts an encrypted value. Returns None if decryption fails."""
    if not encrypted_value:
        return None
    try:
        return CIPHER_SUITE.decrypt(encrypted_value).decode('utf-8')
    except Exception:
        return None

def save_api_key(username, api_key):
    """Encrypts and saves a user's Gemini API key to the database."""
    encrypted_key = encrypt_value(api_key)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET api_key_encrypted = ? WHERE username = ?",
        (encrypted_key, username)
    )
    conn.commit()
    conn.close()

def get_api_key(username):
    """Retrieves and decrypts a user's Gemini API key."""
    user = get_user(username)
    if user and len(user) > 3 and user[3]:
        return decrypt_value(user[3])
    return None

def save_vbee_credentials(username, token, app_id):
    """Encrypts and saves a user's Vbee credentials to the database."""
    encrypted_token = encrypt_value(token) if token else None
    encrypted_app_id = encrypt_value(app_id) if app_id else None
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET vbee_token_encrypted = ?, vbee_app_id_encrypted = ? WHERE username = ?",
        (encrypted_token, encrypted_app_id, username)
    )
    conn.commit()
    conn.close()

def get_vbee_credentials(username):
    """Retrieves and decrypts a user's Vbee credentials."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT vbee_token_encrypted, vbee_app_id_encrypted FROM users WHERE username = ?", (username,))
    creds = cursor.fetchone()
    conn.close()
    
    if creds:
        token = decrypt_value(creds[0]) if creds[0] else None
        app_id = decrypt_value(creds[1]) if creds[1] else None
        return token, app_id
    return None, None

# --- Initial Setup ---
# Ensure the database is ready when the module is imported
setup_database()
