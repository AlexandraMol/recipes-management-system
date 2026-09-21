from faker import Faker
import random

fake = Faker()


def generate_recipe():
    return {
        "category": random.sample(
            ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"],
            k=3
        ),
        "difficulty": random.choice(["Easy", "Medium", "Hard"]),
        "ingredients": [
            {
                "name": fake.word(),
                "quantity": random.randint(1, 10),
                "unit": random.choice(["g", "kg", "ml", "l", "pcs", "tbsp", "tsp"])
            }
            for _ in range(random.randint(3, 7))
        ],
        "name": fake.sentence(nb_words=3).replace(".", ""),
        "preparationTime": random.randint(10, 120),
        "steps": [
            {
                "description": fake.sentence()
            }
            for _ in range(random.randint(1, 3))
        ],
        "visibility": random.choice(["Public", "Private"]),
        "imageUrl": ""
    }


def add_recipes(num_recipes=5, username=None):
    recipes = []

    for _ in range(num_recipes):
        recipe = generate_recipe()
        recipe["username"] = username
        recipes.append(recipe)

    return recipes