#from game_logic import GameLogic
from ten_thousand.game_logic import GameLogic


class Game:
  def play(iterations):
    GameLogic.startup_prompt()
    GameLogic.play_game()