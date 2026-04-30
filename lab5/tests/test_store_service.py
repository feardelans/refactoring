"""Unit tests for Store service."""
import pytest
from src.repositories.game_repository import GameRepository
from src.repositories.user_repository import UserRepository
from src.services.store_service import StoreService
from src.services.user_service import UserService

@pytest.fixture
def store_setup():
    g, u = GameRepository(), UserRepository()
    return StoreService(g, u), UserService(u), u

@pytest.mark.parametrize("query, expected_count", [
    ("Witcher", 1), ("witcher", 1), ("WITCHER", 1), ("craft", 1),
    ("The", 2), ("e", 4), ("GTA 6", 0), ("", 5), ("   ", 5)
])
def test_search_games(store_setup, query, expected_count):
    service, _, _ = store_setup
    assert len(service.search_games(query)) == expected_count

def test_add_game_success(store_setup):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    assert service.add_to_library(1, 1) is True

@pytest.mark.parametrize("u_id, g_id", [(99, 1), (1, 99), (99, 99)])
def test_add_game_exceptions(store_setup, u_id, g_id):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    with pytest.raises(ValueError):
        service.add_to_library(u_id, g_id)

def test_add_game_duplicate(store_setup):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    service.add_to_library(1, 1)
    with pytest.raises(ValueError):
        service.add_to_library(1, 1)

def test_wishlist_flow(store_setup):
    service, u_service, u_repo = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    service.add_to_wishlist(1, 1)
    assert 1 in u_repo.find_by_id(1).wishlist
    service.add_to_library(1, 1)
    assert 1 not in u_repo.find_by_id(1).wishlist

@pytest.mark.parametrize("action", ["add_to_library", "add_to_wishlist"])
def test_wishlist_logic(store_setup, action):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    if action == "add_to_library": service.add_to_library(1, 1)
    else: service.add_to_wishlist(1, 1)
    with pytest.raises(ValueError):
        service.add_to_wishlist(1, 1)

def test_refund_success(store_setup):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    service.add_to_library(1, 1)
    assert service.refund_game(1, 1) is True

@pytest.mark.parametrize("u_id, g_id", [(1, 2), (99, 1)])
def test_refund_exceptions(store_setup, u_id, g_id):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    with pytest.raises(ValueError):
        service.refund_game(u_id, g_id)

@pytest.mark.parametrize("rating, valid", [(1, True), (5, True), (10, True), (0, False), (-1, False), (11, False), (99, False)])
def test_reviews(store_setup, rating, valid):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    service.add_to_library(1, 1)
    if valid: assert service.leave_review(1, 1, rating, "Test").rating == rating
    else:
        with pytest.raises(ValueError):
            service.leave_review(1, 1, rating, "Test")

@pytest.mark.parametrize("u_id, g_id", [(2, 1), (1, 2)])
def test_review_access(store_setup, u_id, g_id):
    service, u_service, _ = store_setup
    u_service.register_user(1, "test@mail.com", 20)
    with pytest.raises(ValueError):
        service.leave_review(u_id, g_id, 10, "Test")