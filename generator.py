import typing
import random
import logging
import secrets


def setup_logger():
    logger = logging.Logger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("generator_debug.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)    

    logger.addHandler(file_handler)
    return logger


def generate_passphrase(number_of_words:int = 6, seprator: str = '+') -> str:

    ## Number of Words should be minimum of 3
    if (number_of_words < 3):
        raise ValueError("number_of_words can not be less than 3, Its really insecure")

    # Intialize Empty passphrase String
    passphrase = ""                 

    for iteration in range(number_of_words):
        # number = generate_random_number()
        number = generate_cryptographically_secure_psuedo_random_number()
        word = choose_word_from_wordlist(number)
        passphrase = str(passphrase) + str(word)
        
        if (iteration == number_of_words - 1):   #Last entry
            pass
        else:
            passphrase = str(passphrase) + str(seprator)

    return str(passphrase)


def generate_cryptographically_secure_psuedo_random_number() -> int:
    
    # Faces of the Die that can be chosen at random
    choice_list  = [1,2,3,4,5,6]

    # 5 rolls to generate a 5-digit number like '15126'
    digits = 5

    rand_number = ''.join(str(secrets.choice(choice_list)) for _ in range(digits))

    return int(rand_number)


def choose_word_from_wordlist(number: int) -> str:
    logger.debug(f"searching for word : <*****>")
    with open("wordlist.txt") as fp:
        for i, line in enumerate(fp):
            try:
                parts = line.split()
            except Exception as e:
                raise ValueError (f"Error in wordlist, unable to split parts, {e}")
            if (len(parts) > 1  and int(parts[0])==number):
                    return str(parts[1])

    raise IndexError("choosen number out of bounds of wordlist")


# Main Execution Block
if __name__ == "__main__":

    logger = setup_logger()
    
    logger.debug("Creating Random PassPhrase")

    passphrase = generate_passphrase(number_of_words=6, seprator='$')
    print(passphrase)


