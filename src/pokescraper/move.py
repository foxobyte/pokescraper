import json
import yaml


class Move:
    def __init__(self,
                 name: str = None,
                 move_type: str = None,
                 category: str = None,
                 power: int = None,
                 accuracy: int = None,
                 pp: int = None,
                 effect_description: str = None,
                 probability: int = None,
                 is_high_crit: bool = None
    ):
        self.name = name
        self.move_type = move_type
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.pp = pp
        self.effect_description = effect_description
        self.probability = probability
        self.is_high_crit = is_high_crit

    def get_enum_name(self):
        enum_name = self.name.replace("-", "_")
        enum_name = enum_name.replace(" ", "_")
        enum_name = enum_name.replace("'", "")
        enum_name = enum_name.replace(":", "")
        enum_name = enum_name.replace("%", "")
        enum_name = enum_name.replace(".", "")
        enum_name = enum_name.replace("é", "e")

        return enum_name.upper()

    def to_yaml(self):
        return yaml.dump(self.fix_keys())

    def to_json(self):
        return json.dumps(self.fix_keys())

    def fix_keys(self):
        move_dict = vars(self)

        try:
            move_dict['type'] = move_dict['move_type']
            del move_dict['move_type']
        except KeyError:
            print("already done did dat bruh")

        keys = list(move_dict.keys())

        for key in keys:
            new_key = ""
            if "_" in key:
                for i, word in enumerate(key.split("_")):
                    if i > 0:
                        word = word[:1].upper() + word[1:]
                    new_key += word
                move_dict[new_key] = move_dict[key]
                del move_dict[key]

        return move_dict