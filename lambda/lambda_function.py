import json

import random
import logging
import secrets
import sys



def lambda_handler(event, context):
    
    # Default Values
    number_of_words = 6
    separator = '$'
    include_numbers = True
    
    
    # Handle API gateway query string parameters
    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['number_of_words']) and (
                event['queryStringParameters']['number_of_words'] is not None):
            number_of_words = event['queryStringParameters']['number_of_words']
            number_of_words = int(number_of_words)
            
        elif (event['multiValueQueryStringParameters']) and (event['multiValueQueryStringParameters']['number_of_words']) and (
                event['multiValueQueryStringParameters']['number_of_words'] is not None):
            number_of_words = event['multiValueQueryStringParameters']['number_of_words'][0]
            number_of_words = int(number_of_words)
            
    except (KeyError, ValueError):
        print('No number_of_words')

        
    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['separator']) and (
                event['queryStringParameters']['separator'] is not None):
            separator = event['queryStringParameters']['separator']
            
        elif (event['multiValueQueryStringParameters']) and (event['multiValueQueryStringParameters']['separator']) and (
                event['multiValueQueryStringParameters']['separator'] is not None):
            separator = event['multiValueQueryStringParameters']['separator'][0]
            
    except KeyError:
        print('No separator')
        
    try:
        if (event['queryStringParameters']) and (event['queryStringParameters']['include_numbers']) and (
                event['queryStringParameters']['include_numbers'] is not None):
            include_numbers = event['queryStringParameters']['include_numbers']
            include_numbers = str_to_bool(include_numbers)
            
        elif (event['multiValueQueryStringParameters']) and (event['multiValueQueryStringParameters']['include_numbers']) and (
                event['multiValueQueryStringParameters']['include_numbers'] is not None):
            include_numbers = event['multiValueQueryStringParameters']['include_numbers'][0]
            include_numbers = str_to_bool(include_numbers)
            
    except KeyError:
        print('No include_numbers')



    passphrase = generate_passphrase(number_of_words = number_of_words, separator = separator, include_numbers = include_numbers)

    data = {'passphrase' : passphrase}
        
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
    
def str_to_bool(value: str) -> bool :
    return value.lower() in ['true','1','yes']
    


#def setup_logger():
#    logger = logging.Logger(__name__)
#    logger.setLevel(logging.DEBUG)
#
#    file_handler = logging.FileHandler("/tmp/generator_debug.log")
#    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#    file_handler.setFormatter(formatter)    
#
#    logger.addHandler(file_handler)
#    return logger


def generate_passphrase(number_of_words:int = 6, separator: str = '+', include_numbers: bool = False) -> str:

    ## Number of Words should be minimum of 3
    if (number_of_words < 3):
        raise ValueError("number_of_words can not be less than 3, Its really insecure")

    # Intialize Empty passphrase list, we will convert this to string later
    passphrase = []
    
    # Intialize an Emptpy list for random number that will be held for sprinkling
    list_of_numbers = []

    if include_numbers:
        # Add 1 to make sure we atleast have one number as secrets.randbelow is lower bound inclusive [0,arg)
        num_numbers = secrets.randbelow(number_of_words) + 1

        # Pick random digits and insert at random positions
        for _ in range(num_numbers):
            number = secrets.randbelow(10)
            # Insert the number at random position in the list, +1 to make sure upperbound is positive
            insert_position = secrets.randbelow(len(list_of_numbers) +1)
            list_of_numbers.insert(insert_position, number)
        
        
    for iteration in range(number_of_words):
        # number = generate_random_number()
        number = generate_cryptographically_secure_psuedo_random_number()
        word = choose_word_from_wordlist(number)

        #Append new word to the passphrase
        passphrase.append(word)

        # if there are still number left in the list, pick one at random and append after the word.
        if list_of_numbers:

            index_of_number_to_insert  = secrets.randbelow(len(list_of_numbers))
            passphrase.append(str(list_of_numbers[index_of_number_to_insert]))
            list_of_numbers.pop(index_of_number_to_insert)

        # Add a seprator for every word additona, except the last one
        if iteration < number_of_words -1:
            passphrase.append(separator)

    
    string_passphrase = ''.join(passphrase)
    return string_passphrase

# returns a randomly choosen 5 digit number that reprsent throwing 5 dices and returns the number
def generate_cryptographically_secure_psuedo_random_number() -> int:
    
    # Faces of the Die that can be chosen at random
    choice_list  = [1,2,3,4,5,6]

    # 5 rolls to generate a 5-digit number like '15126'
    digits = 5

    # Chooses a list of 5 digits from the choice list, to simulate throwing 5 dices
    rand_digits = [secrets.choice(choice_list) for _ in range(digits)]

    # Takes a list and shuffles the list in place around to have more entropy
    random.shuffle(rand_digits)

    shuffled_rand_number = ''.join(map(str, rand_digits))

    return int(shuffled_rand_number)


def choose_word_from_wordlist(number: int) -> str:
#    logger.debug(f"searching for word : <*****>")
    with open("wordlist.txt") as fp:
        for i, line in enumerate(fp):
            try:
                parts = line.split()
            except Exception as e:
                raise ValueError (f"Error in wordlist, unable to split parts, {e}")
            if (len(parts) > 1  and int(parts[0])==number):
                    return str(parts[1])

    raise IndexError("choosen number out of bounds of wordlist")




def is_valid_separator(separator:str) -> bool:
    # Check it the separator is a single Charater
    return len(separator) == 1



class input_class:

    def __init__(self):
        self.number_of_words: int = 6
        self.seprator: str = "-"
        self.include_numbers: bool = True

        # Stil left to implement
        self.capitalize: bool = True



# Main Execution Block
#if __name__ == "__main__":

#    logger = setup_logger()    
#    logger.debug("Creating Random PassPhrase")

    

#    if len(sys.argv) != 3:
#        raise ValueError("\n\n Error: Needs two arguments \n1.number_of_words \n2.separator \n")
#    
#    number_of_words = int(sys.argv[1])
#    separator = str(sys.argv[2])

    

#    if not (is_valid_separator(separator=separator)):
#        raise ValueError ("Seprator should be a single character")



#    passphrase = generate_passphrase(number_of_words=number_of_words, separator=separator, include_numbers= True)
#    print(passphrase)
