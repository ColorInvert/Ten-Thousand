#
#! IMPORTANT: Version one of the scoring system for this program was written through CHATGPT3.5 prompt engineering. Full list of commands given is included in prompt.md, as well as reasoning for this approach.
import random
import time


class GameLogic:
    #!Partially ChatGPT written code below
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

    #!End of partially chatGPT written code

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

    @staticmethod
    def check_cheating(raw_hold_request, tup_available):
        available = list(tup_available)

        matched_hold = []

        # ?Thanks to geeksforgeeks.org's "Python | Convert number to list of integers" for this list comprehension line of code.
        try:
            hold_request = [int(x) for x in str(raw_hold_request)]
        except:
            print(
                "You need to provide the values on the dice you want to hold, no spaces or letters."
            )
            return True

        # Loop through the hold request list submitted by the user
        for i in hold_request:
            if i in available:
                matched_hold.append(i)
                available.remove(i)

        # print(f"the value of matched_hold is {matched_hold} and the value of hold_request is {hold_request}")

        if matched_hold == hold_request:
            # no cheating detected
            return False

        else:
            # cheating detected!
            print("Cheater! or maybe you mistyped something?")
            return True

    # ?CORE GAME LOGIC

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
        new_round = True

        # ?Main loop
        while playing == True:
            # Round begins, if new_round latch is true, state that we're starting a new round.
            if new_round == True:
                print(f"Starting round {round_count}")

            print(f"Rolling {die_count}...")

            this_roll = GameLogic.roll_dice(die_count)

            time.sleep(0.60)

            print(f"***{GameLogic.display_tuple(this_roll)}***")

            # check for zilch, where if holding all dice just rolled along with already held dice gives no increase to hand score.

            zilch_check = this_roll + tuple(held_dice)
            # print(
            #     f"value of zilch_check is {zilch_check} which returns a score of {GameLogic.calculate_score(zilch_check)}"
            # )
            # print(f"value of hand_score is {hand_score}")
            if GameLogic.calculate_score(zilch_check) == hand_score:
                print("\nZilch!\n")
                time.sleep(1)
                hand_score = 0
                held_dice = []
                round_count += 1
                die_count = 6
                new_round = True

            else:
                # Set new_round to false, that way if we roll again on the same round, the Zilch check can occur.
                new_round = False
                print(f"Enter dice to keep, or (q)uit:")

                response = input("> ")

                if response == "q":
                    print(f"Thanks for playing. You earned {total_score} points")
                    exit()

                if GameLogic.check_cheating(response, this_roll) == True:
                    # ?cheater loop below gets activated if the user provide an invalid response (not numbers) as well.
                    cheater = True
                    while cheater == True:
                        response = input("> ")

                        # Allow exit even in cheater loop
                        if response == "q":
                            print(
                                f"Thanks for playing. You earned {total_score} points"
                            )
                            exit()

                        if GameLogic.check_cheating(response, this_roll) == False:
                            cheater = False

                # Convert response to list of string-digits, then convert those string digits to ints.
                held_dice += [*response]
                held_dice = list(map(int, held_dice))

                # Remove the number of dice taken from the die count.
                die_count -= len(response)

                # Calculate this hand's score from the dice currently held
                hand_score = GameLogic.calculate_score(held_dice)

                # Check for user having held all dice, and respond for them that they want to bank whatever they have.
                if die_count == 0:
                    response = "b"

                # Otherwise, tell of hand score, dice available, and prompt for user response.
                else:
                    print(
                        f"You have {hand_score} unbanked points and {die_count} dice remaining"
                    )

                    print("(r)oll again, (b)ank your points or (q)uit:")
                    response = input("> ")

                if response == "q":
                    print(f"Thanks for playing. You earned {total_score} points")
                    exit()

                if response == "r":
                    pass

                if response == "b":
                    print(f"You banked {hand_score} points in round {round_count}")

                    # update total score, reset unbanked points, increment round, reset die count.
                    total_score += hand_score
                    held_dice = []
                    hand_score = 0
                    round_count += 1
                    die_count = 6
                    new_round = True
                    print(f"Total score is {total_score} points")


GameLogic.startup_prompt()
GameLogic.play_game()
