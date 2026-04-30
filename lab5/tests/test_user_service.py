"""Unit tests for User service."""
import pytest
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService

@pytest.fixture
def user_setup():
    repo = UserRepository()
    return UserService(repo), repo

@pytest.mark.parametrize("age, expected_success", [
    (13, True), (14, True), (99, True), (12, False), (0, False), (-5, False)
])
def test_registration_age_boundaries(user_setup, age, expected_success):
    service, _ = user_setup
    if expected_success:
        assert service.register_user(1, f"test{age}@mail.com", age).age == age
    else:
        with pytest.raises(ValueError):
            service.register_user(1, "fail@mail.com", age)

@pytest.mark.parametrize("email1, email2, should_fail", [
    ("test@mail.com", "test@mail.com", True),
    ("user1@mail.com", "user2@mail.com", False),
    ("ADMIN@mail.com", "ADMIN@mail.com", True),
    ("a@b.c", "d@e.f", False)
])
def test_registration_email_uniqueness(user_setup, email1, email2, should_fail):
    service, _ = user_setup
    service.register_user(1, email1, 20)
    if should_fail:
        with pytest.raises(ValueError):
            service.register_user(2, email2, 20)
    else:
        assert service.register_user(2, email2, 20).email == email2