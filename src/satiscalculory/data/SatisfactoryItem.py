"""
SatisfactoryItem.py
"""
from typing import override

# TODO: Change the tuples to be [str, float].
class Recipe:
    def __init__(self, name: str, ingredients: list[tuple[str, float]] = None, facility: tuple[str, float] | None = None,
                 products: list[tuple[str, float]] = None) -> None:
        if ingredients is None:
            ingredients = []

        if products is None:
            products = []

        self.name: str = name
        self.ingredients: list[tuple[str, float]] = ingredients
        self._facility: tuple[str, float] | None = facility
        self.products: list[tuple[str, float]] = products

    @override
    def __str__(self) -> str:
        return(f"\n"
               f"{self.name}\n"
               f"| Ingredients\n"
               f"|| {self.ingredients}\n"
               f"| Products\n"
               f"|| {self.products}\n")

    @override
    def __repr__(self) -> str:
        return f"{self.__class__}: {self.__dict__}"

    def add_ingredient(self, name: str, rate: float) -> None:
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
    def facility(self) -> tuple[str, float]:
        return self._facility

    @facility.setter
    def facility(self, new_facility: tuple[str, float]) -> None:
        corrected_float: float | None = None

        if not isinstance(new_facility, tuple):
            raise TypeError("The argument for \"new_facility\" must be a tuple.")

        if len(new_facility) != 2:
            raise ValueError("The length of the tuple for \"new_facility\" must have a length of 2!")

        if not isinstance(new_facility[0], str):
            raise TypeError("The first value of the tuple for \"new_facility\" must be of type \"str\".")

        if not isinstance(new_facility[1], float):
            try:
                # If it's a float or a string, we'll try to convert it to an int before going crazy.
                corrected_float = float(new_facility[1])

            except ValueError:
                raise TypeError("The second value of the tuple for \"new_facility\" must be of type \"int\".")

        self._facility = (new_facility[0], new_facility[1] if corrected_float is not None else corrected_float)

    def add_product(self, name: str, rate: float) -> None:
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

    def __str__(self) -> str:
        return f"{self.name}\n| Stack size: {self.stack_size}\n| Sink points: {self.sink_points}"

    def add_recipe(self, name: str, ingredients: list[tuple[str, float]], facility: tuple[str, float] | None,
                   products: list[tuple[str, float]]) -> None:
        # My reason for this is because an x is added to the end of the name for each duplicate. However, I want there
        # to be a space between the actual name and any xs, so they can be removed easily later. Therefore, I add
        # a space now, and strip it later. Stripping it will only do something if no xs were added, so we don't have any
        # trailing whitespace.
        name += " "

        for recipe in self.recipes:
            while True:
                if name == recipe.name:
                    name += "x"

                else:
                    break

        name.strip()

        new_recipe: Recipe = Recipe(name, ingredients, facility, products)
        self.recipes.append(new_recipe)
