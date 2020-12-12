from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()

class PssswordlessAuthenticationBackend:
    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None