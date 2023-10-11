import requests
import json
import yaml

from os import listdir
from os.path import isfile, join

from pokemon import Pokemon
from move import Move
from pokemon_sprite import PokemonSprite
from src.pokescraper.pokemondb import fetch_all_pokemon_base_stats_from_pokemondb_pokedex, fetch_moves_from_pokemondb, \
    fetch_pokemon_details_from_pokemondb, fetch_evolutions_by_level


def post_sprites(pokemon: list, url: str = "http://localhost:8080/api/v1/sprites") -> None:
    for i, e in enumerate(pokemon):
        for sprite in e.sprites:
            data = {
                "image": sprite.image,
                "pokemonId": e.pokemon_id
            }

            requests.post(url, headers={'Content-Type': 'application/octet-stream'}, data=data)


def post_pokemon(pokemon_list: list, url: str = "http://localhost:8080/api/v1/pokemon") -> None:
    for pokemon in pokemon_list:
        requests.post(url, data=pokemon.to_json())


def write_pokemon_to_json(pokemon: Pokemon, directory: str = "./pokemon/json") -> None:
    with open(f"{directory}/{pokemon.get_enum_name()}.json", "w") as file:
        file.write(pokemon.to_json())


def write_pokemon_list_to_json(pokemon_list: list, directory: str = "./pokemon/json") -> None:
    for pokemon in pokemon_list:
        write_pokemon_to_json(pokemon, directory)


def write_pokemon_to_yaml(pokemon: Pokemon, directory: str = "./pokemon/properties") -> None:
    try:
        with open(f"{directory}/{pokemon.get_enum_name()}.yaml", "w") as file:
            file.write(pokemon.to_yaml())
    except Exception as e:
        print(e)


def write_pokemon_list_to_yaml(pokemon_list: list, directory: str = "./pokemon/properties") -> None:
    for pokemon in pokemon_list:
        write_pokemon_to_yaml(pokemon)


def load_pokemon_from_file(file_name: str, directory: str = "./pokemon") -> Pokemon:
    try:
        with open(f"{directory}/{file_name}", "r") as file:
            data = json.loads(file.read())
            return build_pokemon_from_json(data)
    except:
        print()


def load_all_pokemon(directory: str = "./pokemon") -> list:
    files = [file_name for file_name in listdir(directory) if isfile(join(directory, file_name))]
    pokemon_list = []

    for file_name in files:
        pokemon_list.append(load_pokemon_from_file(file_name, directory))

    return pokemon_list


def generate_move_json(move: Move, directory: str = "./moves/json") -> None:
    try:
        with open(f"{directory}/{move.get_enum_name()}.json", 'w') as file:
            file.write(move.to_json())
    except:
        print()


def generate_moves_json(moves: list, directory: str = "./moves/json") -> None:
    for move in moves:
        generate_move_json(move, directory)


def generate_move_yaml(move: Move, directory: str = "./moves/properties") -> None:
    try:
        with open(f"{directory}/{move.get_enum_name()}.yaml", "w") as file:
            file.write(move.to_yaml())
    except Exception as e:
        print(e)


def generate_moves_yaml(moves: list, directory: str = "./moves/properties") -> None:
    for move in moves:
        generate_move_yaml(move, directory)


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


def load_move_from_file(file_name: str, directory: str = "./moves") -> Move:
    with open(f"{directory}/{file_name}", "r") as file:
        data = json.loads(file.read())
        return build_move_from_json(data)


def load_all_moves(directory: str = "./moves") -> list:
    files = [file_name for file_name in listdir(directory) if isfile(join(directory, file_name))]
    moves = []

    for file_name in files:
        moves.append(load_move_from_file(file_name, directory))

    return moves


def build_move_from_json(data: dict) -> Move:
    return Move(
        name=data['name'],
        move_type=data['type'],
        category=data['category'],
        power=data['power'],
        accuracy=data['accuracy'],
        pp=data['pp'],
        effect_description=data['effectDescription'],
        probability=data['probability'],
        is_high_crit=data['isHighCrit']
    )


def post_moves(moves: list, url: str = "http://localhost:8080/api/v1/move"):
    headers = {
        'Content-Type': 'application/json'
    }
    moves = [move.fix_keys() for move in moves]
    moves = requests.post(url, json=moves, headers=headers)


if __name__ == '__main__':
    moves = fetch_moves_from_pokemondb()
    moves = post_moves(moves)
    # generate_moves_yaml(moves)
    # moves = load_all_moves()

    # pokemon_list = fetch_all_pokemon_base_stats_from_pokemondb_pokedex()

    # test_pokemon = load_pokemon_from_file("IRON_LEAVES.json")
    # fetch_pokemon_details_from_pokemondb(test_pokemon)
    # write_pokemon_to_json(test_pokemon)

    # pokemon_list = load_all_pokemon()
    # for pokemon in pokemon_list:
    #     fetch_pokemon_details_from_pokemondb(pokemon)
    #     write_pokemon_to_yaml(pokemon)

    # generate_pokemon_json(pokemon_list)

    # fetch_evolutions_by_level()
    # fetch_evolutions_by_elemental_stone()

    # pokemon = fetch_pokemon()
    # pokemon = fetch_sprites_from_pokemondb(pokemon[:1])
    # post_sprites(pokemon)

