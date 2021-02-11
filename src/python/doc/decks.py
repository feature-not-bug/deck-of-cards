from __future__ import annotations

from .cards import Card, PokerCard, Suit
from .messages import unknownValue
from enum import Enum
from typing import List
from abc import abstractmethod, ABC
import random


class DeckType(Enum):
    POKER = 1


class Deck(ABC):
    def __init__(self, cards: List[Card], deckType: DeckType):
        self._cards = cards
        self._deckType = deckType

        # ensure cards are ordered properly as if you purchased a new deck and cards have not been shuffled yet
        # list will act as a stack where card at top of deck is the last item in the list
        # this will allow dealing the next card from top of deck to have O(1) time complexity
        if cards:
            self._cards = sorted(cards, key=lambda c: c.order)
        else:
            self._cards = []

        self._initCardCount = len(self._cards)

    @property
    def deckType(self) -> DeckType:
        return self._deckType

    @staticmethod
    @abstractmethod
    def create(config: dict={}) -> Deck:
        pass

    def shuffle(self):
        currCardCount = self.cardsRemaining()

        if currCardCount == 0 or currCardCount == 1: # nothing to shuffle
            return

        if currCardCount == 2: # simply swap the two otherwise dealer needs to be fired :D
            self._cards[0], self._cards[1] = self._cards[1], self._cards[0]

        # NOTE: There is no guarantee that a card won't remain in its original position in the deck after the while loop breaks
        # Decided to use currCardCount as the "# of iterations" signal as opposed to a constant, arbitrary value
        # This is beneficial as the deck becomes smaller in terms of runtime performance. Another thought I had was potentially
        # building a configuration "knob" into the class design to delegate the "quality of shuffle" to the person/entity
        # this is performing the shuffle on the deck. Decided to not go down that rabbit hole though for the sake of this being an exercise.
        swapCount = 0
        while swapCount < currCardCount:
            idx1 = random.randint(0, currCardCount - 1)
            idx2 = random.randint(0, currCardCount - 1)
            self._cards[idx1], self._cards[idx2] = self._cards[idx2], self._cards[idx1]
            swapCount += 1

    def dealOneCard(self) -> Card:
        if self.cardsRemaining() == 0:
            return

        return self._cards.pop() # constant time

    def cardsDealt(self) -> int:
        return self._initCardCount - len(self._cards)

    def cardsRemaining(self) -> int:
        return len(self._cards)

    def isEmpty(self) -> bool:
        return True if len(self._cards) == 0 else False

    # NOTE: Nice to have - reset method that simulates cards being returned back to deck. Would some combination
    # of non-abstract and abstract methods to control resetting common card attrs here and re-creation of cards
    # on the implementers. Otherwise could store a second copy of cards passed to constructor and just point to
    # it during reset. Downside is memory footprint doubles (also depends on if its a shallow vs. deep copy) but time complexity is better.


class PokerDeck(Deck):
    def __init__(self, cards: List[PokerCard]):
        super().__init__(cards, DeckType.POKER)

    @staticmethod
    def create(config: dict={}) -> PokerDeck:
        ace_high = True # default

        if "ace_high" in config:
            ace_high = config["ace_high"]

        cards = []

        # each card has 4 copies, one in each suit
        for suit in [Suit.HEART, Suit.SPADE, Suit.CLUB, Suit.DIAMOND]:
            cards.append(PokerCard('2', 'Two', suit, 2))
            cards.append(PokerCard('3', 'Three', suit, 3))
            cards.append(PokerCard('4', 'Four', suit, 4))
            cards.append(PokerCard('5', 'Five', suit, 5))
            cards.append(PokerCard('6', 'Six', suit, 6))
            cards.append(PokerCard('7', 'Seven', suit, 7))
            cards.append(PokerCard('8', 'Eight', suit, 8))
            cards.append(PokerCard('9', 'Nine', suit, 9))
            cards.append(PokerCard('10', 'Ten', suit, 10))
            cards.append(PokerCard('J', 'Jack', suit, 11))
            cards.append(PokerCard('Q', 'Queen', suit, 12))
            cards.append(PokerCard('K', 'King', suit, 13))
            cards.append(PokerCard('A', 'Ace', suit, 14 if ace_high else 1))

        return PokerDeck(cards)


class DeckFactory:
    @staticmethod
    def create(deckType: DeckType, deckConfig: dict={}) -> Deck:
        if deckType == DeckType.POKER:
            return PokerDeck.create(deckConfig)
        else:
            raise ValueError(unknownValue("deck type", deckType.name))
