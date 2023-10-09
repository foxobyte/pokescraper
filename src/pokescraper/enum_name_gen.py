def generate_pokemon_enum_name(name: str) -> str:
    enum_name = name.replace("-", "_")
    enum_name = enum_name.replace(" ", "_")
    enum_name = enum_name.replace("'", "")
    enum_name = enum_name.replace(":", "")
    enum_name = enum_name.replace("%", "")
    enum_name = enum_name.replace(".", "")
    enum_name = enum_name.replace("♀", "_F")
    enum_name = enum_name.replace("♂", "_M")
    enum_name = enum_name.replace("é", "e")

    return enum_name.upper()


def generate_move_enum_name(name: str) -> str:
    enum_name = name

    return enum_name
