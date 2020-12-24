from pathlib import Path
from typing import List


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


def read_input(path: Path) -> List[int]:
    foods = []
    all_ingredients = list()
    all_allergens = list()

    for line in path.read_text().strip("\n").split("\n"):
        ingredients, allergens = line.replace(")", "").split(" (contains ")
        ingredients = ingredients.split(" ")
        allergens = allergens.split(", ")

        foods.append((ingredients, allergens))
        all_ingredients.extend(ingredients)
        all_allergens.extend(allergens)

    all_ingredients = list(set(all_ingredients))
    all_allergens = list(set(all_allergens))

    return foods, all_ingredients, all_allergens


def main(problem_number: int):
    foods, all_ingredients, all_allergens = read_input(
        DATA_PATH / f"input_{problem_number}.txt"
    )

    # Part 1
    # Contains for each allergen a list of list of possible ingredients
    map_allergen_list_ingredient = dict()
    for ingredients, allergens in foods:
        for allergen in allergens:
            map_allergen_list_ingredient.setdefault(allergen, []).append(ingredients)

    # Ingredients that can match an allergen
    ingredients_included = set()
    for allergen, list_ingredients in map_allergen_list_ingredient.items():
        s = set.intersection(*map(set, list_ingredients))
        ingredients_included.update(s)
    # Ingredients that can't match an allergen
    ingredients_excluded = set(all_ingredients).difference(ingredients_included)

    result = 0
    for ingredients, allergens in foods:
        for ingredient in ingredients:
            if ingredient in ingredients_excluded:
                result += 1
    print(result)

    # Part 2
    # Mapping between an allergen and the corresponding ingredient
    mapping = dict()
    while len(mapping) != len(all_allergens):
        for allergen, list_ingredients in map_allergen_list_ingredient.items():
            if allergen in mapping:
                continue
            list_set = [
                set(ingredients).difference(ingredients_excluded)
                for ingredients in list_ingredients
            ]
            s = set.intersection(*list_set)
            # if the len is 1 then we can do an association allergen <-> ingredient
            if len(s) == 1:
                ingredient = s.pop()
                mapping[allergen] = ingredient
                ingredients_excluded.add(ingredient)

    print(",".join(mapping[key] for key in sorted(mapping)))
