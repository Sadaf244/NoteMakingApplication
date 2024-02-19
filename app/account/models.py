from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
import logging


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

    def authenticate(self, username_or_email, password):
        user = self.get_by_username_or_email(username_or_email)
        if user and user.check_password(password) and user.is_active:
            return user
        return None

    def get_by_username_or_email(self, username_or_email):
        try:
            return self.get(email=username_or_email, is_deleted=False) if '@' in username_or_email else self.get(
                username=username_or_email, is_deleted=False)
        except ObjectDoesNotExist:
            return None
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @staticmethod
    def is_user_exists(email, username):
        return User.objects.filter(email=email, username=username, is_deleted=False).exists()


    @staticmethod
    def get_user_token(user):
        try:
            token = Token.objects.get(user=user)
            token.delete()
        except ObjectDoesNotExist:
            token = Token.objects.create(user=user)
        except Exception as e:
            logging.error("Exception on get_user_token: %s", repr(e))
            token = None

        return token

    @staticmethod
    def get_user_object(user_id=None):
        user_object = None
        if user_id:
            try:
                user_object = User.objects.get(id=user_id)
            except Exception as e:
                logging.error('getting exception on get_user_object', repr(e))
        return user_object
class UserSignupValidation:
    def is_disposable_domain(self, email):
        return 'yopmail' in email.lower()

    def check_is_user_is_new_user(self, email, username):
        resp_dict = {'status': True, 'message': 'User does not exist in our system.'}

        if email and username:
            if User.is_user_exists(email, username):
                resp_dict.update({'status': False, 'message': 'User already registered. Please contact.'})
            elif self.is_disposable_domain(email):
                resp_dict.update({'status': False, 'message': 'Please provide a valid email address.'})
        else:
            resp_dict.update({'status': False, 'message': 'Please provide valid email address.'})

        return resp_dict

class UserOnBoard:
    def __init__(self, request):
        self.request = request

    def start_on_boarding(self):
        email_address = self.request.data.get('email_address', None)
        password = self.request.data.get('password', None)
        username = self.request.data.get('user_name', '')
        user_signup_validation = UserSignupValidation()
        resp_dict = user_signup_validation.check_is_user_is_new_user(email_address, username)
        user = None

        if resp_dict['status']:
            try:
                print("testing", username, email_address, password)
                user = User.objects.create_user(username=username, email=email_address, password=password)
                logging.info('User created: %s', user)
            except Exception as e:
                logging.error('Exception on UserOnBoard start_on_boarding: %s', repr(e))
                response_message = 'User already exists. Sign in again.'
                resp_dict.update({'status': False, 'message': response_message})

        return resp_dict, user