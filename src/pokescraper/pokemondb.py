import requests
from pokemon import Pokemon
from bs4 import BeautifulSoup, Tag, ResultSet
from enum_name_gen import generate_pokemon_enum_name, generate_move_enum_name
from evolution_constraint import EvolutionConstraint
from move import Move
from pokemon_sprite import PokemonSprite
import json

from src.pokescraper.file_manager import load_pokemon_from_file, write_pokemon_to_json

POKEMONDB_POKEDEX_URL = "https://pokemondb.net/pokedex"
POKEMONDB_MOVE_URL = "https://pokemondb.net/move/all"
POKEMONDB_ABILITY_URL = "https://pokemondb.net/ability/"
POKEMONDB_SPRITES_URL = "https://img.pokemondb.net/sprites"
POKEMONDB_EVOLUTIONS_BY_LEVEL = "https://pokemondb.net/evolution/level"
POKEMONDB_EVOLUTIONS_BY_STONE = "https://pokemondb.net/evolution/stone"
POKEMONDB_EVOLUTIONS_BY_TRADING = "https://pokemondb.net/evolution/trade"
POKEMONDB_EVOLUTIONS_BY_FRIENDSHIP = "https://pokemondb.net/evolution/friendship"
POKEMONDB_EVOLUTIONS_BY_OTHER = "https://pokemondb.net/evolution/status"


def fetch_pokemon_details_from_pokemondb(pokemon: Pokemon) -> tuple:
    print(f"Fetching details for pokemon {pokemon.name} {pokemon.special_name} at {POKEMONDB_POKEDEX_URL}/{pokemon.get_url_name()}")
    url = f"{POKEMONDB_POKEDEX_URL}/{pokemon.get_url_name()}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    move_tables = dict()

    soup_move_tables = soup.find("div", {"class": "tabset-moves-game"}).findChildren("table", {"class": "data-table"})
    soup_move_tables = soup_move_tables[0].parent.parent.parent.findChildren("table", {"class": "data-table"})

    for table in soup_move_tables:
        move_tables[table.parent.find_previous("h3").text] = table.find("tbody").findChildren("tr")

    target_panel = get_target_panel(soup, pokemon)
    vitals_tables = target_panel.findChildren("table", {"class": "vitals-table"})

    generation = int(soup.find("main").find("abbr").text.split("Generation ")[1])
    if "Mega" in pokemon.name:
        generation = 6

    pokemon.generation = generation
    get_species(vitals_tables[0], pokemon)
    get_height(vitals_tables[0], pokemon)
    get_weight(vitals_tables[0], pokemon)
    get_special_abilities(vitals_tables[0], pokemon)
    get_hidden_ability(vitals_tables[0], pokemon)
    get_catch_rate(vitals_tables[1], pokemon)
    get_ev_yield(vitals_tables[1], pokemon)
    get_base_exp(vitals_tables[1], pokemon)
    get_base_friendship(vitals_tables[1], pokemon)
    get_growth_rate(vitals_tables[1], pokemon)
    get_egg_groups(vitals_tables[2], pokemon)
    get_gender(vitals_tables[2], pokemon)
    get_egg_cycles(vitals_tables[2], pokemon)
    get_moves_learned_by_level(move_tables, pokemon)
    get_moves_learned_by_tm(move_tables, pokemon)
    get_moves_learned_on_evolution(move_tables, pokemon)
    get_moves_learned_by_eggs(move_tables, pokemon)
    get_moves_learned_by_tutor(move_tables, pokemon)

    print(f"Finished getting details for pokemon {pokemon.name} {pokemon.special_name}")


def get_species(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        text = vitals_table.findChildren("tr")[2].find("td").text
        pokemon.species = text
    except:
        print(f"\033[91mError getting species for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_height(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        text = vitals_table.findChildren("tr")[3].find("td").text
        pokemon.height = text
    except:
        print(f"\033[91mError getting height for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_weight(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        text = vitals_table.findChildren("tr")[3].find("td").text
        pokemon.weight = text
    except:
        print(f"\033[91mError getting weight for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_special_abilities(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        ability_thing = vitals_table.findChildren("tr")[5].find("td")
        special_abilities = ability_thing.findChildren("span")
        special_abilities = [s.text.split(". ")[1] for s in special_abilities]

        pokemon.special_abilities = special_abilities
    except:
        print(f"\033[91mError getting special abilities for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_hidden_ability(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        ability_thing = vitals_table.findChildren("tr")[5].find("td")
        hidden_ability_thing = ability_thing.find("small")
        hidden_ability = hidden_ability_thing.find("a").text if hidden_ability_thing is not None else None

        pokemon.hidden_ability = hidden_ability
    except:
        print(f"\033[91mError getting hidden ability for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_catch_rate(vitals_table: Tag, pokemon: Pokemon):
    try:
        catch_rate = None
        text = vitals_table.findChildren("tr")[1].find("td").find(text=True)
        if "—" not in text:
            catch_rate = int(text)

        pokemon.catch_rate = catch_rate
    except Exception as e:
        print(f"\033[91mError getting catch rate for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_base_exp(vitals_table: Tag, pokemon: Pokemon):
    try:
        base_exp = None
        text = vitals_table.findChildren("tr")[3].find("td").text

        if '—' not in text:
            base_exp = int(text)

        pokemon.base_exp = base_exp
    except:
        print(f"\033[91mError getting base exp for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_base_friendship(vitals_table: Tag, pokemon: Pokemon):
    try:
        base_friendship = None
        text = vitals_table.findChildren("tr")[2].find("td").find(text=True)

        if "—" not in text:
            base_friendship = int(text)

        pokemon.base_friendship = base_friendship
    except:
        print(f"\033[91mError getting base friendship for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_growth_rate(vitals_table: Tag, pokemon: Pokemon):
    try:
        growth_rate = None
        text = vitals_table.findChildren("tr")[4].find("td").text

        if "—" not in text:
            growth_rate = text

        pokemon.growth_rate = growth_rate
    except:
        print(f"\033[91mError getting growth rate for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_target_panel(soup: BeautifulSoup, pokemon: Pokemon):
    target_panel = None
    tabs = soup.find("div", {"class": "sv-tabs-tab-list"}).findChildren("a")
    panels = soup.find("div", {"class": "sv-tabs-panel-list"}).findChildren("div", {"class": "sv-tabs-panel"}, recursive=False)

    for i, a in enumerate(tabs):
        if pokemon.special_name is not None:
            if a.text == pokemon.special_name:
                target_panel = panels[i]
                break
        else:
            if a.text in pokemon.name:
                target_panel = panels[i]
                break

    return target_panel


def get_ev_yield(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        ev_yield = dict()
        ev_yield_strings = vitals_table.findChildren("tr")[0].find("td").text.split(",")
        if "—" not in ev_yield_strings[0]:
            for ev_yield_string in ev_yield_strings:
                ev_yield[ev_yield_string[2:].strip()] = int(ev_yield_string[:2])

        pokemon.ev_yield = ev_yield
    except:
        print(f"\033[91mError getting ev yield for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_egg_cycles(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        egg_cycles = None
        text = vitals_table.findChildren("tr")[2].find("td").find(text=True)

        if "—" not in text:
            egg_cycles = int(text)

        pokemon.egg_cycles = egg_cycles
    except:
        print(f"\033[91mError getting egg cycles for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_egg_groups(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        egg_groups_thing = vitals_table.findChildren("tr")[0].find("td")
        egg_groups = [a.text for a in egg_groups_thing.findChildren("a")]
        pokemon.egg_groups = egg_groups
    except:
        print(f"\033[91mError getting egg groups for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_gender(vitals_table: Tag, pokemon: Pokemon) -> None:
    try:
        gender = dict()
        gender_string = vitals_table.findChildren("tr")[1].find("td").text
        gender_strings = gender_string.split(", ")

        if gender_string in ["Genderless", "—"]:
            gender = None
        else:
            gender[gender_strings[0].split(" ")[1]] = gender_strings[0].split(" ")[0]
            gender[gender_strings[1].split(" ")[1]] = gender_strings[1].split(" ")[0]

        pokemon.gender = gender
    except:
        print(f"\033[91mError getting gender for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_moves_learned_by_level(move_tables: dict, pokemon: Pokemon) -> None:
    try:
        moves_dict = dict()

        for m in move_tables['Moves learnt by level up']:
            values = m.findChildren("td", recursive=False)
            level = int(values[0].text)
            move_name = values[1].text
            move_enum_name = generate_move_enum_name(move_name)
            moves_dict[move_enum_name] = level

        pokemon.moves_learned_at_level = moves_dict
    except KeyError as e:
        print(f"\033[93mPokemon {pokemon.name} does not have moves learned by level\033[0m")
    except Exception as e:
        print(f"\033[91mError getting moves learned by level for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_moves_learned_by_tm(move_tables: dict, pokemon: Pokemon) -> None:
    try:
        moves_dict = dict()

        for m in move_tables['Moves learnt by TM']:
            values = m.findChildren("td", recursive=False)
            tm = int(values[0].text)
            move_name = values[1].text
            move_enum_name = generate_move_enum_name(move_name)
            moves_dict[move_enum_name] = tm

        pokemon.moves_learned_by_tm = moves_dict
    except KeyError as e:
        print(f"\033[93mPokemon {pokemon.name} does not have moves learned by tm\033[0m")
    except Exception as e:
        print(f"\033[91mError getting moves learned by tm for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_moves_learned_on_evolution(move_tables: dict, pokemon: Pokemon) -> None:
    try:
        moves = list()

        for m in move_tables['Moves learnt on evolution']:
            values = m.findChildren("td", recursive=False)
            move_name = values[0].text
            move_enum_name = generate_move_enum_name(move_name)
            moves.append(move_enum_name)

        pokemon.moves_learned_on_evolution = moves
    except KeyError as e:
        print(f"\033[93mPokemon {pokemon.name} does not have moves learned on evolution\033[0m")
    except Exception as e:
        print(f"\033[91mError getting moves learned on evolution for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_moves_learned_by_eggs(move_tables: dict, pokemon: Pokemon) -> None:
    try:
        moves = list()

        for m in move_tables['Egg moves']:
            values = m.findChildren("td", recursive=False)
            move_name = values[0].text
            move_enum_name = generate_move_enum_name(move_name)
            moves.append(move_enum_name)

        pokemon.moves_learned_by_eggs = moves
    except KeyError as e:
        print(f"\033[93mPokemon {pokemon.name} does not have moves learned by egg\033[0m")
    except Exception as e:
        print(f"\033[91mError getting moves learned by egg for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def get_moves_learned_by_tutor(move_tables: dict, pokemon: Pokemon) -> None:
    try:
        moves = list()

        for m in move_tables['Move Tutor moves']:
            values = m.findChildren("td", recursive=False)
            move_name = values[0].text
            move_enum_name = generate_move_enum_name(move_name)
            moves.append(move_enum_name)

        pokemon.moves_learned_by_tutor = moves
    except KeyError as e:
        print(f"\033[93mPokemon {pokemon.name} does not have moves learned by tutor\033[0m")
    except Exception as e:
        print(f"\033[91mError getting moves learned by tutor for pokemon {pokemon.name} {pokemon.special_name}\033[0m")


def fetch_all_pokemon_base_stats_from_pokemondb_pokedex(url: str = f"{POKEMONDB_POKEDEX_URL}/all"):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pokedex = soup.find(id="pokedex").find("tbody").findChildren("tr", recursive=False)
    pokemon = []

    for i, e in enumerate(pokedex):
        elements = e.findChildren("td", recursive=False)

        national_number = int(elements[0].findChildren("span", recursive=False)[1].text)
        name = elements[1].find("a").text
        pokemon_type = [e.text for e in elements[2].findChildren("a", recursive=False)]
        hp = int(elements[4].text)
        attack = int(elements[5].text)
        defense = int(elements[6].text)
        special_attack = int(elements[7].text)
        special_defense = int(elements[8].text)
        speed = int(elements[9].text)
        special_name = elements[1].find("small").text if elements[1].find("small") is not None else None

        pokemon.append(Pokemon(
            national_number=national_number,
            name=name,
            special_name=special_name,
            pokemon_type=pokemon_type,
            hp=hp,
            attack=attack,
            defense=defense,
            special_attack=special_attack,
            special_defense=special_defense,
            speed=speed
        ))

    return pokemon


def fetch_moves_from_pokemondb() -> list:
    response = requests.get(POKEMONDB_MOVE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find(id="moves").find("tbody").findChildren("tr", recursive=False)
    moves = []

    for i, e in enumerate(table):
        elements = e.findChildren("td", recursive=False)
        category = None if elements[2].text.find("—") == 0 else elements[2].find("img")['title']
        effect_description = elements[6].text

        if category:
            name = elements[0].find("a").text
            type = elements[1].find("a").text
            category = None if elements[2].text.find("—") == 0 else elements[2].find("img")['title']
            power = None if elements[3].text.find("—") == 0 else int(elements[3].text)
            accuracy = None if elements[4].text.find("—") == 0 or elements[4].text.find("∞") == 0 else int(elements[4].text)
            pp = None if elements[5].text.find("—") == 0 else int(elements[5].text)
            probability = None if elements[7].text.find("—") == 0 else int(elements[7].text)
            is_high_crit = True if effect_description.find("High critical hit ratio") == 0 else False

            moves.append(
                Move(name, type, category, power, accuracy, pp, effect_description, probability, is_high_crit)
            )

    return moves


# def fetch_sprites_from_pokemondb(pokemon: list) -> list:
#     print("fetching sprites")
#
#     for i, e in enumerate(pokemon):
#         print(f"fetching sprites for {e.name}")
#         front_normal = requests.get(POKEMONDB_SPRITES_URL + "/black-white/normal/" + e.name.lower() + ".png")
#         front_shiny = requests.get(POKEMONDB_SPRITES_URL + "/black-white/shiny/" + e.name.lower() + ".png")
#         front_anim_normal = requests.get(POKEMONDB_SPRITES_URL + "/black-white/anim/normal/" + e.name.lower() + ".gif")
#         front_anim_shiny = requests.get(POKEMONDB_SPRITES_URL + "/black-white/anim/shiny/" + e.name.lower() + ".gif")
#
#         test = shutil.copyfileobj(front_normal.raw, '')
#
#         if front_normal.status_code == 200:
#             e.sprites.append(PokemonSprite(front_normal.content, "image/png", f"{e.name}_front_normal"))
#         if front_shiny.status_code == 200:
#             e.sprites.append(PokemonSprite(front_shiny.content, "image/png", f"{e.name}_front_shiny"))
#         if front_anim_normal.status_code == 200:
#             e.sprites.append(PokemonSprite(front_anim_normal.content, "image/gif", f"{e.name}_front_normal"))
#         if front_anim_shiny.status_code == 200:
#             e.sprites.append(PokemonSprite(front_anim_shiny.content, "image/gif", f"{e.name}_front_normal"))
#
#         print(f"fetched sprites for {e.name}")
#
#     print("fetched sprites")
#     return pokemon


def fetch_evolutions_by_level(url: str = POKEMONDB_EVOLUTIONS_BY_LEVEL) -> None:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    evolution_table = soup.find("table", {"id": "evolution"})
    rows = evolution_table.find("tbody").findChildren("tr", recursive=False)

    for i, e in enumerate(rows):
        values = rows[i].findChildren("td")
        evolution_from = values[0].findChildren("span")[1].find("a").text
        evolution_to = values[2].findChildren("span")[1].find("a").text
        level = int(values[3].text)
        evolution_from_enum_name = generate_pokemon_enum_name(evolution_from)
        evolution_to_enum_name = generate_pokemon_enum_name(evolution_to)
        enum_name = generate_pokemon_enum_name(evolution_from_enum_name)

        pokemon = load_pokemon_from_file(f"{enum_name}.json")
        pokemon.evolutions[evolution_to_enum_name] = EvolutionConstraint(
            level=level
        )
        write_pokemon_to_json(pokemon)


def fetch_evolutions_by_elemental_stone(url: str = POKEMONDB_EVOLUTIONS_BY_STONE):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    evolution_table = soup.find("table", {"id": "evolution"})
    rows = evolution_table.find("tbody").findChildren("tr", recursive=False)

    for i, e in enumerate(rows):
        values = rows[i].findChildren("td")
        evolution_from = values[0].findChildren("span")[1].find("a").text
        evolution_to = values[2].findChildren("span")[1].find("a").text
        item = values[3].text.split(",")[0]
        evolution_from_enum_name = generate_pokemon_enum_name(evolution_from)
        evolution_to_enum_name = generate_pokemon_enum_name(evolution_to)
        enum_name = generate_pokemon_enum_name(evolution_from_enum_name)

        pokemon = load_pokemon_from_file(f"{enum_name}.json")
        pokemon.evolutions[evolution_to_enum_name] = EvolutionConstraint(
            used_item=item
        )
        write_pokemon_to_json(pokemon)
