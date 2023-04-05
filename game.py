import requests
import random

# Fetch data about a random Pokemon
pokemon_id = random.randint(1, 898)
url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
response = requests.get(url)
pokemon_data = response.json()

# Extract the name and image URL of the Pokemon and create a function that displays a partially hidden image of the Pokemon:

pokemon_name = pokemon_data["name"]
pokemon_image_url = pokemon_data["sprites"]["front_default"]

def display_partial_image(pokemon_image_url, percent_hidden):
    """
    Display a partially hidden image of a Pokemon.
    """
    response = requests.get(pokemon_image_url, stream=True)
    total_bytes = len(response.content)
    bytes_to_hide = int(total_bytes * percent_hidden)
    hidden_image_bytes = b"\x00" * bytes_to_hide
    visible_image_bytes = response.content[bytes_to_hide:]
    hidden_image = hidden_image_bytes + visible_image_bytes
    with open("pokemon.png", "wb") as f:
        f.write(hidden_image)

# Create a loop that allows the user to guess the name of the Pokemon:

guesses_left = 5
percent_hidden = 0.5

print("Guess That Pokemon!")
print("You have 5 guesses to guess the name of the Pokemon.")
print("Here's an image of the Pokemon, with 50% of it hidden:")
display_partial_image(pokemon_image_url, percent_hidden)

while guesses_left > 0:
    guess = input("Guess the name of the Pokemon: ").lower()
    if guess == pokemon_name:
        print("Congratulations, you guessed the Pokemon!")
        break
    else:
        guesses_left -= 1
        if guesses_left > 0:
            print(f"Incorrect. You have {guesses_left} guesses left.")
        else:
            print(f"Sorry, you're out of guesses. The Pokemon was {pokemon_name}.")
    percent_hidden += 0.1
    display_partial_image(pokemon_image_url, percent_hidden)
