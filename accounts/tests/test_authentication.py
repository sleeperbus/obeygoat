from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PssswordlessAuthenticationBackend

from accounts.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):
    def test_returns_None_if_no_such_token(self):
        result = PssswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        email = 'a@b.com'
        token = Token.objects.create(email=email)
        user = PssswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        email = 'a@b.com'
        token = Token.objects.create(email=email)
        existing_user = User.objects.create(email=email)
        user = PssswordlessAuthenticationBackend().authenticate(uid=token.uid)
        self.assertEqual(existing_user, user)


class GetUserTest(TestCase):
    def test_gets_user_by_email(self):
        User.objects.create(email='extra@b.com')
        desired_user = User.objects.create(email='a@b.com')
        found_user = PssswordlessAuthenticationBackend().get_user(email='a@b.com')
        self.assertEqual(desired_user, found_user)

    def test_return_None_if_no_user_with_that_email(self):
        self.assertIsNone(PssswordlessAuthenticationBackend().get_user('a@b.com'))