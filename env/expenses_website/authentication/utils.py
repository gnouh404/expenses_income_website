from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> text_type:
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))
# đối tượng tạo token    
token_generator = AppTokenGenerator()    