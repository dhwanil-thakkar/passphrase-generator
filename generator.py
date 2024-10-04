import typing
import random
import logging



def setup_logger():
    logger = logging.Logger(__file__)
    file_handler = logging.FileHandler("log.txt")
    logger.addHandler(file_handler)
    return logger


def generate_passphrase(number_of_words:int = 6, seprator: str = '+') -> str:

#    number1 = generate_random_number()
#    number2 = generate_random_number()
#    number3 = generate_random_number()
#    number4 = generate_random_number()
#    number5 = generate_random_number()
#    number6 = generate_random_number()
#
#    word1 = choose_word_from_wordlist(number1)
#    word2 = choose_word_from_wordlist(number2)
#    word3 = choose_word_from_wordlist(number3)
#    word4 = choose_word_from_wordlist(number4)
#    word5 = choose_word_from_wordlist(number5)
#    word6 = choose_word_from_wordlist(number6)


#    passphrase =str(
#                word1 + seprator + 
#                word2 + seprator + 
#                word3 + seprator +
#                word4 + seprator +
#                word5 + seprator +
#                word6 + seprator 
#                )

    ## Number of Words should be minimum of 3

    if (number_of_words < 3):
        raise ValueError("number_of_words can not be less than 3")

    passphrase = ""                 # Intialize Empty passphrase String


    for iteration in range(number_of_words):
        number = generate_random_number()
        word = choose_word_from_wordlist(number)
        passphrase = str(passphrase) + str(word)
        
        if (iteration == number_of_words - 1):   #Last entry
            pass
        else:
            passphrase = str(passphrase) + str(seprator)


    return str(passphrase)

def generate_random_number() -> int:
    number = 0
    for i in range(5):
        number = str(number) + str(random.randint(1,6))
    return int(number)


def choose_word_from_wordlist(number: int) -> str:
    logger.debug(f"searching for word : {number}")
    with open("wordlist.txt") as fp:
        for i, line in enumerate(fp):
            try:
                parts = line.split()
            except Exception as e:
                raise ValueError (f"Error in wordlist, unable to split parts, {e}")
            if (len(parts) > 1  and int(parts[0])==number):
                    return str(parts[1])

    raise IndexError("choosen number out of bounds of wordlist")






if __name__ == "__main__":

    logger = setup_logger()

    passphrase = generate_passphrase(number_of_words=6, seprator='$')
    print(passphrase)


