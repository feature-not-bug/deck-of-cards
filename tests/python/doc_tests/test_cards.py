from __future__ import annotations

from doc.cards import Card, PokerCard, CardCompare, Suit

# cannot instantiate an ABC so this is a dummy class to test simple functionality
class SampleCard(Card):
    def __init__(self, id, userFriendlyName, order):
        super().__init__(id, userFriendlyName, order)

    # have to implement abstract but not actually using it
    def compare(self, card) -> CardCompare:
        return CardCompare.DRAW


class TestCard:
    def test_init_whenValsPassed_thenSetSuccess(self):
        card = SampleCard("testid", "testname", 10)
        assert card.id == "testid"
        assert card.getUserFriendlyName() == "testname"
        assert card.order == 10


class TestPokerCard:
    def test_suit_whenHeartSuit_thenSetSuccess(self):
        card = PokerCard("testid", "testname", Suit.HEART, 10)
        assert card.suit == Suit.HEART

    def test_isFaceValue_whenFaceValue_thenReturnTrue(self):
        card = PokerCard("J", "Jack", Suit.HEART, 11)
        assert card.isFaceValue == True
        card = PokerCard("Q", "Queen", Suit.HEART, 12)
        assert card.isFaceValue == True
        card = PokerCard("K", "King", Suit.HEART, 13)
        assert card.isFaceValue == True
        card = PokerCard("A", "Ace", Suit.HEART, 14) # ace high
        assert card.isFaceValue == True
        card = PokerCard("A", "Ace", Suit.HEART, 1) # ace low
        assert card.isFaceValue == True

    def test_isFaceValue_whenNotFaceValue_thenReturnFalse(self):
        card = PokerCard("2", "Two", Suit.HEART, 2)
        assert card.isFaceValue == False

    def test_getUserFriendlyName_whenSpadeSuit_thenIncludeSpadePlural(self):
        card = PokerCard("2", "Two", Suit.SPADE, 2)
        assert card.getUserFriendlyName() == "Two of Spades"

    def test_compare_whenFiveAndTen_thenFiveLoses(self):
        fiveCard = PokerCard("5", "Five", Suit.SPADE, 5)
        tenCard = PokerCard("10", "Ten", Suit.SPADE, 10)
        assert fiveCard.compare(tenCard) == CardCompare.LOSE

    def test_compare_whenJackAndTen_thenJackWins(self):
        jackCard = PokerCard("J", "Jack", Suit.SPADE, 11)
        tenCard = PokerCard("10", "Ten", Suit.SPADE, 10)
        assert jackCard.compare(tenCard) == CardCompare.WIN

    def test_compare_whenTwoAndTwo_thenDraw(self):
        twoCard1 = PokerCard("2", "Two", Suit.SPADE, 2)
        twoCard2 = PokerCard("2", "Two", Suit.SPADE, 2)
        assert twoCard1.compare(twoCard2) == CardCompare.DRAW
