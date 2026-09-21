from faker import Faker
from datetime import datetime

fake = Faker()


def generate_user():
    return {
        "email": fake.email(),
        "password": "password",
        "username": fake.user_name(),
        "createdAt": datetime.utcnow().isoformat()
    }


def add_user(number=0):
    users = []

    for _ in range(number):
        users.append(generate_user())

    return users