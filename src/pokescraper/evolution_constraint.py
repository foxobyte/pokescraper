class EvolutionConstraint:
    def __init__(self, level: int = None,
                 held_item: str = None,
                 used_item: str = None,
                 has_pokemon: str = None,
                 time: str = None,
                 high_friendship: bool = None,
                 needs_trade: bool = None,
                 used_move: dict = None,
                 learned_move: str = None):
        self.level = level
        self.held_item = held_item
        self.used_item = used_item
        self.has_pokemon = has_pokemon
        self.time = time
        self.high_friendship = high_friendship
        self.needs_trade = needs_trade
        self.used_move = used_move
        self.learned_move = learned_move

    def to_json(self):
        evolution_constraint_dict = vars(self)

        try:
            evolution_constraint_dict['heldItem'] = evolution_constraint_dict['held_item']
            del evolution_constraint_dict['held_item']
            evolution_constraint_dict['usedItem'] = evolution_constraint_dict['used_item']
            del evolution_constraint_dict['used_item']
            evolution_constraint_dict['hasPokemon'] = evolution_constraint_dict['has_pokemon']
            del evolution_constraint_dict['has_pokemon']
            evolution_constraint_dict['highFriendship'] = evolution_constraint_dict['high_friendship']
            del evolution_constraint_dict['high_friendship']
            evolution_constraint_dict['needsTrade'] = evolution_constraint_dict['needs_trade']
            del evolution_constraint_dict['needs_trade']
            evolution_constraint_dict['usedMove'] = evolution_constraint_dict['used_move']
            del evolution_constraint_dict['used_move']
            evolution_constraint_dict['learnedMove'] = evolution_constraint_dict['learned_move']
            del evolution_constraint_dict['learned_move']
        except KeyError:
            print("blah blah blahh")

        return evolution_constraint_dict
