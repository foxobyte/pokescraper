import requests
import json

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


def write_pokemon_to_json(pokemon: Pokemon, directory: str = "./pokemon") -> None:
    with open(f"{directory}/{pokemon.get_enum_name()}.json", "w") as file:
        file.write(pokemon.to_json())


def write_pokemon_list_to_json(pokemon_list: list, directory: str = "./pokemon") -> None:
    for pokemon in pokemon_list:
        write_pokemon_to_json(pokemon, directory)


def generate_moves_json(moves_list: list) -> None:
    for i, e in enumerate(moves_list):
        with open(f"./moves/{e.get_enum_name()}.json", 'w') as file:
            file.write(e.to_json())


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


if __name__ == '__main__':
    # moves = fetch_moves_from_pokemondb()
    # generate_moves_json(moves)
    moves = load_all_moves()

    # pokemon_list = fetch_all_pokemon_base_stats_from_pokemondb_pokedex()

    # test_pokemon = load_pokemon_from_file("IRON_LEAVES.json")
    # fetch_pokemon_details_from_pokemondb(test_pokemon)
    # write_pokemon_to_json(test_pokemon)

    # pokemon_list = load_all_pokemon()
    # for pokemon in pokemon_list:
    #     fetch_pokemon_details_from_pokemondb(pokemon)
    #     write_pokemon_to_json(pokemon)

    # generate_pokemon_json(pokemon_list)

    fetch_evolutions_by_level()
    # fetch_evolutions_by_elemental_stone()

    # pokemon = fetch_pokemon()
    # pokemon = fetch_sprites_from_pokemondb(pokemon[:1])
    # post_sprites(pokemon)

