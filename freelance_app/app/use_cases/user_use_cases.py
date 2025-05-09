from app.domain.interfaces import UserRepository
from app.domain.models import User
from app.services.auth_service import AuthService

class RegisterUser:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, user_data: dict) -> User:
        # تحقق إذا كان المستخدم موجودًا بالفعل
        existing_user = self.user_repo.get_by_email(user_data['email'])
        if existing_user:
            raise ValueError("User already exists")
        
        # هاش كلمة السر
        user_data['password'] = self.auth_service.hash_password(user_data['password'])

        # إنشاء المستخدم
        new_user = User(
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            role=user_data['role']
        )
        return self.user_repo.create(new_user)

class LoginUser:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def execute(self, email: str, password: str) -> User:
        # التحقق من وجود المستخدم
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        # التحقق من صحة كلمة السر
        if not self.auth_service.verify_password(password, user.password):
            raise ValueError("Invalid email or password")
        
        return user
