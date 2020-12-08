import sys
import logging
from accounts.models import ListUser, Token

logger = logging.getLogger(__name__)


class PasswordlessAuthenticationBackend(object):
    def authenticate(self, uid):
        logger.error(f'uid:{uid}')
        if not Token.objects.filter(uid=uid).exists():
            logger.error('no token  found')
            return None
        token = Token.objects.get(uid=uid)
        logger.error('got token')
        try:
            user = ListUser.objects.get(email=token.email)
            logger.error('got user')
            return user
        except ListUser.DoesNotExist:
            logger.error('new user')
            return ListUser.objects.create(email=token.email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)
