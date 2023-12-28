import random


def name_generator():
    split_char = "-._"

    with open('../hetzner/resources/names.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        surname = lines[random.randint(0, len(lines) - 1)].replace('\n', '').lower()

    with open('../hetzner/resources/surnames.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        first_name = lines[random.randint(0, len(lines) - 1)].replace('\n', '')

    char = random.choice(split_char)

    year_birthday = str(random.choice(range(60, 100)))
    return surname + char + first_name + year_birthday


