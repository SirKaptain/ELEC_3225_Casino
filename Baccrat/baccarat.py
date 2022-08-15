import time
from rules import Table

class Baccarat:
    """Command line interface of the game. Only interacts with Table object in
    order to receive input from the game logic.
    """
    def __init__(self):
        self._game = Table()
        self._quit = False
        self._options = {
            '1': self.status,
            '2': self.create_shoe,
            '3': self.add_person,
            '4': self.place_bets,
            '5': self.deal_hands,
            '0': self.quit
            }

    def run(self):
        """Main menu of the game."""
        print('------------Baccarat---------------')
        while not self._quit:
            print('''
Select an option:
1: See Status
2: Change shoe
3: Add new person
4: Place bets
5: Deal cards
0: Quit''')
            print()
            selection = input('Your selection: ')
            print()
            if selection in self._options:
                self._options[selection]()
            else:
                print('Selection not recognized.')

    def status(self):
        print(f'No of decks in shoe : {self._game.num_decks}')
        if self._game.available_persons:
            print(f'No of persons in game: {len(self._game.available_persons)} ')
            for person in self._game.available_persons:
                print(self._game[person])
        else:
            print('No persons.')
        
    def add_person(self):
        """Adds a new person to the game."""
        print('Adding new person')
        balance_input = input('Enter balance or <c> to cancel: ')
        if balance_input.lower() in ['c', 'cancel']:
            return
        try:
            # Try to convert to int but don't capture error
            try:
                balance_input = int(balance_input)
            except:
                pass
            self._game.add_person(balance_input)
            print()
            print(f'Person added with {balance_input} balance.')
        except (ValueError, TypeError) as error:
            print()
            print(error)
            self.add_person()

    def place_bets(self):
        """Loops through out all the available person to place the individual
        bets.
        """
        if self._game.available_persons:
            for person_i in self._game.available_persons:
                self.bet(person_i)
            print('All bets placed.')
        else:
            print('No persons to place bets.')

    def bet(self, person_i):
        """Places an individual bet for person_i."""
        hands = {
            'p': 'player',
            'player': 'player',
            'b': 'banker',
            'banker': 'banker',
            't': 'tie',
            'tie': 'tie'
            }
        action = 'Replacing' if person_i in self._game.valid_bets else 'New'
        print(f'{action} bet for Person {person_i + 1}. Press <s> to skip.')
        hand_input = input('The hand to bet. <p> player, <b> banker, <t> tie: ')
        if hand_input.lower() in ['s', 'skip']:
            print()
            return
        amount_input = input('The amount to bet: ')
        if amount_input.lower() in ['s', 'skip']:
            print()
            return
        try:
            # Try to convert to int but don't capture error
            try:
                amount_input = int(amount_input)
            except:
                pass
            self._game.bet(person_i, hands.get(hand_input.lower()), amount_input)
            print()
        except (ValueError, TypeError, GameError) as error:
            print()
            print(error)
            self.bet(person_i)

    def deal_hands(self):
        """Deals both player and banker hands and proceeds with the game itself.
        Check if there is a natural, draws possible thrird cards and apply the
        bet results.
        """

        def result_str():
            """Returns a string with the game result to be printed as output."""
            if self._game.game_result() != 'tie':
                return self._game.game_result().title() + ' win'
            else:
                return self._game.game_result().title()

        def print_hands():
            print()
            print('Showing Player hand')
            print(f'Player hand   {self._game.player_cards}')
            player_values = ', '.join([str(value) for value in self._game.player_values])
            print(f'Cards values  {player_values}.')
            print(f'Total hand value   {self._game.player_value}.')
            time.sleep(0.5)
            print()
            print('Showing Banker hand')
            print(f'Banker hand   {self._game.banker_cards}.')
            banker_values = ', '.join([str(value) for value in self._game.banker_values])
            print(f'Cards values   {banker_values}.')
            print(f'Total hand value   {self._game.banker_value}.')


        print('Dealing hands...')
        time.sleep(1)
        self._game.deal_hands()
        print_hands()
        print()
        if self._game.is_natural():
            time.sleep(0.5)
            print(f'{result_str()}. Natural.')
        else:
            print('Drawing third cards...')
            time.sleep(1)
            third_draws = self._game.draw_thirds()
            for third_draw in third_draws:
                print(f'{third_draw[0].title()} draw third card, {third_draw[1]}.')
                time.sleep(0.5)
            print()
            print_hands()
            time.sleep(0.5)
            print(f'{result_str()}.')
        print()
        print()
        print('Checking bets...')
        time.sleep(1)
        if self._game.valid_bets:
            for person_i in self._game.valid_bets:
                bet_result = self._game.bet_result(person_i)
                print(f'Person {person_i + 1} {bet_result[0]}. Balance: {bet_result[1]}.')
                time.sleep(0.5)
        else:
            print('No bets no table.')
        if self._game.open_bets():
            print('Bets are open.')
        print()

    def create_shoe(self):
        """Creates a new shoe. Replaces the previous one."""
        shoe_input = input('The number of decks for the new shoe or <c> to cancel: ')
        if shoe_input.lower() in ['c', 'cancel']:
            return
        try:
            # Try to convert to int but don't capture error
            try:
                shoe_input = int(shoe_input)
            except:
                pass
            self._game.create_shoe(shoe_input)
            print()
            print(f'A new shoe with {int(shoe_input)} deck(s) will be used on the game.')
        except (ValueError, TypeError) as error:
            print()
            print(error)
            self.create_shoe()

    def quit(self):
        self._quit = True

if __name__ == '__main__':
    Baccarat().run()