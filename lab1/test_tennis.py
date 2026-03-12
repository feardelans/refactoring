import pytest
from tennis import TennisGame

def create_game():
    return TennisGame("player1", "player2")

def test_love_all():
    game = create_game()
    assert game.score() == "Love-All"

def test_fifteen_love():
    game = create_game()
    game.won_point("player1")
    assert game.score() == "Fifteen-Love"

def test_love_fifteen():
    game = create_game()
    game.won_point("player2")
    assert game.score() == "Love-Fifteen"

def test_thirty_all():
    game = create_game()
    game.won_point("player1")
    game.won_point("player1")
    game.won_point("player2")
    game.won_point("player2")
    assert game.score() == "Thirty-All"

def test_forty_thirty():
    game = create_game()
    for _ in range(3):
        game.won_point("player1")
    for _ in range(2):
        game.won_point("player2")
    assert game.score() == "Forty-Thirty"

def test_deuce():
    game = create_game()
    for _ in range(4):
        game.won_point("player1")
        game.won_point("player2")
    assert game.score() == "Deuce"

def test_advantage_player1():
    game = create_game()
    for _ in range(3):
        game.won_point("player1")
        game.won_point("player2")
    game.won_point("player1")
    assert game.score() == "Advantage player1"

def test_advantage_player2():
    game = create_game()
    for _ in range(3):
        game.won_point("player1")
        game.won_point("player2")
    game.won_point("player2")
    assert game.score() == "Advantage player2"

def test_win_player1():
    game = create_game()
    for _ in range(4):
        game.won_point("player1")
    assert "Win for player1" in game.score()

def test_win_player2():
    game = create_game()
    for _ in range(4):
        game.won_point("player2")
    assert "Win for player2" in game.score()
