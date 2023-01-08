import concurrent.futures
import logging
import random
from typing import NamedTuple, Final, Iterator
from custom_logger import CustomFormatter
from math import ceil, floor


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


class ActionArgs(NamedTuple):
    alphabet: str
    number_of_start_word: int
    word_length: int
    start_word_as_digits: list[int]
    word: str

def make_actions_partial(alphabet: str, number_of_start_word:int, word_length: int, start_word_as_digits: list[int], word: str) -> int:
    logger.warning(f'{alphabet=}, {number_of_start_word=}, {word_length=}, {start_word_as_digits=}, {word=}')


    return number_of_start_word


def make_action__wrapper(args: ActionArgs) -> int:
    logger.debug(f'{args=}')
    return make_actions_partial(**args._asdict())


def convert_decimal_number_to_custom_base(number: int, base: int) -> Iterator[int]:
    """Convert decimal integer to list of numbers for custom base by iteration. From lowest to bigger."""
    number_to_convert = number
    while number_to_convert:
        floor_division, remainder = divmod(number_to_convert, base)
        yield remainder

        number_to_convert = floor_division

def main_2():
    alphabet = 'abc'
    alphabet_length = len(alphabet)
    word_length = 5
    total_number_of_words: Final[int] = len(alphabet) ** word_length
    logger.error(f'{alphabet=}, {word_length=}, {total_number_of_words=}')
    qtty_of_items_in_package = 10
    qtty_of_packages = ceil(total_number_of_words / qtty_of_items_in_package)

    # min_character_index: Final[int] = 0
    # max_character_index: Final[int] = alphabet_length - 1
    # start_word_as_digits = [random.randint(min_character_index, max_character_index) for _ in range(word_length)]

    number_of_start_word = floor(total_number_of_words / 2)

    number_in_decimal_system = number_of_start_word

    number_in_alphabet_length_system_as_list = list(convert_decimal_number_to_custom_base(number=number_in_decimal_system, base=alphabet_length))

    start_word_as_digits = number_in_alphabet_length_system_as_list

    word = ''.join([alphabet[character_index] for character_index in start_word_as_digits])

    packages = [
        ActionArgs(
            alphabet=alphabet,
            number_of_start_word=qtty_of_items_in_package * package_number,
            word_length=word_length,
            start_word_as_digits=start_word_as_digits,
            word=word
        )
        for package_number in range(qtty_of_packages)
    ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(
            make_action__wrapper,
            packages,
        )

        print(list(results))

    print()


if __name__ == "__main__":
    CustomFormatter()
    main_2()



