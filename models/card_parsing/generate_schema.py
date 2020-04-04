import base

import cards


class CardContainer(base.BaseModel):
    card: cards.Card


if __name__ == '__main__':
    schema_root = cards.CardRoot  # todo want to remove the container aspect and just use the union of cards.
    schema_json = schema_root.schema_json(indent=2)
    file_name = 'duelers_schema'
    version = '0_1'
    with open(f'../schema_exports/{file_name}_{version}.json', 'w+') as file:
        file.write(schema_json)
