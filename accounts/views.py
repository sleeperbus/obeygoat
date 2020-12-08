import sys
import logging
import uuid
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

from accounts.models import Token

logger = logging.getLogger(__name__)


def send_login_email(request):
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    logger.error(f'savaing uid: {uid}, for email: {email}')
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Superlists',
        f'Use this link to login:\n\n{url}',
        'noreply@superlists',
        [email],
    )
    return render(request, 'login_email_sent.html')


def login(request):
    logger.error('login view')
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')