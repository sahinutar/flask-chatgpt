import os
import secrets

class Config:
    SECRET_KEY = secrets.token_hex(32)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'youropenaiapikey'