from unittest.mock import patch, call
from unittest.mock import patch, call
from django.test import TestCase

import accounts
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={'email': 'healblue@example.com'})
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_send_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={'email': 'healblue@example.com'})
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['healblue@example.com'])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email',
                                data={'email': 'healblue@example.com'}, follow=True)
        expected = "Check your email, we've sent you a link you can use to log in."
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, expected)
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email', data={'email': 'healblue@example.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'healblue@example.com')


    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={'email': 'healblue@example.com'})
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)


class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    @patch('accounts.views.auth')
    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?uid=abcd1234')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd1234')
        )

    @patch('accounts.views.auth')
    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?uid=abcd1234')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )


