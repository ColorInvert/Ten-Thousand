
LAB - Class 08
Project: Ten Thousand Version 3
Author: Casey Glidewell

How to initialize/run your application (where applicable)

    Running game_logic.py in the ten_thousand folder will begin the game in your console.

Tests

    Tests are run through pytest, and v1 of this assignment came with a premade set of tests to pass before version one is considered complete.
    v2 required the ability to match the "simulations" provided in the version_2 folder. Counting the rounds, adding up score, calculating current hand, and the ability to quit at any time with q were all requirements of v2.

    v3 had the following written requirements without a testing suite:

    Should handle setting aside scoring dice and continuing turn with remaining dice.
    Should handle when cheating occurs.

    Or just typos.
    E.g. roll = [1,3,5,2] and user selects 1, 1, 1, 1, 1, 1

    Should allow user to continue rolling with 6 new dice when all dice have scored in current turn.

    Handle zilch
    No points for round, and round is over
