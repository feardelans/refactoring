import pytest
from yahtzee import Yahtzee

def test_chance():
    assert Yahtzee.chance(1, 2, 3, 4, 5) == 15


def test_yahtzee_success():
    assert Yahtzee.yahtzee([6, 6, 6, 6, 6]) == 50


def test_yahtzee_fail():
    assert Yahtzee.yahtzee([6, 6, 6, 6, 5]) == 0


def test_ones():
    assert Yahtzee.ones(1, 1, 2, 3, 4) == 2


def test_twos():
    assert Yahtzee.twos(2, 2, 3, 4, 5) == 4


def test_threes():
    assert Yahtzee.threes(3, 3, 3, 4, 5) == 9

def test_fours():
    game = Yahtzee(4, 4, 2, 1, 6)
    assert game.fours() == 8


def test_fives():
    game = Yahtzee(5, 5, 5, 2, 1)
    assert game.fives() == 15


def test_sixes():
    game = Yahtzee(6, 6, 6, 1, 2)
    assert game.sixes() == 18

def test_score_pair():
    assert Yahtzee.score_pair(3, 3, 4, 5, 6) == 6


def test_two_pair():
    assert Yahtzee.two_pair(3, 3, 5, 5, 6) == 16


def test_three_of_a_kind():
    assert Yahtzee.three_of_a_kind(2, 2, 2, 4, 5) == 6


def test_four_of_a_kind():
    assert Yahtzee.four_of_a_kind(4, 4, 4, 4, 1) == 16


def test_small_straight():
    assert Yahtzee.smallStraight(1, 2, 3, 4, 5) == 15


def test_full_house():
    assert Yahtzee.fullHouse(2, 2, 3, 3, 3) == 13