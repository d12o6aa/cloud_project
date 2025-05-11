import hashlib
import base64
from app.services.auth_service import AuthService

class SimpleAuthService(AuthService):
    def hash_password(self, password):
        return base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()

    def verify_password(self, plain, hashed):
        return self.hash_password(plain) == hashed

    def create_token(self, user_id):
        return f"token-{user_id}"
