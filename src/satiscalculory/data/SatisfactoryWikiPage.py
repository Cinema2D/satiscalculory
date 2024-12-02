"""
SatisfactoryWikiPage.py
"""

from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag
import re
import requests
from requests import Response
from typing import Any

from .SatisfactoryItem import SatisfactoryItem


class SatisfactoryWikiPage:
    # TODO: Currently, there's too much tuples being converted to lists and back. I need to figure out a better way of
    #  doing this.
    def __init__(self, url: str) -> None:
        """

        :param url: The URL of the page.
        :raises TimeoutError: Raises if the page cannot be reached.
        """
        self.url: str = url

        response: Response = requests.get(self.url)

        if response.status_code != 200:
            raise TimeoutError(f"Failed to fetch {url}!\nStatus code: {response.status_code}")

        self.soup: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        # STEP 1: Retrieve the item's identifying information from the webpage.
        page_aside: BeautifulSoup | NavigableString | None = self.soup.find(
            "aside",
            class_="portable-infobox noexcerpt pi-background pi-theme-default pi-layout-default"
        )

        item_info: list[str | float | int] = []

        try:
            # First thing we look for is the name, which is the first element in the page's aside, if one is present.
            item_info.insert(0, page_aside.find_all()[0].text)

        except AttributeError:
            # If, for some reason, no aside is present, we just insert this to make it obvious.
            item_info.insert(0, "<ItemNameNotFound>")

        try:
            # Next is the item's stack size.
            item_info.insert(1, self._float_str(self.soup.find(string="Stack size").find_next().text))

        except AttributeError:
            # If there's no stack size specified, that means it's 1.
            item_info.insert(1, 1)

        try:
            # Last is the item's sink points.
            item_info.insert(2, self._float_str(self.soup.find(string="Sink points").find_next().text))

        except AttributeError:
            # If no sink points are listed, it means it cannot be sunk, and is therefore worth 0 points.
            item_info.insert(2, 0)

        self.item: SatisfactoryItem = SatisfactoryItem(item_info[0], item_info[1], item_info[2])

        # STEP 2: Retrieve the item's recipes, if any, from the webpage.
        # raw_recipe_table is a mostly unreadable mess of data.
        try:
            raw_recipe_table: Tag | NavigableString | None = self.soup.find(id="Crafting").find_next("table")

        except AttributeError:
            raw_recipe_table = None

        recipe_table = []

        # Sorts the raw table into a more readable format that isn't necessarily usable yet.
        if raw_recipe_table:
            rows: ResultSet[Any] = raw_recipe_table.find_all("tr")

            for row in rows:
                cells = []

                for cell in row.find_all(['th', 'td']):
                    cells.append(cell.text.strip())

                recipe_table.append(cells)

            # Removes the table column headers.
            recipe_table.pop(0)

            for recipe in recipe_table:
                # Removes the "Unlocked by" column from the table, since it's not needed.
                recipe.pop(-1)
                # Removes the regex from the recipe and splits it up.
                for i in range(len(recipe)):
                    recipe[i] = re.sub(r"\xa0", " ", recipe[i])

                # If a recipe is an alternate recipe, that makes its way into the name, so we remove it here, in case.
                recipe[0] = recipe[0].removesuffix("Alternate")

                # Properly spaces the ingredients.
                recipe[1] = re.findall(r"(\d+\.?\d*\s×\s[^0-9]+)(\d+\.?\d*\s/ min)", recipe[1])

                for i in range(len(recipe[1])):
                    # Converts it from a tuple to a list.
                    recipe[1][i] = list(recipe[1][i])

                    # Keeps the name of the item only.
                    recipe[1][i][0] = recipe[1][i][0].split(" × ")[-1]
                    # Keeps the rate of the item only.
                    recipe[1][i][1] = float(recipe[1][i][1].split(" / ")[0])
                    # Converts it to a tuple since it doesn't need to be changed.
                    recipe[1][i] = tuple(recipe[1][i])

                # Removes any manual crafting facilities.
                recipe[2] = recipe[2].split(" × ")[0]

                if recipe[2].endswith("Craft Bench"):
                    recipe[2] = recipe[2][:-len("Craft Bench")]

                elif recipe[2].endswith("Equipment Workshop"):
                    recipe[2] = recipe[2][:-len("Equipment Workshop")]

                # Properly spaces and removes lettering.
                try:
                    recipe[2] = re.split(r"(?<=\d)(?=[a-zA-Z])|(?<=[a-zA-Z])(?=\d)", recipe[2])
                    recipe[2][1] = float(recipe[2][1][:-len("sec")].strip())
                    recipe[2] = tuple(recipe[2])

                except IndexError:
                    recipe[2] = "MANUAL RECIPE"

                # Does the exact same thing we did above with recipe[1].
                recipe[3] = list(re.findall(r"(\d+\.?\d*\s×\s[^0-9]+)(\d+\.?\d*\s/ min)", recipe[3]))

                for i in range(len(recipe[3])):
                    recipe[3][i] = list(recipe[3][i])
                    recipe[3][i][0] = recipe[3][i][0].split(" × ")[-1]
                    recipe[3][i][1] = float(recipe[3][i][1].split(" / ")[0])
                    recipe[3][i] = tuple(recipe[3][i])

                # Creates recipes for these items and adds them to item.
                self.item.add_recipe(recipe[0], recipe[1], recipe[2], recipe[3])

    @staticmethod
    def _float_str(text: str) -> float | bool:
        """
        Converts a string of numbers containing commas to a float. For example, "1,234" -> 1_234.0.

        :param text: The number (as a string).
        :return: The number given as a float or False if it couldn't be converted.
        """
        result: float | bool = 0.0

        if text:
            split_numbers: list[str] = str.split(text, ",")
            number_string: str = ""

            for number in split_numbers:
                number_string += number

            try:
                result = float(number_string)

            except ValueError:
                result = False

        return result



