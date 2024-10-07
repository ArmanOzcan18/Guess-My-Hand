import random
from CardGame import Card
from copy import copy
PARTNERS = {
    'North': 'South',
    'South': 'North',
    'East': 'West',
    'West': 'East'
}

# Helper function to define suit pair opposites
def get_opposite_suit(suit):
    suit_pairs = {
        "Spades": "Hearts",
        "Hearts": "Spades",
        "Clubs": "Diamonds",
        "Diamonds": "Clubs"
    }
    return suit_pairs[suit]

# Helper function to categorize card values into groups
def get_card_value_group(value):
    high_cards = ["A", "K", "Q"]
    mid_cards = ["J", "10", "9", "8"]
    low_cards = ["7", "6", "5", "4", "3", "2"]

    if value in high_cards:
        return "High"
    elif value in mid_cards:
        return "Mid"
    else:
        return "Low"

# Function to determine remaining cards
def set_of_remaining_cards(player, cards):
    """
    Determine the remaining cards in the deck by excluding played, exposed, and hand cards.
    """
    remaining_cards = copy(cards)
    to_remove = player.hand + player.played_cards + player.exposed_cards['North'] + player.exposed_cards['East'] + player.exposed_cards['South'] + player.exposed_cards['West']
    
    for card in to_remove:
        if card in remaining_cards:
            remaining_cards.remove(card)
    
    return remaining_cards

# New strategy logic for North/South players
def NorthSouthStrategy(player, deck):
    """
    New strategy using suit pairing and value grouping.
    Expose cards that inform about opposite suits and complement card values.
    """
    if not player.hand:
        return None
    
    random_seed_index = len(player.played_cards)

    # Group cards by their suits
    suit_groups = {suit: [] for suit in ["Spades", "Hearts", "Clubs", "Diamonds"]}
    for card in player.hand:
        suit_groups[card.suit].append(card)

    # Prioritize playing cards from a suit if the opposite suit is present in the partner's exposed cards
    partner_suit = get_opposite_suit(player.exposed_cards[PARTNERS[player.name]][-1].suit) if player.exposed_cards[PARTNERS[player.name]] else None

    if partner_suit and suit_groups[partner_suit]:
        # Play a low card from the opposite suit pair
        for card in suit_groups[partner_suit]:
            if get_card_value_group(card.value) == "Low":
                return player.hand.index(card)

    # If no pairing suit card is available, play a low-value card
    for suit, cards in suit_groups.items():
        for card in cards:
            if get_card_value_group(card.value) == "Low":
                return player.hand.index(card)

    # Default to playing a random card if no other conditions are met
    return random.randint(0, len(player.hand) - 1)

# New strategy logic for East/West players (mirrors North/South)
def EastWestStrategy(player, deck):
    """
    Mirrors the North/South strategy with the new suit pairing and value grouping logic.
    """
    return NorthSouthStrategy(player, deck)

# New guessing strategy based on pairing logic
def guessing(player, cards, round):
    """
    Guess based on the new logic using suit pairing and value grouping.
    Infer which suits and values are more likely based on exposed cards.
    """
    number_of_cards_to_guess = 13 - round
    remaining_cards = set_of_remaining_cards(player, cards)

    partner_exposed_cards = player.exposed_cards[PARTNERS[player.name]]

    # Prioritize guessing cards in suits opposite to what the partner has exposed
    partner_last_exposed = partner_exposed_cards[-1] if partner_exposed_cards else None
    opposite_suit = get_opposite_suit(partner_last_exposed.suit) if partner_last_exposed else None

    guessed_cards = [card for card in remaining_cards if card.suit == opposite_suit]

    # Add mid-value cards if not enough guessed cards are available from the opposite suit
    if len(guessed_cards) < number_of_cards_to_guess:
        additional_cards = [card for card in remaining_cards if get_card_value_group(card.value) == "Mid"]
        guessed_cards.extend(additional_cards)

    if len(guessed_cards) >= number_of_cards_to_guess:
        return random.sample(guessed_cards, number_of_cards_to_guess)
    else:
        remaining_cards_sample = random.sample(remaining_cards, number_of_cards_to_guess - len(guessed_cards))
        return guessed_cards + remaining_cards_sample

# Playing function to assign the strategy based on the player's position
def playing(player, deck):
    """
    Applies the appropriate strategy (North/South or East/West) based on the player's position.
    Implements the suit pairing and value grouping logic.
    """
    global cards
    global random_seeds
    cards = deck.copyCards

    if player.name == "North" or player.name == "South":
        # Use the new North/South strategy with pairing and value grouping
        return NorthSouthStrategy(player, deck)
    else:
        # Use the new East/West strategy which mirrors the North/South strategy
        return EastWestStrategy(player, deck)
