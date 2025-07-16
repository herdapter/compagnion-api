from bingo.models import Bingos


cases = [
    "Ace",
    "No scope",
    "1v5 clutch",
    "Team kill",
    "Knife kill",
    "Commentateur qui crie"
]

for content in cases:
    Bingos.objects.get_or_create(case_text=content)
