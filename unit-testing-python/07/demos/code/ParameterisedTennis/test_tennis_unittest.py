import unittest

from tennis import score_tennis


class TennisTest(unittest.TestCase):

    def test_score_tennis(self):
        test_cases = [
            (0, 0, "Love-All"),
            (1, 1, "Fifteen-All"),
            (2, 2, "Thirty-All"),
            (2, 1, "Thirty-Fifteen"),
            (3, 1, "Forty-Fifteen"),
            (4, 1, "Win for Player 1"),
        ]
        for player1_points, player2_points, expected_score in test_cases:
            with self.subTest(f"{player1_points}, {player2_points} -> {expected_score}"):
                self.assertEqual(expected_score, score_tennis(player1_points, player2_points))


