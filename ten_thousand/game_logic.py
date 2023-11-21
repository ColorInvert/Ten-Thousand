
#! IMPORTANT: Version one of the scoring system for this program was written through CHATGPT3.5 prompt engineering. Full list of commands given is included in prompt.md, as well as reasoning for this approach.
import random


class GameLogic:
    @staticmethod
    def calculate_score(dice):
        score = 0

        if len(dice) == 1:
            if dice[0] == 5:
                score += 50
            elif dice[0] == 1:
                score += 100
        elif len(dice) == 2 and sorted(dice) == [1, 5]:
            score += 150
        elif len(dice) == 2 and all(d == 5 for d in dice):
            score += 100
        else:
            dice_counts = [dice.count(i) for i in range(1, 7)]

            for i in range(1, 7):
                if dice_counts[i - 1] >= 3:
                    if i == 1:
                        score += 1000
                    else:
                        score += i * 100

                    remaining = dice_counts[i - 1] - 3
                    if remaining > 0:
                        if i == 1:
                            score += remaining * 100
                        elif i == 5:
                            # Change score value for a combination of 1 and 5
                            score += remaining * 50  # Change to 150

                        else:
                            score += remaining * i * 100

            if all(count == 1 for count in dice_counts):
                score += 150

            if dice_counts[0] == 3 and dice_counts[4] == 1:
                # Change score value for three ones and a five
                score = 1000 + 50  # Change to 1000 + 100

            if sorted(dice) == [1, 2, 3, 4, 5, 6]:
                score = 1500
            elif dice == (1, 1, 1, 1, 1, 1):
                score = 4000
            
            # Add score for two ones
            if dice_counts[0] == 2:
                score += 200

        return score

    @staticmethod
    def roll_dice(num_dice):
        return tuple(random.randint(1, 6) for _ in range(num_dice))
