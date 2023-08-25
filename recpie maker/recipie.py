import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import pyttsx3

recognizer = sr.Recognizer()


def search_recipe(item):
    search_recipe_link = f"https://tasty.co/search?q={item}&sort=popular"
    response = requests.get(url=search_recipe_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    searched_elements = soup.select(".feed-item__title")
    recipe_items = soup.select(".feed-item.feed-item__4-col")
    found_recipes = False

    for idx, name in enumerate(searched_elements):
        if item.lower() in name.text.lower():
            print(idx + 1, name.text.strip())
            found_recipes = True

    if not found_recipes:
        raise Exception("Food not found")

    recipe_links = []
    for name in recipe_items:
        recipe_link = name.a['href']
        recipe_links.append(recipe_link)

    return recipe_links


def scrape_ingredients(recipe_links, recipe_index):
    if 1 <= recipe_index <= len(recipe_links):
        recipe_link = "https://tasty.co" + recipe_links[recipe_index - 1]
        response = requests.get(url=recipe_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        food_elements = soup.select(".list-unstyled.xs-text-3")
        title_element = soup.select(".recipe-name.extra-bold.xs-mb05.md-mb1")
        description_element = soup.select(
            ".description.xs-text-4.md-text-3.lg-text-2.xs-mb2.lg-mb2.lg-pb05")
        print("\n" + "*" * 70)
        print("\n", title_element[0].text.strip())
        print("\n" + "*" * 70)
        print("\n" + description_element[0].text.strip() + "\n")
        print("\nIngredients\n")
        for idx, _ in enumerate(food_elements):
            print("* " + food_elements[idx].text.strip())
            print()
            engine.say(food_elements[idx].text.strip())
            engine.runAndWait()
            engine.stop()
    else:
        print("Invalid recipe index. Please select a valid index.")


if __name__ == "__main__":
    engine = pyttsx3.init(driverName='sapi5')
    with sr.Microphone() as source:
        print("Tell Food Name...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"Your {text} recipe is here")
        recipe_links = search_recipe(text)
        recipe_index = int(
            input("Enter the index of the recipe you want to view the ingredients for: "))
        scrape_ingredients(recipe_links, recipe_index)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except ValueError:
        print("Invalid input. Please enter a valid recipe index.")
    except Exception as e:
        print(e)
