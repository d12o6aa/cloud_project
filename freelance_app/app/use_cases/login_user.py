from app.domain.interfaces import UserRepository, AuthService

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass

class LoginUser:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, email, password):
        user = self.user_repo.get_by_email(email)
        if user is None:
            raise ValueError("User not found")
        if not self.auth_service.verify_password(password, user.password):
            raise AuthenticationError("Invalid credentials")
        
        # This block is redundant and removed as the specific AuthenticationError is already raised above.
        
        return user
