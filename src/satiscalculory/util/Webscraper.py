"""
Webscraper.py
"""

from bs4 import BeautifulSoup, NavigableString, ResultSet
import re
import requests
from requests import Response
from typing import Any


class Webscraper:
    @staticmethod
    def scrape_item_information(url: str) -> dict[str:str | float]:
        """
        Scrapes item information from the item's wiki page on satisfactory.wiki.gg.
        :param url: The item's URL on the wiki. Example: https://satisfactory.wiki.gg/wiki/Adaptive_Control_Unit.
        :return: A dictionary containing the item's name, stack size, and sink points.
        """
        def comma_str_to_float(text: str) -> float:
            """
            Converts a string containing a number with commas to a float. This function will not work if the string has
            text other than the number in it. Will pass a number with no commas through normally.
            :param text: The number (as a string) to convert.
            :return: The number as a proper float.
            """
            result: float = 0.0

            if text:
                split_numbers: list[str] = str.split(text, ",")
                number_string: str = ""


                for item in split_numbers:
                    number_string += item

                result = float(number_string)

            return result

        response: Response = requests.get(url)
        if response.status_code != 200:
            raise TimeoutError(f"Failed to fetch {url}")

        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        page_aside: BeautifulSoup | NavigableString | None = soup.find("aside", class_="portable-infobox noexcerpt pi-background pi-theme-default pi-layout-default")

        return {
            "name": page_aside.find_all()[0].text,
            "stack size": comma_str_to_float(soup.find(string="Stack size").find_next().text),
            "sink points": comma_str_to_float(soup.find(string="Sink points").find_next().text)
        }

    @staticmethod
    def scrape_recipe_information(url: str):
        response: Response = requests.get(url)
        if response.status_code != 200:
            raise TimeoutError(f"Failed to fetch {url}")

        soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        recipe_wiki_table = soup.find(id="Crafting").find_next("table")

        dirty_recipe_table = []
        recipes = {}

        def extract_recipe_items(item_cell: str) -> dict[str:dict[str:float]]:
            """
            Separates and organizes the information extracted regarding recipes.
            :param item_cell: The cell which contains the ingredients or products of the recipe.
            :return: The ingredient data, sorted.
            """
            # Splits each "informational item".
            split_items = re.findall(r"\d*\D+", item_cell)
            dirty_ingredients = []

            # Gathers related items together.
            for i in range(len(split_items)):
                if i % 2 == 0:
                    dirty_ingredients.append((split_items[i], split_items[i + 1]))

            clean_ingredients = {}

            for i, ii in dirty_ingredients:
                split_string_1 = str.split(i, "×")
                split_string_2 = str.split(ii, "/")

                clean_ingredients[split_string_1[1].strip()] = {
                    "rate": float(split_string_2[0].strip()),
                    "amount": float(split_string_1[0].strip())
                }

            return clean_ingredients

        def extract_facility_items(item_cell: str) -> list[str | float]:
            facility_info = re.findall(r"\d*\D+", item_cell)

            # Some recipes can be made manually with the Craft Bench or the Equipment Workshop in addition to an automatic
            # facility. When this is the case, the name of that manual facility gets tacked on to the end of the automatic
            # facility.
            #
            # facility_info[1] generally looks something like "12 sec". Since no facility takes more than 999 seconds to
            # cycle once (without under-clocking), the length of facility_info[1] should never be more than 7 characters. If
            # it is, we know that the manual facility was tacked on, which means we need to remove it.
            if len(facility_info[1]) > 7:
                # If this is the case, then facility_info[1] will look something like "12 secCraftBench × ". So, the first
                # thing we do is remove the " × " from it, since we always know its length.
                facility_info[1] = facility_info[1][:-3]

                # Now that the manual facility is at the end, we can cut it off easier.
                if facility_info[1].endswith("Craft Bench"):
                    facility_info[1] = facility_info[1][:-len("Craft Bench")]

                elif facility_info[1].endswith("Equipment Workshop"):
                    facility_info[1] = facility_info[1][:-len("Equipment Workshop")]

            # Finally, we remove the " sec" and convert it to a float, regardless of the conditions above.
            facility_info[1] = float(facility_info[1][:-4])

            return facility_info

        def rchop(name: str) -> str:
            """
            Cuts off the "Alternate" that gets included in some recipe names when they're scraped from the wiki.
            :param name: The string to check.
            :return: The string, cleaned.
            """
            result: str = name

            if name.endswith("Alternate"):
                result = name[:-len("Alternate")]

            return result

        if recipe_wiki_table:
            rows: ResultSet[Any] = recipe_wiki_table.find_all("tr")

            for row in rows:
                cells = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                dirty_recipe_table.append(cells)

            # Removes the column headers.
            dirty_recipe_table.pop(0)

            # Removes the "Unblocked by" column from each row.
            for item in dirty_recipe_table:
                item.pop(-1)

            clean_recipe_table: list[list[str]] = []

            # Removes the regular expressions from the table.
            for i in range(len(dirty_recipe_table)):
                for info_item in dirty_recipe_table[i]:
                    try:
                        clean_recipe_table[i].append(re.sub(r"\xa0", " ", info_item))

                    except IndexError:
                        clean_recipe_table.append([])
                        clean_recipe_table[i].append(re.sub(r"\xa0", " ", info_item))

            for recipe in clean_recipe_table:

                facility_info: list[str | float] = extract_facility_items(recipe[2])

                recipes[rchop(recipe[0])] = {
                    "facility": {"name": facility_info[0], "time": facility_info[1]},
                    "ingredients": extract_recipe_items(recipe[1]),
                    "products": extract_recipe_items(recipe[3])
                }

            return recipes