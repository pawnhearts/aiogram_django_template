# users/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
from users.models import User

pytestmark = pytest.mark.django_db

def test_user_creation():
    user = User.objects.create_user(username="testuser", email="test@example.com")
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_user_telegram_username_unique():
    user1 = User.objects.create_user(username="testuser1", email="test1@example.com", telegram_username="testusername")
    with pytest.raises(ValidationError):
        User.objects.create_user(username="testuser2", email="test2@example.com", telegram_username="testusername")

def test_user_telegram_id_unique():
    user1 = User.objects.create_user(username="testuser1", email="test1@example.com", telegram_id=12345)
    with pytest.raises(ValidationError):
        User.objects.create_user(username="testuser2", email="test2@example.com", telegram_id=12345)

def test_user_phone_number_unique():
    user1 = User.objects.create_user(username="testuser1", email="test1@example.com", phone_number="+1234567890")
    with pytest.raises(ValidationError):
        User.objects.create_user(username="testuser2", email="test2@example.com", phone_number="+1234567890")

def test_user_referral():
    user1 = User.objects.create_user(username="testuser1", email="test1@example.com")
    user2 = User.objects.create_user(username="testuser2", email="test2@example.com", referral=user1)
    assert user2.referral == user1

def test_user_str_representation():
    user = User.objects.create_user(username="testuser", email="test@example.com")
    assert str(user) == "testuser"