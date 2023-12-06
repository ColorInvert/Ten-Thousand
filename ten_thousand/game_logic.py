#
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

            elif dice == (1, 1, 1, 1):
                score = 2000

            elif dice == (5, 5, 5, 5):
                score = 1000

            elif dice == (1, 1, 1, 1, 1):
                score = 3000

            elif dice == (5, 5, 5, 5, 5):
                score = 1500

            elif dice == (5, 5, 5, 5, 5, 5):
                score = 2000

            elif dice == (2, 2, 3, 3, 6, 6):
                score = 1500

            # Add score for two ones
            if dice_counts[0] == 2:
                score += 200

        return score

    @staticmethod
    def roll_dice(num_dice):
        return tuple(random.randint(1, 6) for _ in range(num_dice))

    @staticmethod
    def display_tuple(tuple):
        output = " "
        for i in tuple:
            output = output + str(i)
            output = output + " "
        return output

    # TODO: Do an elimination passover comparing hold request against available, and if hold request can match/eliminate itself fully from available, then the hold request is valid.
    @staticmethod
    def check_cheating(hold_request, available):
        pass

    @staticmethod
    def startup_prompt():
        print(f"Welcome to Ten Thousand")
        print(f"(y)es to play or (n)o to decline")
        response = input("> ")

        if response == "n":
            print(f"OK. Maybe another time")
            exit()

    @staticmethod
    def play_game():
        round_count = 1
        die_count = 6
        response = ""
        total_score = 0
        hand_score = 0
        held_dice = []
        playing = True
        cheater = False

        # ?Main loop
        while playing == True:
            # Round begins
            this_roll = GameLogic.roll_dice(die_count)
            print(f"Starting round {round_count}\nRolling {die_count}...")
            print(f"***{GameLogic.display_tuple(this_roll)}***")
            print(f"Enter dice to keep, or (q)uit:")

            response = input("> ")

            if response == "q":
                print(f"Thanks for playing. You earned {total_score} points")
                exit()

            # if GameLogic.check_cheating(response, this_roll) == True:
            #     cheater = True
            #     print("Cheater! or maybe you mistyped something?")

            # Convert response to list of string-digits, then convert those string digits to ints.
            held_dice = [*response]
            held_dice = list(map(int, held_dice))

            # Remove the number of dice taken from the die count.
            die_count -= len(held_dice)

            # Calculate this hand's score from the dice currently held
            hand_score = GameLogic.calculate_score(held_dice)

            print(
                f"You have {hand_score} unbanked points and {die_count} dice remaining"
            )

            print("(r)oll again, (b)ank your points or (q)uit:")
            response = input("> ")

            if response == "q":
                print(f"Thanks for playing. You earned {total_score} points")
                exit()

            # None of the provided sim files ever press r at this point, so it remains unimplemented for version 2.
            if response == "r":
                print("Not implemented!")
                response = "b"

            if response == "b":
                print(f"You banked {hand_score} points in round {round_count}")

                # update total score, reset unbanked points, increment round, reset die count.
                total_score += hand_score
                hand_score = 0
                round_count += 1
                die_count = 6

                print(f"Total score is {total_score} points")


GameLogic.startup_prompt()
GameLogic.play_game()
