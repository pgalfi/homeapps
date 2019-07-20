import re

from django.core.management import BaseCommand


def evaluate_amount(amount_str):
    amount_str = amount_str.strip()
    amount_str = amount_str.replace("½", "0.5")
    amount_str = amount_str.replace("¼", "0.25")
    amount_str = amount_str.replace("¾", "0.75")

    if "/" in amount_str:
        amounts = amount_str.split("/", maxsplit=1)
        return evaluate_amount(amounts[0]) / evaluate_amount(amounts[1])

    if ":" in amount_str:
        amounts = amount_str.split(":", maxsplit=1)
        return evaluate_amount(amounts[0]) + (evaluate_amount(amounts[1]) / 60)

    if "-" in amount_str:
        amount1, amount2 = amount_str.split("-", maxsplit=1)
        return (evaluate_amount(amount1) + evaluate_amount(amount2)) / 2

    if " " in amount_str:
        amounts = amount_str.split()
        return sum(evaluate_amount(one_amount) for one_amount in amounts)

    return float(amount_str)


def get_amount(value_str):
    return re.match("(^[0-9 :\\-/½¼¾]+)", value_str)


class Ingredient:
    food = None
    amount = None
    unit = None

    def __init__(self, line=None,food=None, amount=None, unit=None):
        if line is not None:
            self.construct_from_text(line)
        else:
            self.food = food
            self.amount = amount
            self.unit = unit

    def construct_from_text(self, line):
        ingredient = line.strip().split("-", maxsplit=1)
        self.food = ingredient[0].strip()
        if len(ingredient) > 1:
            amount_part = ingredient[1].strip()
            match = get_amount(amount_part)
            if match is not None:
                self.amount = evaluate_amount(match.group(1))
                unit_part = amount_part.replace(match.group(), "")
            else:
                unit_part = amount_part
                self.amount = None
            self.unit = unit_part.strip()

    def get(self):
        return {"food": self.food, "amount": self.amount, "unit": self.unit}


class PrepTime:
    time = None  # in minutes
    unparsed = ""

    def __init__(self, line=None, time=None):
        if line is not None:
            self.unparsed = line.strip()
            if "&" in self.unparsed or "and" in self.unparsed.lower():
                parts = re.split("and|&", self.unparsed, maxsplit=1, flags=re.IGNORECASE)
                self.time = PrepTime(parts[0]).get() + PrepTime("&".join(parts[1:])).get()
                return
            match = get_amount(re.sub("about", "", self.unparsed, flags=re.IGNORECASE).strip())
            if match is not None:
                value = evaluate_amount(match.group(1))
                unit = self.unparsed.replace(match.group(), "").lower()
                if "min" in unit:
                    self.time = value
                elif "hour" in unit:
                    self.time = value * 60
        else:
            self.time = time

    def get(self):
        if self.time is None:
            return -1
        return self.time


class ServingSize:
    amount = None  # number of servings
    unparsed = ""

    def __init__(self, line=None, amount=None):
        if line is not None:
            self.unparsed = line.strip()
            match = get_amount(self.unparsed.strip())
            if match is not None:
                self.amount = evaluate_amount(match.group(1))
        else:
            self.amount = amount

    def get(self):
        return self.amount if self.amount is not None else self.unparsed


class ParsedRecipe:
    name = ""
    desc = ""
    prep_time = None
    serving_size = None
    ingredients = []
    directions = ""

    def __repr__(self):
        return " {\r\n" + self.name + "\r\n(" + self.desc + ")\r\nTIME: " + str(self.prep_time) + "\r\nINGREDIENTS:\r\n" \
               + str(self.ingredients) + "\r\nDIRECTIONS:\r\n" + self.directions + "}"

    def finalize(self):
        self.desc = self.desc.strip()


class BuildSwitch:
    ingredients = False
    directions = False
    start = True
    description = False

    def reset(self):
        self.ingredients = False
        self.directions = False
        self.description = False
        self.start = True


class RecipeParser:

    def __init__(self, txt_path):
        self.path = txt_path

    def parse(self):
        build_recipe = ParsedRecipe()
        recipes = []
        switch = BuildSwitch()
        empty_line_count = 0
        with open(self.path, encoding="utf-8") as txt_file:
            line = None
            while line != "":
                line = txt_file.readline()
                if line.strip().isdigit(): line = "\r\n"
                if len(line.strip()) == 0:
                    empty_line_count += 1
                    if empty_line_count > 2 and switch.directions:
                        build_recipe.finalize()
                        recipes.append(build_recipe)
                        build_recipe = ParsedRecipe()
                        switch.reset()
                    continue
                else:
                    empty_line_count = 0
                if switch.start:
                    build_recipe.name = line.strip()
                    switch.start = False
                    switch.description = True
                    continue
                if line.startswith("TOTAL TIME:"):
                    switch.description = False
                    build_recipe.prep_time = PrepTime(line.replace("TOTAL TIME:", "").strip()).get()
                if line.startswith("SERVING SIZE:"):
                    switch.description = False
                    build_recipe.serving_size = ServingSize(line.replace("SERVING SIZE:", "").strip()).get()
                if line.startswith("INGREDIENTS:"):
                    switch.description = False
                    switch.ingredients = True
                    continue
                if line.startswith("DIRECTIONS:"):
                    switch.ingredients = False
                    switch.directions = True
                    continue

                if switch.description:
                    build_recipe.desc += line.strip() + " "
                if switch.ingredients:
                    ingredient = Ingredient(line)
                    build_recipe.ingredients.append(ingredient)
                if switch.directions:
                    if re.match("^[0-9]+?\\.\\s", line):
                        build_recipe.directions += "\r\n" + line.strip() + " "
                    else:
                        build_recipe.directions += line.strip() + " "
            if switch.directions:
                build_recipe.finalize()
                recipes.append(build_recipe)
        return recipes


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="+", type=str)

    def handle(self, *args, **options):
        recipe_parser = RecipeParser(options["path"][0])
        print(recipe_parser.parse())
