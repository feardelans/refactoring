from collections import Counter


NUMBER_OF_DICE = 5
MAX_DIE_VALUE = 6
YAHTZEE_SCORE = 50
SMALL_STRAIGHT_SCORE = 15
LARGE_STRAIGHT_SCORE = 20


class Yahtzee:

    def __init__(self, d1, d2, d3, d4, d5):
        self.dice = [d1, d2, d3, d4, d5]


    def _counts(self):
        return Counter(self.dice)

    def _sum_of_number(self, number):
        return sum(die for die in self.dice if die == number)

    def chance(self):
        return sum(self.dice)

    def yahtzee(self):
        counts = self._counts()
        return YAHTZEE_SCORE if 5 in counts.values() else 0

    def ones(self):
        return self._sum_of_number(1)

    def twos(self):
        return self._sum_of_number(2)

    def threes(self):
        return self._sum_of_number(3)

    def fours(self):
        return self._sum_of_number(4)

    def fives(self):
        return self._sum_of_number(5)

    def sixes(self):
        return self._sum_of_number(6)

    def score_pair(self):
        counts = self._counts()
        for number in range(MAX_DIE_VALUE, 0, -1):
            if counts[number] >= 2:
                return number * 2
        return 0

    def two_pair(self):
        counts = self._counts()
        pairs = [number for number in range(1, MAX_DIE_VALUE + 1)
                 if counts[number] >= 2]

        if len(pairs) >= 2:
            highest_two = sorted(pairs, reverse=True)[:2]
            return sum(number * 2 for number in highest_two)

        return 0

    def three_of_a_kind(self):
        counts = self._counts()
        for number in range(MAX_DIE_VALUE, 0, -1):
            if counts[number] >= 3:
                return number * 3
        return 0

    def four_of_a_kind(self):
        counts = self._counts()
        for number in range(MAX_DIE_VALUE, 0, -1):
            if counts[number] >= 4:
                return number * 4
        return 0

    def small_straight(self):
        return SMALL_STRAIGHT_SCORE if sorted(self.dice) == [1, 2, 3, 4, 5] else 0

    def large_straight(self):
        return LARGE_STRAIGHT_SCORE if sorted(self.dice) == [2, 3, 4, 5, 6] else 0

    def full_house(self):
        counts = self._counts()
        if sorted(counts.values()) == [2, 3]:
            return sum(self.dice)
        return 0