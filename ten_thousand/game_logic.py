#
#! IMPORTANT: Version one of the scoring system for this program was written through CHATGPT3.5 prompt engineering. Full list of commands given is included in prompt.md, as well as reasoning for this approach. As of version 4 the GPT code was completely replaced with my own.
import random
import time
from collections import Counter


class GameLogic:
    @staticmethod
    def calculate_score(dice):
        dice = sorted(dice)
        score = 0

        dice_counts = [dice.count(i) for i in range(1, 7)]

        # A straight.
        if dice == [1, 2, 3, 4, 5, 6]:
            return 1500

        # Is there a 3 of a kind?
        for i in range(len(dice_counts)):
            if dice_counts[i] == 3:
                # Is the 3 of a kind of 1s?
                if i == 0:
                    score += 1000

                # If not, then the score is dievalue * 100
                else:
                    # Remember to add 1 to i to account for the index offset!
                    score += (i + 1) * 100

        # Is there a 4 of a kind?
        for i in range(len(dice_counts)):
            if dice_counts[i] == 4:
                # Is the 4 of a kind of 1s?
                if i == 0:
                    score += 2000

                # If not, then the score is dievalue * 100, *2.
                else:
                    # Remember to add 1 to i to account for the index offset!
                    score += ((i + 1) * 100) * 2

        # Is there a 5 of a kind?
        for i in range(len(dice_counts)):
            if dice_counts[i] == 5:
                # Is the 5 of a kind of 1s?
                if i == 0:
                    score += 3000

                # If not, then the score is dievalue * 100, *3.
                else:
                    # Remember to add 1 to i to account for the index offset!
                    score += ((i + 1) * 100) * 3

        # Is there a 6 of a kind?
        for i in range(len(dice_counts)):
            if dice_counts[i] == 6:
                # Is the 6 of a kind of 1s?
                if i == 0:
                    score += 4000

                # If not, then the score is dievalue * 100, *4.
                else:
                    # Remember to add 1 to i to account for the index offset!
                    score += ((i + 1) * 100) * 4

        # Handle "alone" 1s and 5s, each 1 worth 100, each 5 worth 50.
        # alone being not part of a 3 of a kind or better.
        if dice_counts[0] < 3:
            score += dice.count(1) * 100
        if dice_counts[4] < 3:
            score += dice.count(5) * 50

            # Override score entirely with 1500 if we've got Pairs. eg:1,1,3,3,5,5
            pairs_count = sum(1 for count in dice_counts if count >= 2)
            if pairs_count >= 3:
                return 1500

        return score

    @staticmethod
    def roll_dice(num_dice):
        return tuple(random.randint(1, 6) for _ in range(num_dice))

    @staticmethod
    def zilch_check(this_roll, held_dice):
        #!ZILCH CHECK IS CURRENTLY DUMMIED OUT, IN FAVOR OF GET_SCORERS.
        # NOTE this_roll is a tuple and thus immutable, and held_dice is a list.

        # TODO: Make check for if new roll has a 1, has a 5, or if held and new
        # roll combined create 3 of a kind of any number, or a straight, or 3 pairs.

        print(f"this_roll is {this_roll}")
        print(f"held dice is {held_dice}")
        combined = held_dice + list(this_roll)
        print(f"combined is {combined}")

        # ? Is there a 1 in the newly rolled dice?
        if 1 in this_roll:
            return False

        # ? Is there a 5 in the newly rolled dice?
        if 5 in this_roll:
            return False

        # ? Is there a 3 of a kind or better of any die face, WITHOUT use of held dice?
        if (
            this_roll.count(1) >= 3
            or this_roll.count(2) >= 3
            or this_roll.count(3) >= 3
            or this_roll.count(4) >= 3
            or this_roll.count(5) >= 3
            or this_roll.count(6) >= 3
        ):
            return False

        # ? None of the above are true, which means no
        # ? scoring dice exist. Zilch!
        return True

    @staticmethod
    def display_tuple(tuple):
        output = " "
        for i in tuple:
            output = output + str(i)
            output = output + " "
        return output


    #! ALERT: UNSOLVED BUG IN GET SCORERS BELOW!!!
    #! After holding some dice and rolling again, unscoring dice 
    #! like 2 are occasionally treated as scorers.
    
    # The bot only uses the roll value, but my scorer determination method
    # requires both the scorer, and the current hand of held dice.
    # Having a None held value that gets updated with the current held dice
    # allows get_scorers to be called without getting "wrong arg count" issues.
    @staticmethod
    def get_scorers(roll, held=None):
        scorers = []
        print(f"roll is {roll}")

        # held should always be none, and then get updated with
        # the actual hold here.
        if held == None:
            held = held_dice
            print(f"Player's held dice is {held}")
        combined = held + list(roll)
        print(f"combined is {combined}")

        # Get the total score on the table for all dice, in hand AND just rolled.
        all_score = GameLogic.calculate_score(combined)

        # Zilch check!
        if all_score == 0:
            return False

        print(f"all_score prior to calculations is {all_score}")

        tabled_dice = list(roll)

        confirmed_scorers = []

        # Iterate through the non-held dice, and for each one, try adding up
        # the score if that die did not exist. If the score decreases with that
        # die removed, then it was a scorer.
        for i in range(len(tabled_dice)):
            removed = tabled_dice[:i] + tabled_dice[i + 1 :]
            print(f"value of removed is {removed}")
            print(
                f"the calculated score of removed was {GameLogic.calculate_score(removed)}"
            )
            if GameLogic.calculate_score(removed) != all_score:
                confirmed_scorers.append(tabled_dice[i])
                print(f"scorer found! confirmed scorers is now {confirmed_scorers}")

        print(f"confirmed scorers being returned is {confirmed_scorers}")

        return confirmed_scorers
    
    #! ALERT: UNSOLVED BUG IN GET SCORERS ABOVE!!!

    @staticmethod
    # Gets user input for hold request and eliminates spaces or letters,
    # then converts to a tuple via list comprehension.
    # ?Thanks to instructor Adam Owada for the code snippet.
    def clean_input(input):
        cleaned = [int(element) for element in input if element.isnumeric()]
        cleaned = tuple(cleaned)
        return cleaned

    @staticmethod
    def validate_keepers(roll, hold_request):
        # Initialize a dictionary of the form {1:0,2:0,3:0,4:0,5:0,6:0}.
        # The key is the die face (what you rolled) and the value is number of
        # occurrences of that die face.
        roll_dict = Counter({i: 0 for i in range(1, 7)})

        # Update the dictionary with the possible dice that can be held.
        roll_dict.update(Counter(roll))
        # Iterate through the hold request, decrementing the dictionary at the address
        for i in hold_request:
            if i in roll_dict:
                roll_dict[i] -= 1

        # Check if all values in roll_dict are 0 or above, indicating that no
        # non-present or overflow numbers were requested in the hold.
        all_positive = all(value >= 0 for value in roll_dict.values())

        if all_positive:
            # no cheating detected, hold request validated
            return True

        else:
            # cheating detected, hold request invalid!
            print("Cheater! or maybe you mistyped something?")
            return False

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
        # ? Held dice is global because it is needed for my solution to get_scorers
        global held_dice
        held_dice = []
        round_count = 1
        die_count = 6
        response = ""
        total_score = 0
        hand_score = 0
        playing = True
        validated = True
        new_round = True

        # ?Main loop
        while playing == True:
            # Round begins, if new_round latch is true, state that we're starting a new round.
            if new_round == True:
                print(f"Starting round {round_count}")

            print(f"Rolling {die_count} dice...")

            this_roll = GameLogic.roll_dice(die_count)

            # ?Sleep was a fun idea, but it slows down bots.py.
            # time.sleep(0.60)

            print(f"***{GameLogic.display_tuple(this_roll)}***")

            # check for zilch, where if holding all dice just rolled along with already held dice gives no increase to hand score.
            # print(f"at time of zilch check, this_roll was {this_roll}")
            # print(f"the get scorers just returned{GameLogic.get_scorers(this_roll)}")

            if GameLogic.get_scorers(this_roll) == False:
                print("\nZilch!\n")
                hand_score = 0
                held_dice = []
                round_count += 1
                die_count = 6
                new_round = True

            # if GameLogic.zilch_check(this_roll, held_dice) == True:
            #     print("\nZilch!\n")
            #     hand_score = 0
            #     held_dice = []
            #     round_count += 1
            #     die_count = 6
            #     new_round = True

            else:
                # Set new_round to false, that way if we roll again on the same round, the Zilch check can occur.
                new_round = False
                print(f"Enter dice to keep, or (q)uit:")

                response = input("> ")

                if response == "q":
                    print(f"Thanks for playing. You earned {total_score} points")
                    exit()

                # Now that we know user didn't want to quit, clean input.
                response = GameLogic.clean_input(response)

                if GameLogic.validate_keepers(this_roll, response) == False:
                    # ?cheater loop below gets activated if the user provide an invalid response (not numbers) as well.
                    validated = False
                    while validated == False:
                        response = input("> ")

                        # Allow exit even in cheater loop
                        if response == "q":
                            print(
                                f"Thanks for playing. You earned {total_score} points"
                            )
                            exit()

                        # Now that we know user didn't want to quit, clean input.
                        response = GameLogic.clean_input(response)
                        if GameLogic.validate_keepers(this_roll, response) == True:
                            validated = True

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


if __name__ == "__main__":
    GameLogic.startup_prompt()
    GameLogic.play_game()
