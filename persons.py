class Person:
    """A player of baccarat game. Create several instances to have multiplayer.

    Args:
        balance: int, the initial balance of the player.

    Atributes:
        pid: int, sequencial id number of the playeri.
        balance: int, the balance of player.
        hand_bet: str, the hand in which the player is betting.
        amount_bet: int, the amount of a bet. """
    _pid = 1

    def __init__(self, balance):
        if not isinstance(balance, int):
            raise TypeError('Balance must be an integer.')
        elif balance < 1:
            raise ValueError('Balance must be positive.')
        self._pid = Person._pid
        self._balance = balance
        self._hand_bet = None
        self._amount_bet = 0
        Person._pid += 1

    @property
    def pid(self):
        """Get the player id."""
        return self._pid

    @property
    def balance(self):
        """Get the player balance."""
        return self._balance

    @property
    def hand_bet(self):
        """Get the hand on which the bet was made.
        """
        return self._hand_bet

    @hand_bet.setter
    def hand_bet(self, hand):
        #print(hand)
        if hand not in ['player', 'banker', 'tie']:
            raise ValueError('Invalid hand.')
        self._hand_bet = hand

    @property
    def amount_bet(self):
        """Get the amount of a bet.
        """
        return self._amount_bet

    @amount_bet.setter
    def amount_bet(self, amount):
        if not isinstance(amount, int):
            raise TypeError('Amount must be a integer.')
        if amount < 1:
            raise ValueError('Amount must be positive.')
        if amount > self._balance:
            raise ValueError('Amount exceeds available balance.')
        self._amount_bet = amount

    def is_valid_bet(self):
        """Checks if the current bet is valid.

        Returns:
            bol, True if the bet is valid, False otherwise.
        """
        if self._hand_bet not in ['player', 'banker', 'tie'] or self._amount_bet <= 0:
            return False
        return True

    def win(self):
        """Perform the necessary actions upon a player win: adds the winnings
        to the balance according the bet and resets the bet.
        """
        if self.is_valid_bet():
            if self._hand_bet == 'player':
                self._balance += int(self._amount_bet * 1)
            elif self._hand_bet == 'banker':
                self._balance += int(self._amount_bet * 0.95)# 5% casino commision
            elif self._hand_bet == 'tie':
                self._balance += int(self._amount_bet * 8)
            self._hand_bet = None
            self._amount_bet = 0
        else:
            raise InvalidBet('Player does not have a valid bet.')

    def lose(self):
        """Performs the necessary action upon a player lose: resets the bet.
        """
        if self.is_valid_bet():
            self._balance -= self._amount_bet
            self._hand_bet = None
            self._amount_bet = 0
        else:
            raise InvalidBet('Player does not have a valid bet.')

    def __repr__(self):
        """Return the representation string as if the object was
        called when creating a new instance with the current balance.
        """
        return f'Person({self._balance})'

    def __str__(self):
        """Return a string separated by new lines with the id, amount and bet
        of the player in case there is a valid one.
        """
        bet = f'Hand bet: {self._hand_bet}, Amount bet: {self._amount_bet}'
        no_bet = 'No bet'
        return f'Person: {self._pid}, Balance: {self._balance}, {bet if self.is_valid_bet() else no_bet}.'

class InvalidBet(Exception):
    pass
