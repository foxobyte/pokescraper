import json


class Pokemon:
    def __init__(
            self, generation: int = None,
            national_number: int = None,
            name: str = None,
            special_name: str = None,
            species: str = None,
            height: str = None,
            weight: str = None,
            special_abilities: list = None,
            hidden_ability: str = None,
            pokemon_type: list = None,
            hp: int = None,
            attack: int = None,
            defense: int = None,
            special_attack: int = None,
            special_defense: int = None,
            speed: int = None,
            catch_rate: int = None,
            ev_yield: dict = None,
            base_friendship: int = None,
            base_exp: int = None,
            growth_rate: str = None,
            egg_groups: list = None,
            gender: dict = None,
            egg_cycles: int = None,
            moves_learned_at_level: dict = None,
            moves_learned_on_evolution: list = None,
            moves_learned_by_eggs: list = None,
            moves_learned_by_tutor: list = None,
            moves_learned_by_tm: dict = None,
            evolutions: dict = {}
    ):
        self.generation = generation
        self.national_number = national_number
        self.name = name
        self.special_name = special_name
        self.species = species
        self.height = height
        self.weight = weight
        self.special_abilities = special_abilities
        self.hidden_ability = hidden_ability
        self.pokemon_type = pokemon_type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.catch_rate = catch_rate
        self.ev_yield = ev_yield
        self.base_friendship = base_friendship
        self.base_exp = base_exp
        self.growth_rate = growth_rate
        self.egg_groups = egg_groups
        self.gender = gender
        self.egg_cycles = egg_cycles
        self.moves_learned_at_level = moves_learned_at_level
        self.moves_learned_on_evolution = moves_learned_on_evolution
        self.moves_learned_by_eggs = moves_learned_by_eggs
        self.moves_learned_by_tutor = moves_learned_by_tutor
        self.moves_learned_by_tm = moves_learned_by_tm
        self.evolutions = evolutions

    def get_url_name(self):
        url_name = self.name.lower()
        url_name = url_name.replace("♀", "-f")
        url_name = url_name.replace("♂", "-m")
        url_name = url_name.replace(". ", "-")
        url_name = url_name.replace(": ", "-")
        url_name = url_name.replace(" ", "-")
        url_name = url_name.replace(".", "")
        url_name = url_name.replace("'", "")
        url_name = url_name.replace("é", "e")

        return url_name

    def get_enum_name(self):
        enum_name = self.name

        if self.special_name is not None:
            enum_name += " " + self.special_name

            if self.special_name.find("Mega", 0, 4) == 0:
                enum_name = self.special_name
            if self.special_name.find("Hisuian", 0, 7) == 0:
                enum_name = self.special_name
            if self.special_name.find("Galarian", 0, 8) == 0:
                enum_name = self.special_name
            if self.special_name.find("Primal", 0, 6) == 0:
                enum_name = self.special_name
            if self.special_name.find("Paldean", 0, 7) == 0:
                enum_name = self.special_name
            if self.special_name.find("Partner", 0, 7) == 0:
                enum_name = self.special_name
            if self.special_name.find("Alolan", 0, 6) == 0:
                enum_name = self.special_name

        enum_name = enum_name.replace("-", "_")
        enum_name = enum_name.replace(" ", "_")
        enum_name = enum_name.replace("'", "")
        enum_name = enum_name.replace(":", "")
        enum_name = enum_name.replace("%", "")
        enum_name = enum_name.replace(".", "")
        enum_name = enum_name.replace("♀", "_F")
        enum_name = enum_name.replace("♂", "_M")
        enum_name = enum_name.replace("é", "e")

        return enum_name.upper()

    def to_json(self):
        pokemon_dict = vars(self)

        try:
            pokemon_dict['type'] = pokemon_dict['pokemon_type']
            del pokemon_dict['pokemon_type']
        except KeyError:
            print("already done did dat bruh")

        keys = list(pokemon_dict.keys())

        for key in keys:
            new_key = ""
            if "_" in key:
                for i, word in enumerate(key.split("_")):
                    if i > 0:
                        word = word[:1].upper() + word[1:]
                    new_key += word
                pokemon_dict[new_key] = pokemon_dict[key]
                del pokemon_dict[key]

        for e in pokemon_dict['evolutions']:
            pokemon_dict['evolutions'][e] = pokemon_dict['evolutions'][e].to_json()

        return json.dumps(pokemon_dict, indent=4)
