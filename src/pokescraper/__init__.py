import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pokemon import Pokemon
import json

POKEMONDB_POKEDEX_URL = "https://pokemondb.net/pokedex/all"
POKEMONDB_SPRITES_URL = "https://pokemondb.net/sprites/"

# Create list of pokemon with basic stats
#
def fetch_pokemon_from_pokemondb() -> list:
    response = requests.get(POKEMONDB_POKEDEX_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    pokedex = soup.find(id="pokedex").find("tbody").findChildren("tr", recursive=False)
    pokemon = []

    for i, e in enumerate(pokedex):
        elements = e.findChildren("td", recursive=False)

        national_number = int(elements[0].findChildren("span", recursive=False)[1].text)
        name = elements[1].find("a").text
        type = [e.text for e in elements[2].findChildren("a", recursive=False)]
        hp = int(elements[4].text)
        attack = int(elements[5].text)
        defense = int(elements[6].text)
        spAtk = int(elements[7].text)
        spDef = int(elements[8].text)
        speed = int(elements[9].text)
        special_name = elements[1].find("small")

        if special_name != None:
            name = special_name.text

        pokemon.append(Pokemon(
            national_number, name, type,
            hp, attack, defense,
            spAtk, spDef, speed
        ))

    return pokemon


def fetch_sprites_from_pokemondb(pokemon: list) -> list:
    sprites = []

    for i, e in enumerate(pokemon):
        front_normal = requests.get("https://img.pokemondb.net/sprites/black-white/normal/" + e.name + ".png")
        front_shiny = requests.get("https://img.pokemondb.net/sprites/black-white/shiny/" + e.name + ".png")
        front_anim_normal = requests.get("https://img.pokemondb.net/sprites/black-white/anim/normal/" + e.name + ".gif")
        front_anim_shiny = requests.get("https://img.pokemondb.net/sprites/black-white/anim/shiny/" + e.name + ".gif")
        print()


    return sprites


def fetch_from_pokemon_tcg() -> None:
    return None


def post_pokemon(pokemon: list, url: str = "http://localhost:8080/api/v1/pokemon") -> None:
    headers = {
        "Content-Type": "application/json"
    }

    for i, e in enumerate(pokemon):
        test = e.__dict__
        requests.post(url, json=test)


if __name__ == '__main__':
    pokemon = fetch_pokemon_from_pokemondb()
    # sprites = fetch_sprites_from_pokemondb(pokemon)
    post_pokemon(pokemon)

