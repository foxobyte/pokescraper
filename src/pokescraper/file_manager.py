import json
from os import listdir
from os.path import isfile, join
from pokemon import Pokemon


def load_pokemon_from_file(file_name: str, directory: str = "./pokemon") -> Pokemon:
    with open(f"{directory}/{file_name}", "r") as file:
        data = json.loads(file.read())
        return build_pokemon_from_json(data)


def load_all_pokemon(directory: str = "./pokemon") -> list:
    files = [file_name for file_name in listdir(directory) if isfile(join(directory, file_name))]
    pokemon_list = []

    for file_name in files:
        pokemon_list.append(load_pokemon_from_file(file_name, directory))

    return pokemon_list


def write_pokemon_to_json(pokemon: Pokemon, directory: str = "./pokemon") -> None:
    with open(f"{directory}/{pokemon.get_enum_name()}.json", "w") as file:
        file.write(pokemon.to_json())


def build_pokemon_from_json(data: dict):
    return Pokemon(
        generation=data['generation'],
        national_number=data['nationalNumber'],
        name=data['name'],
        special_name=data['specialName'],
        species=data['species'],
        height=data['height'],
        weight=data['weight'],
        special_abilities=data['specialAbilities'],
        hidden_ability=data['hiddenAbility'],
        pokemon_type=data['type'],
        hp=data['hp'],
        attack=data['attack'],
        defense=data['defense'],
        special_attack=data['specialAttack'],
        special_defense=data['specialDefense'],
        speed=data['speed'],
        catch_rate=data['catchRate'],
        ev_yield=data['evYield'],
        base_friendship=data['baseFriendship'],
        base_exp=data['baseExp'],
        growth_rate=data['growthRate'],
        egg_groups=data['eggGroups'],
        gender=data['gender'],
        egg_cycles=data['eggCycles'],
        moves_learned_at_level=data['movesLearnedAtLevel'],
        moves_learned_on_evolution=data['movesLearnedOnEvolution'],
        moves_learned_by_eggs=data['movesLearnedByEggs'],
        moves_learned_by_tutor=data['movesLearnedByTutor'],
        moves_learned_by_tm=data['movesLearnedByTm'],
        evolutions=data['evolutions']
    )
