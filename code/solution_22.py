from collections import deque
from pathlib import Path
from typing import Tuple


DATA_PATH = Path(__file__).resolve().parents[1] / "data"


class Deck:
    def __init__(self):
        self.cards = []

    def draw(self) -> int:
        card = max(self.cards)
        self.cards.remove(card)
        return card

    def add(self, card: int):
        self.cards.append(card)

    def __repr__(self):
        return str(self.cards)


def read_input(path: Path) -> Tuple[Deck, Deck]:
    decks = (deque(), deque())
    for i, block in enumerate(path.read_text().strip("\n").split("\n\n")):
        for card in block.split("\n")[1:]:
            decks[i].append(int(card))
    return decks


def play_combat(deck1: deque, deck2: deque) -> deque:
    """Play the Combat game until one player wins, the winner's deck is
    returned"""

    while deck1 and deck2:
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card1 < card2:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise ValueError

    return deck1 if deck1 else deck2


def play_recursive_combat(deck1: deque, deck2: deque) -> Tuple[deque, int]:
    """Play the Recursive Combat game until one player wins, the winner's deck is
    returned, and the winner."""

    played_config = []
    while deck1 and deck2:
        # Check if the config was already played
        config_hash = hash((tuple(deck1), tuple(deck2)))
        if config_hash in played_config:
            return deck1, 1
        played_config.append(config_hash)

        # Play round
        card1 = deck1.popleft()
        card2 = deck2.popleft()

        if len(deck1) >= card1 and len(deck2) >= card2:
            _, winner = play_recursive_combat(
                deque(list(deck1)[:card1]), deque(list(deck2)[:card2])
            )
        else:
            winner = 1 if card1 > card2 else 2

        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        elif winner == 2:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise ValueError

    if deck1:
        return deck1, 1
    elif deck2:
        return deck2, 2
    else:
        raise ValueError


def main(problem_number: int):
    # Part 1
    deck1, deck2 = read_input(DATA_PATH / f"input_{problem_number}.txt")
    winner_deck = play_combat(deck1, deck2)
    print(sum((i + 1) * card for i, card in enumerate(reversed(winner_deck))))

    # Part 2
    deck1, deck2 = read_input(DATA_PATH / f"input_{problem_number}.txt")
    winner_deck, _ = play_recursive_combat(deck1, deck2)
    print(sum((i + 1) * card for i, card in enumerate(reversed(winner_deck))))
