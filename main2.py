import concurrent.futures
import logging
import random
from typing import NamedTuple, Final, Iterator
from custom_logger import CustomFormatter
from math import ceil, floor
import time


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
    package_number: int

def generate_words_for_current_package(alphabet: str, number_of_start_word:int, word_length: int, start_word_as_digits: list[int], word: str, package_number: int) -> int:
    logger.warning(f'{package_number=}, {number_of_start_word=}, {word_length=}, {start_word_as_digits=}, {word=}')
    list_of_package_words = []
    for i in range(qtty_of_items_in_package):
        word_as_digits = list(convert_decimal_number_to_custom_base(number=number_of_start_word, base=alphabet_length))
        word = ''.join([alphabet[character_index] for character_index in word_as_digits])
        logger.info(f'{word}')
        number_of_start_word+=1
        if len(word) <= 5:
            list_of_package_words.append(word)
        else:
            break

    return list_of_package_words


def __wrapper(args: ActionArgs) -> int:
    logger.debug(f'{args=}')
    return generate_words_for_current_package(**args._asdict())


def convert_decimal_number_to_custom_base(number: int, base: int) -> Iterator[int]:
    """Convert decimal integer to list of numbers for custom base by iteration. From lowest to bigger."""
    number_to_convert = number
    while number_to_convert:
        floor_division, remainder = divmod(number_to_convert, base)
        yield remainder

        number_to_convert = floor_division

def main_2():
    packages = [
        ActionArgs(
            alphabet=alphabet,
            number_of_start_word=qtty_of_items_in_package * package_number,
            word_length=word_length,
            start_word_as_digits=list(convert_decimal_number_to_custom_base(number=qtty_of_items_in_package * package_number, base=alphabet_length)),
            word=''.join([alphabet[character_index] for character_index in list(convert_decimal_number_to_custom_base(number=qtty_of_items_in_package * package_number, base=alphabet_length))]),
            package_number=package_number
        )
        for package_number in range(qtty_of_packages)
    ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(
            __wrapper,
            packages,
        )

        print(list(results))

    print()


if __name__ == "__main__":
    alphabet = 'abc'
    alphabet_length = len(alphabet)
    word_length = 5
    total_number_of_words: Final[int] = len(alphabet) ** word_length
    logger.error(f'{alphabet=}, {word_length=}, {total_number_of_words=}')
    qtty_of_items_in_package = 10
    qtty_of_packages = ceil(total_number_of_words / qtty_of_items_in_package)
    CustomFormatter()
    start = time.perf_counter()
    main_2()
    elapsed = time.perf_counter() - start
    logger.error(f"Program completed in {elapsed:0.5f} seconds.")




    # min_character_index: Final[int] = 0
    # max_character_index: Final[int] = alphabet_length - 1
    # start_word_as_digits = [random.randint(min_character_index, max_character_index) for _ in range(word_length)]



    # number_of_start_word = floor(total_number_of_words / 2)
    # number_in_decimal_system = number_of_start_word
    # number_in_alphabet_length_system_as_list = list(convert_decimal_number_to_custom_base(number=number_in_decimal_system, base=alphabet_length))
    # start_word_as_digits = number_in_alphabet_length_system_as_list
    # word = ''.join([alphabet[character_index] for character_index in start_word_as_digits])