from doc.cards import PokerCard, Suit
from doc.decks import PokerDeck, DeckType, DeckFactory

# NOTE: To save time, will testing Abstract Base Class (ABC) Deck inside here
class TestPokerDeck:
    def test_init_whenCardsProvided_thenSetProperly(self):
        cards = []
        cards.append(PokerCard('2', 'Two', Suit.HEART, 2))
        cards.append(PokerCard('3', 'Three', Suit.HEART, 3))
        deck = PokerDeck(cards)
        assert len(deck._cards) == 2

    def test_init_whenCalled_thenDeckTypeIsPoker(self):
        deck = PokerDeck([])
        assert deck.deckType == DeckType.POKER

    def test_create_whenCalled_thenFiftyTwoCardsCreatedSuccessfully(self):
        deck = PokerDeck.create()

        heartUniqueSeen = set()
        spadeUniqueSeen = set()
        clubUniqueSeen = set()
        diamondUniqueSeen = set()

        for card in deck._cards:
            if card.suit == Suit.HEART: heartUniqueSeen.add(card.id)
            if card.suit == Suit.SPADE: spadeUniqueSeen.add(card.id)
            if card.suit == Suit.CLUB: clubUniqueSeen.add(card.id)
            if card.suit == Suit.DIAMOND: diamondUniqueSeen.add(card.id)

        assert len(heartUniqueSeen) == 13
        assert len(spadeUniqueSeen) == 13
        assert len(clubUniqueSeen) == 13
        assert len(diamondUniqueSeen) == 13

        # NOTE: ace high logic actually tested below in TestDeckFactory. probably should be here but not a big deal

    def test_create_whenCalled_thenCardsOrderedAscending(self):
        deck = PokerDeck.create()

        orderedCorrectly = True
        for i in range(1, len(deck._cards)): # start at index 1 to guarantee (i-1) in bounds
            if deck._cards[i - 1].order > deck._cards[i].order:
                orderedCorrectly = False
                break

        assert orderedCorrectly

    def test_shuffle_whenFullDeck_thenSuccess(self):
        deck = PokerDeck.create()

        preShuffleCards = deck._cards[:] # shallow copy

        deck.shuffle()

        atLeastOneCardPositionChanged = False
        for i in range(deck._initCardCount):
            if preShuffleCards[i].id != deck._cards[i].id:
                atLeastOneCardPositionChanged = True
                break

        assert atLeastOneCardPositionChanged

    def test_shuffle_whenTwoCards_thenSwapped(self):
        deck = PokerDeck.create()

        numCards = deck.cardsRemaining()
        for _ in range(numCards - 2):
            deck.dealOneCard()

        preShuffleCards = deck._cards[:] # shallow copy

        deck.shuffle()

        assert preShuffleCards[0].id == deck._cards[1].id
        assert preShuffleCards[1].id == deck._cards[0].id

    def test_shuffle_whenNoCards_thenNoError(self):
        deck = PokerDeck.create()

        # deal all cards
        while deck.cardsRemaining():
            deck.dealOneCard()

        deck.shuffle()

        assert True

    def test_dealOneCard_whenCalledBeforeShuffle_returnsAceCardAsDeckConfiguredAceHigh(self):
        deck = PokerDeck.create()

        card = deck.dealOneCard()

        # by default cards are ordered asc so smallest cards are at the bottom
        # this is definitely an implementation detail that could be interpreted differently
        # if we wanted to have the "2" at the top, would change the Deck's init to sort descending then update this test
        assert card and card.id == "A"

    def test_dealOneCard_whenCalledBeforeShuffle_returnsKingCardAsDeckConfiguredAceLow(self):
        deck = PokerDeck.create({"ace_high": False})
        card = deck.dealOneCard()
        assert card and card.id == "K"

    def test_dealOneCard_whenDeckIsEmpty_thenNoCardDealt(self):
        deck = PokerDeck.create()
        deck.shuffle()

        # deal all cards
        while deck.cardsRemaining() > 0:
            deck.dealOneCard()

        # deck is now empty
        card = deck.dealOneCard()

        assert card is None

    def test_cardsDealt_whenNone_thenReturnZero(self):
        deck = PokerDeck.create()
        assert deck.cardsDealt() == 0

    def test_cardsDealt_whenOneDealt_thenReturnOne(self):
        deck = PokerDeck.create()
        deck.dealOneCard()
        assert deck.cardsDealt() == 1

    def test_cardsRemaining_whenNoneDealt_thenReturnFiftyTwo(self):
        deck = PokerDeck.create()
        assert deck.cardsRemaining() == 52

    def test_cardsRemaining_whenOneDealt_thenReturnFiftyOne(self):
        deck = PokerDeck.create()
        deck.dealOneCard()
        assert deck.cardsRemaining() == 51

    def test_isEmpty_whenNoneDealt_thenReturnFalse(self):
        deck = PokerDeck.create()
        assert deck.isEmpty() == False

    def test_isEmpty_whenOneDealt_thenReturnFalse(self):
        deck = PokerDeck.create()
        deck.dealOneCard()
        assert deck.isEmpty() == False

    def test_isEmpty_whenFiftyTwoDealt_thenReturnTrue(self):
        deck = PokerDeck.create()
        for _ in range(52):
            deck.dealOneCard()
        assert deck.isEmpty() == True


class TestDeckFactory:
    def test_create_whenPokerDeckTypeNoConfig_thenSuccessWithAceHigh(self):
        deck = DeckFactory.create(DeckType.POKER)

        assert deck.deckType == DeckType.POKER

        for card in deck._cards:
            if card.id == "A":
                assert card.order == 14
                return

        assert False, "Ace not found."

    def test_create_whenPokerDeckTypeConfigAceLow_thenSuccessWithAceLow(self):
        config = { "ace_high": False }
        deck = DeckFactory.create(DeckType.POKER, config)

        for card in deck._cards:
            if card.id == "A":
                assert card.order == 1
                return

        assert False, "Ace not found."