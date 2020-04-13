import models.decks

resource = models.decks.MasterDeck(
    general_id="mr_general",
    cards=[
        models.cards.CardInclusionInDeck(card_id='underling', count=1)
    ]
)
