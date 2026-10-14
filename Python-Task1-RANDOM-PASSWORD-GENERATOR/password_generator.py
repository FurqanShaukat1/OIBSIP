import secrets
import string


AMBIGUOUS_CHARACTERS = "0Ol1"


def generate_password(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols,
    exclude_ambiguous=False
):
    if length < 8:
        raise ValueError(
            "Password length must be at least 8 characters."
        )

    character_sets = []

    if use_uppercase:
        characters = string.ascii_uppercase

        if exclude_ambiguous:
            characters = "".join(
                char for char in characters
                if char not in AMBIGUOUS_CHARACTERS
            )

        character_sets.append(characters)

    if use_lowercase:
        characters = string.ascii_lowercase

        if exclude_ambiguous:
            characters = "".join(
                char for char in characters
                if char not in AMBIGUOUS_CHARACTERS
            )

        character_sets.append(characters)

    if use_numbers:
        characters = string.digits

        if exclude_ambiguous:
            characters = "".join(
                char for char in characters
                if char not in AMBIGUOUS_CHARACTERS
            )

        character_sets.append(characters)

    if use_symbols:
        characters = string.punctuation
        character_sets.append(characters)

    if len(character_sets) < 2:
        raise ValueError(
            "Select at least two character types."
        )

    # Guarantee at least one character from every
    # selected character type.
    password = [
        secrets.choice(character_set)
        for character_set in character_sets
    ]

    # Combine all selected character sets.
    all_characters = "".join(character_sets)

    # Fill the remaining password positions.
    remaining_length = length - len(password)

    password.extend(
        secrets.choice(all_characters)
        for _ in range(remaining_length)
    )

    # Securely shuffle the final password.
    secrets.SystemRandom().shuffle(password)

    return "".join(password)