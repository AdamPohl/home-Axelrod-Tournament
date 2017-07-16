from axelrod import Player, Actions, Game, DeterministicCache
from flask_assistant import Assistant, ask, tell
import axelrod.interaction_utils as iu
from flask import Flask
import axelrod as axl
import logging

app = Flask(__name__)
assist = Assistant(app, '/')

logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
C, D = Actions.C, Actions.D
PLAYERS = []
ROUNDS = 0


def update_history(player, move):
    """
    Updates histories and cooperation / defections counts following play.
    """
    player.history.append(move) # Update histories

    # Update player counts of cooperation and defection
    if move == C:
        player.cooperations += 1
    elif move == D:
        player.defections += 1

def update_state_distribution(player, action, reply):
    """
    Updates state_distribution following play.
    """
    last_turn = (action, reply)
    player.state_distribution[last_turn] += 1

class Googliness(Player):
    name = 'Googliness'

    classifier = {
        'memory_depth': float('inf'),
        'stochastic': True,
        'makes_use_of': set(['length', 'game']),
        'long_run_time': True,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def __init__(self, name='Googliness'):
        Player.__init__(self)
        self.name = name

    def strategy(self, opponent, choice):
        """
        This strategy should in theory work similar to human except for the Google
        Assistant, so you will have to say whetherr you want to cooperate or defect.
        """
        action = choice
        return action

class Match(object):

    def __init__(self):
        global ROUNDS
        global PLAYERS
        self.result = []
        self.game = Game()
        self.turns = ROUNDS
        self.players = list(PLAYERS)
        self._cache = DeterministicCache()

    def final_score(self):
        """
        Returns the final score for a Match.
        """
        return iu.compute_final_score(self.result, self.game)

    def winner(self):
        """
        Returns the winner of the Match.
        """
        winner_index = iu.compute_winner_index(self.result, self.game)
        if winner_index is False:  # No winner
            return False
        if winner_index is None:  # No plays
            return None
        return self.players[winner_index]

    def _last_round_moves(self):
        move = self.players[1].history[-1]
        opp_move = self.players[0].history[-1]

        return move, opp_move

    def talk(self):
        round = len(self.players[0].history) + 1
        opp = self.players[0].name
        turns = self.turns

        if opp == '$\phi$':
            opp = 'phi'
        elif opp == '$\pi$':
            opp = 'pi'
        elif opp == '$e$':
            opp = 'e'

        if round == 1:
            msg = ask("Starting a {} round match between you and {}.  Round 1, would you like to cooperate or defect?".format(turns, opp))
        elif round > 1 and round < turns:
            move, opp_move = self._last_round_moves()
            msg = ask("In round {}, you played {}, {} played {}.  Round {}, would you like to cooperate or defect?".format(round - 1, move, opp, opp_move, round))
        elif round == turns:
            move, opp_move = self._last_round_moves()
            msg = ask("In round {}, you played {}, {} played {}. Final round, would you like to cooperate or defect?".format(round - 1, move, opp, opp_move))
        elif round > turns:
            self.result = list(zip(self.players[0].history, self.players[1].history))
            score = self.final_score()
            winner = self.winner()

            if winner == False:
                msg = tell("End of the match, you scored {}, and {} scored {}, meaning the match is a draw.".format(score[1], opp, score[0]))
            elif str(winner) == '$\phi$':
                msg = tell("End of the match, you scored {}, and {} scored {}, meaning phi is the winner. Better luck next time.".format(score[1], opp, score[0]))
            elif str(winner) == '$\pi$':
                msg = tell("End of the match, you scored {}, and {} scored {}, meaning pi is the winner. Better luck next time.".format(score[1], opp, score[0]))
            elif str(winner) == '$e$':
                msg = tell("End of the match, you scored {}, and {} scored {}, meaning e is the winner. Better luck next time.".format(score[1], opp, score[0]))
            elif str(winner) == 'you: you':
                msg = tell("End of the match, you scored {}, and {} scored {}, meaning you are the winner.".format(score[1], opp, score[0]))
            else:
                msg = tell("End of the match, you scored {}, and {} scored {}, meaning {} is the winner. Better luck next time.".format(score[1], opp, score[0], winner))

        return msg

def which_strategy(opp):
    if opp == "adaptive":
        subject = "Adaptive"
    elif opp == "adaptive tit for tat":
        subject = "Adaptive Tit For Tat"
    elif opp == "aggravater":
        subject = "Aggravater"
    elif opp == "allcoralld":
        subject = "ALLCorALLD"
    elif opp == "alternator":
        subject = "Alternator"
    elif opp == "alternator hunter":
        subject = "Alternator Hunter"
    elif opp == "anticycler":
        subject = "AntiCycler"
    elif opp == "anti tit for tat":
        subject = "Anti Tit For Tat"
    elif opp == "adapative pavlov 2006":
        subject = "Adapative Pavlov 2006"
    elif opp == "adapative pavlov 2011":
        subject = "Adapative Pavlov 2011"
    elif opp == "appeaser":
        subject = "Appeaser"
    elif opp == "arrogant qlearner":
        subject = "Arrogant QLearner"
    elif opp == "average copier":
        subject = "Average Copier"
    elif opp == "better and better":
        subject = "Better and Better"
    elif opp == "backstabber":
        subject = "BackStabber"
    elif opp == "bully":
        subject = "Bully"
    elif opp == "calculator":
        subject = "Calculator"
    elif opp == "cautious qlearner":
        subject = "Cautious QLearner"
    elif opp == "champion":
        subject = "Champion"
    elif opp == "contrite tit for tat":
        subject = "Contrite Tit For Tat"
    elif opp == "cooperator":
        subject = "Cooperator"
    elif opp == "cooperator hunter":
        subject = "Cooperator Hunter"
    elif opp == "cycle hunter":
        subject = "Cycle Hunter"
    elif opp == "cycler cccccd":
        subject = "Cycler CCCCCD"
    elif opp == "cycler cccd":
        subject = "Cycler CCCD"
    elif opp == "cycler ccd":
        subject = "Cycler CCD"
    elif opp == "cycler dc":
        subject = "Cycler DC"
    elif opp == "cycler ddc":
        subject = "Cycler DDC"
    elif opp == "cycler cccdcd":
        subject = "Cycler CCCDCD"
    elif opp == "davis":
        subject = "Davis"
    elif opp == "defector":
        subject = "Defector"
    elif opp == "defector hunter":
        subject = "Defector Hunter"
    elif opp == "desperate":
        subject = "Desperate"
    elif opp == "doublecrosser":
        subject = "DoubleCrosser"
    elif opp == "doubler":
        subject = "Doubler"
    elif opp == "easygo":
        subject = "EasyGo"
    elif opp == "eatherley":
        subject = "Eatherley"
    elif opp == "eventual cycle hunter":
        subject = "Eventual Cycle Hunter"
    elif opp == "evolvedann":
        subject = "EvolvedANN"
    elif opp == "evolvedlookerup":
        subject = "EvolvedLookerUp"
    elif opp == "feld":
        subject = "Feld"
    elif opp == "firm but fair":
        subject = "Firm But Fair"
    elif opp == "fool me forever":
        subject = "Fool Me Forever"
    elif opp == "fool me once":
        subject = "Fool Me Once"
    elif opp == "forgetful fool me once":
        subject = "Forgetful Fool Me Once"
    elif opp == "forgetful grudger":
        subject = "Forgetful Grudger"
    elif opp == "forgiver":
        subject = "Forgiver"
    elif opp == "forgiving tit for tat":
        subject = "Forgiving Tit For Tat"
    elif opp == "fortress3":
        subject = "Fortress3"
    elif opp == "fortress4":
        subject = "Fortress4"
    elif opp == "pso gambler":
        subject = "PSO Gambler"
    elif opp == "gtft":
        subject = "GTFT"
    elif opp == "go by marjority":
        subject = "Go By Marjority"
    elif opp == "go by majority 10":
        subject = "Go By Majority 10"
    elif opp == "go by majority 20":
        subject = "Go By Majority 20"
    elif opp == "go by majority 40":
        subject = "Go By Majority 40"
    elif opp == "go by majority 5":
        subject = "Go By Majority 5"
    elif opp == "phi":
        subject = "$\phi$"
    elif opp == "gradual":
        subject = "Gradual"
    elif opp == "gradual killer":
        subject = "Gradual Killer"
    elif opp == "grofman":
        subject = "Grofman"
    elif opp == "grudger":
        subject = "Grudger"
    elif opp == "grudgeralternator":
        subject = "GrudgerAlternator"
    elif opp == "grumpy":
        subject = "Grumpy"
    elif opp == "handshake":
        subject = "Handshake"
    elif opp == "hard go by majority":
        subject = "Hard Go By Majority"
    elif opp == "hard go by majority 10":
        subject = "Hard Go By Majority 10"
    elif opp == "hard go by majority 20":
        subject = "Hard Go By Majority 20"
    elif opp == "hard go by majority 40":
        subject = "Hard Go By Majority 40"
    elif opp == "hard go by majority 5":
        subject = "Hard Go By Majority 5"
    elif opp == "hard prober":
        subject = "Hard Prober"
    elif opp == "hard tit for 2 tats":
        subject = "Hard Tit For 2 Tats"
    elif opp == "hard tit for tat":
        subject = "Hard Tit For Tat"
    elif opp == "hesitant qlearner":
        subject = "Hesitant QLearner"
    elif opp == "hopeless":
        subject = "Hopeless"
    elif opp == "inverse":
        subject = "Inverse"
    elif opp == "inverse punisher":
        subject = "Inverse Punisher"
    elif opp == "joss":
        subject = "Joss"
    elif opp == "knowledgeable worse and worse":
        subject = "Knowledgeable Worse and Worse"
    elif opp == "limited retaliate":
        subject = "Limited Retaliate"
    elif opp == "limited retaliate 2":
        subject = "Limited Retaliate 2"
    elif opp == "limited retaliate 3":
        subject = "Limited Retaliate 3"
    elif opp == "math constant hunter":
        subject = "Math Constant Hunter"
    elif opp == "naive prober":
        subject = "Naive Prober"
    elif opp == "negation":
        subject = "Negation"
    elif opp == "nice average copier":
        subject = "Nice Average Copier"
    elif opp == "nydegger":
        subject = "Nydegger"
    elif opp == "omega tft":
        subject = "Omega TFT"
    elif opp == "once bitten":
        subject = "Once Bitten"
    elif opp == "opposite grudger":
        subject = "Opposite Grudger"
    elif opp == "pi":
        subject = "$\pi$"
    elif opp == "predator":
        subject = "Predator"
    elif opp == "prober":
        subject = "Prober"
    elif opp == "prober 2":
        subject = "Prober 2"
    elif opp == "prober 3":
        subject = "Prober 3"
    elif opp == "prober 4":
        subject = "Prober 4"
    elif opp == "punisher":
        subject = "Punisher"
    elif opp == "raider":
        subject = "Raider"
    elif opp == "random":
        subject = "Random"
    elif opp == "random hunter":
        subject = "Random Hunter"
    elif opp == "remorseful prober":
        subject = "Remorseful Prober"
    elif opp == "retaliate":
        subject = "Retaliate"
    elif opp == "retaliate 2":
        subject = "Retaliate 2"
    elif opp == "retaliate 3":
        subject = "Retaliate 3"
    elif opp == "ripoff":
        subject = "Ripoff"
    elif opp == "risky qlearner":
        subject = "Risky QLearner"
    elif opp == "shubik":
        subject = "Shubik"
    elif opp == "slow tit for two tats":
        subject = "Slow Tit For Two Tats"
    elif opp == "sneaky tit for tat":
        subject = "Sneaky Tit For Tat"
    elif opp == "soft grudger":
        subject = "Soft Grudger"
    elif opp == "soft joss":
        subject = "Soft Joss"
    elif opp == "solutionb1":
        subject = "SolutionB1"
    elif opp == "solutionb5":
        subject = "SolutionB5"
    elif opp == "spiteful tit for tat":
        subject = "Spiteful Tit For Tat"
    elif opp == "stochastic cooperator":
        subject = "Stochastic Cooperator"
    elif opp == "stochastic wsls":
        subject = "Stochastic WSLS"
    elif opp == "suspicious tit for tat":
        subject = "Suspicious Tit For Tat"
    elif opp == "tester":
        subject = "Tester"
    elif opp == "thuemorse":
        subject = "ThueMorse"
    elif opp == "thuemorseinverse":
        subject = "ThueMorseInverse"
    elif opp == "thumper":
        subject = "Thumper"
    elif opp == "tit for tat":
        subject = "Tit For Tat"
    elif opp == "tit for 2 tats":
        subject = "Tit For 2 Tats"
    elif opp == "tricky cooperator":
        subject = "Tricky Cooperator"
    elif opp == "tricky defector":
        subject = "Tricky Defector"
    elif opp == "tullock":
        subject = "Tullock"
    elif opp == "two tits for tat":
        subject = "Two Tits For Tat"
    elif opp == "willing":
        subject = "Willing"
    elif opp == "win-shift lose-stay":
        subject = "Win-Shift Lose-Stay"
    elif opp == "win-stay lose-shift":
        subject = "Win-Stay Lose-Shift"
    elif opp == "worse and worse":
        subject = "Worse and Worse"
    elif opp == "worse and worse 2":
        subject = "Worse and Worse 2"
    elif opp == "worse and worse 3":
        subject = "Worse and Worse 3"
    elif opp == "zd-extort-2":
        subject = "ZD-Extort-2"
    elif opp == "zd-extort-2 v2":
        subject = "ZD-Extort-2 v2"
    elif opp == "zd-extort-4":
        subject = "ZD-Extort-4"
    elif opp == "zd-gtft-2":
        subject = "ZD-GTFT-2"
    elif opp == "zd-gen-2":
        subject = "ZD-GEN-2"
    elif opp == "zd-set-2":
        subject = "ZD-SET-2"
    elif opp == "e":
        subject = "$e$"
    elif opp == "meta hunter":
        subject = "Meta Hunter"
    elif opp == "meta hunter aggressive":
        subject = "Meta Hunter Aggressive"
    elif opp == "meta majority":
        subject = "Meta Majority"
    elif opp == "meta majority memory one":
        subject = "Meta Majority Memory One"
    elif opp == "meta majority finite memory":
        subject = "Meta Majority Finite Memory"
    elif opp == "meta majority long memory":
        subject = "Meta Majority Long Memory"
    elif opp == "meta minority":
        subject = "Meta Minority"
    elif opp == "meta mixer":
        subject = "Meta Mixer"
    elif opp == "meta winner":
        subject = "Meta Winner"
    elif opp == "meta winner deterministic":
        subject = "Meta Winner Deterministic"
    elif opp == "meta winner ensemble":
        subject = "Meta Winner Ensemble"
    elif opp == "meta winner memory one":
        subject = "Meta Winner Memory One"
    elif opp == "meta winner finite memory":
        subject = "Meta Winner Finite Memory"
    elif opp == "meta winner long memory":
        subject = "Meta Winner Long Memory"
    elif opp == "meta winner stochastic":
        subject = "Meta Winner Stochastic"
    elif opp == "mwe deterministic":
        subject = "MWE Deterministic"
    elif opp == "mwe finite memory":
        subject = "MWE Finite Memory"
    elif opp == "mwe long memory":
        subject = "MWE Long Memory"
    elif opp == "mwe memory one":
        subject = "MWE Memory One"
    elif opp == "mwe stochastic":
        subject = "MWE Stochastic"
    else:
        subject = "ERROR"

    return subject

@assist.action('LaunchAction')
def welcome():
    welcome_msg = 'Welcome to the Axelrod tournament. Do you want to play a game?'
    return ask(welcome_msg)

@assist.action("PlayAction", mapping={'Rounds': '@sys.number'})
def play_intent(Rounds, Strategy):
    you = Googliness(name='you')
    strategy = which_strategy(Strategy)

    if strategy == "ERROR":
        return err('play')

    opp = axl.strategies[[s.name for s in axl.strategies].index(strategy)]()

    global ROUNDS
    try:
        ROUNDS = int(Rounds)
    except ValueError or TypeError:
        return err('round')

    if ROUNDS == 0:
        return err('round')

    global PLAYERS
    PLAYERS = []
    PLAYERS.append(opp)
    PLAYERS.append(you)

    for p in PLAYERS:
        p.reset()

    for player in PLAYERS:
        player.set_match_attributes(length=ROUNDS, game=Game(), noise=0)

    return Match().talk()

@assist.action("ChoiceAction")
def choice_intent(Choice):
    if Choice == 'defect':
        choice = D
    elif Choice == 'cooperate':
        choice = C
    else:
        choice = "ERROR"

    if choice == "ERROR":
        return err('choice')

    global PLAYERS
    s1, s2 = PLAYERS[0].strategy(PLAYERS[1]), PLAYERS[1].strategy(PLAYERS[0], choice)

    update_history(PLAYERS[0], s1)
    update_history(PLAYERS[1], s2)
    update_state_distribution(PLAYERS[0], s1, s2)
    update_state_distribution(PLAYERS[1], s2, s1)

    return Match().talk()

@assist.action("HelpAction")
def help_intent():
    help_msg = """Using this skill you are able to start a 2 player match against one of 161 different strategies in the Axelrod library.
    You define how many rounds you want to go for, who you want to challenge, then tell me to cooperate or defect when it is your turn.
    Why not give a 3 round game against tit for tat a go, or, if your feeling adventurous, try a 23 round game against EvolvedANN.
    So... what would you like to do?"""
    return ask(help_msg)

def err(option):
    if option == 'choice':
        err_msg = "Your response is invalid, I require you cooperate or defect. Which one will it be?"
    elif option == 'play':
        err_msg = """That stategy does not exist, you can use any strategy currently in the Axelrod Python library.
        Take a look if you want I can wait..."""
    elif option == 'round':
        err_msg = "You haven`t given me the number of rounds that you want to play. Canceling match. What would you like to do?"

    return ask(err_msg)

def bye():
    bye_msg = "Guys, this isn't the user we're looking for. You can go about your business. Move along... move along."
    return tell(bye_msg)

@assist.action("StopAction")
def stop_intent():
    return bye()

@assist.action("CancelAction")
def cancel_intent():
    return bye()

if __name__ == '__main__':
    app.run(debug=True)
