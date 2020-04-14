import models.cards.objects

resource = models.cards.General(
    name='Mr. General',
    attack=2,
    max_health=25,
    move_options=models.cards.locations.UnionLocations(
        locations=[
            models.cards.locations.ChooseLocation(
                choose_from=models.cards.locations.Column(col=3)
            )
        ]

        # locations=[
        #     models.cards.locations.LocationFromOffset(
        #         origin=models.cards.locations.LocationFromUnit(
        #             unit=models.cards.objects.This()
        #         ),
        #         row_offset=0,
        #         column_offset=1
        #     ),
        #     models.cards.locations.LocationFromOffset(
        #         origin=models.cards.locations.LocationFromUnit(
        #             unit=models.cards.objects.This()
        #         ),
        #         row_offset=1,
        #         column_offset=0
        #     ),
        #     models.cards.locations.LocationFromOffset(
        #         origin=models.cards.locations.LocationFromUnit(
        #             unit=models.cards.objects.This()
        #         ),
        #         row_offset=-1,
        #         column_offset=0
        #     ),
        #     models.cards.locations.LocationFromOffset(
        #         origin=models.cards.locations.LocationFromUnit(
        #             unit=models.cards.objects.This()
        #         ),
        #         row_offset=0,
        #         column_offset=-1
        #     )
        # ]

    )
)
