import models.cards.objects

resource = models.cards.General(
    name='Mr. General',
    attack=2,
    max_health=25,
    move_options=models.cards.locations.LocationFromCoords(row=2, col=2)
)
