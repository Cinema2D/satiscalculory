"""
SatisfactoryItem.py
"""

from typing import override

# TODO: Change the tuples to be [str, float].
class Recipe:
    def __init__(self, name: str, ingredients: list[tuple[str, int]] = None, facility: tuple[str, int] | None = None,
                 products: list[tuple[str, int]] = None) -> None:
        if ingredients is None:
            ingredients = []

        if products is None:
            products = []

        self.name: str = name
        self.ingredients: list[tuple[str, int]] = ingredients
        self._facility: tuple[str, int] | None = facility
        self.products: list[tuple[str, int]] = products

    @override
    def __repr__(self) -> str:
        return(f"\n"
               f"--- {self.name}\n"
               f"-- Ingredients\n"
               f"{self.ingredients}\n"
               f"-- Products\n"
               f"{self.products}\n")

    def add_ingredient(self, name: str, rate: int) -> None:
        for ingredient_name, _ in self.ingredients:
            if name == ingredient_name:
                raise ValueError("That ingredient is already apart of this recipe.")

        self.ingredients.append((name, rate))

    def remove_ingredient(self, name: str) -> bool:
        for ingredient_name, rate in self.ingredients:
            if name == ingredient_name:
                self.ingredients.remove((ingredient_name, rate))
                return True

        else:
            return False

    @property
    def facility(self) -> tuple[str, int]:
        return self._facility

    @facility.setter
    def facility(self, new_facility: tuple[str, int]) -> None:
        corrected_int: int | None = None

        if not isinstance(new_facility, tuple):
            raise TypeError("The argument for \"new_facility\" must be a tuple.")

        if len(new_facility) != 2:
            raise ValueError("The length of the tuple for \"new_facility\" must have a length of 2!")

        if not isinstance(new_facility[0], str):
            raise TypeError("The first value of the tuple for \"new_facility\" must be of type \"str\".")

        if not isinstance(new_facility[1], int):
            try:
                # If it's a float or a string, we'll try to convert it to an int before going crazy.
                corrected_int = int(new_facility[1])

            except ValueError:
                raise TypeError("The second value of the tuple for \"new_facility\" must be of type \"int\".")

        self._facility = (new_facility[0], new_facility[1] if corrected_int is not None else corrected_int)

    def add_product(self, name: str, rate: int) -> None:
        for product_name, _ in self.products:
            if name == product_name:
                raise ValueError("That product is already apart of this recipe.")

        self.products.append((name, rate))

    def remove_product(self, name: str) -> bool:
        for product_name, rate in self.ingredients:
            if name == product_name:
                self.products.remove((product_name, rate))
                return True

        else:
            return False

class SatisfactoryItem:
    def __init__(self, name: str, stack_size: int | float = 1, sink_points: int | float = 0) -> None:
        self.name: str = name
        self.stack_size: int = int(stack_size)
        self.sink_points: int = int(sink_points)

        self.recipes: list[Recipe] = []

    def add_recipe(self, name: str, ingredients: list[tuple[str, int]], facility: tuple[str, int] | None,
                   products: list[tuple[str, int]]) -> None:
        for recipe in self.recipes:
            if name == recipe.name:
                raise ValueError("A recipe with that name already exists.")

        self.recipes.append(Recipe(name, ingredients, facility, products))
