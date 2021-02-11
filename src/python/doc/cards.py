from __future__ import annotations

from .messages import unknownValue
from enum import Enum
from abc import abstractmethod, ABC


class Suit(Enum):
    HEART = 1
    SPADE = 2
    CLUB = 3
    DIAMOND = 4


class CardCompare(Enum):
    WIN = 1
    DRAW = 2
    LOSE = 3


class Card(ABC):
    def __init__(self, id: str, userFriendlyName: str, order: int=0):
        self._id = id
        self._userFriendlyName = userFriendlyName
        self._order = order

    @property
    def id(self) -> str:
        return self._id

    @property
    def order(self) -> int:
        return self._order

    def getUserFriendlyName(self) -> str:
        return self._userFriendlyName

    @abstractmethod
    def compare(self, card: Card) -> CardCompare:
        pass


# NOTE: Thought about making classes to represent a collection of cards (dealt hand). Deferred but would be useful (necessary)
# to complement these other classes to build out an actual game simulation


class PokerCard(Card):
    def __init__(self, id: str, userFriendlyName: str, suit: Suit, order: int=0):
        super().__init__(id, userFriendlyName, order)

        self._suit = suit
        self._order = order

    @property
    def suit(self) -> Suit:
        return self._suit

    @property
    def isFaceValue(self) -> bool:
        # NOTE: Making constants for identifiers might be a good idea but deferring to save time
        return self.id in ['A', 'J', 'Q', 'K']

    def getUserFriendlyName(self) -> str:
        return f"{self._userFriendlyName} of {self._getSuitDesc()}"

    def compare(self, other: PokerCard) -> CardCompare:
        # Using "order" as the card's weight/strength.
        # Since cards are typically ordered by their by strength (ascending), leveraging that logic here
        if self.order > other.order:
            return CardCompare.WIN
        elif self.order < other.order:
            return CardCompare.LOSE
        else:
            return CardCompare.DRAW

    def _getSuitDesc(self) -> str:
        if self.suit == Suit.HEART:
            return "Hearts"
        elif self.suit == Suit.SPADE:
            return "Spades"
        elif self.suit == Suit.CLUB:
            return "Clubs"
        elif self.suit == Suit.DIAMOND:
            return "Diamonds"
        else:
            raise ValueError(unknownValue("suit", value=self.suit.name))
