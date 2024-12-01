"""
SatisfactoryItem.py
"""


class Recipe:
    def __init__(self) -> None:
        pass


class SatisfactoryItem:
    def __init__(self, name: str, stack_size: int | float = 1, sink_points: int | float = 0) -> None:
        self.name: str = name
        self.stack_size: int = int(stack_size)
        self.sink_points: int = int(sink_points)

        self.recipes = {}

    def add_recipe(self, name: str, ingredients: list[list[str]], facility: list[str], products: list[list[str]]) -> None:
        for recipe_name, _ in self.recipes.items():
            if name == recipe_name:
                raise ValueError("A recipe with that name already exists.")

        self.recipes[name] = {

        }
