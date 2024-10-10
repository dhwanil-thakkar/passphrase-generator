#!/bin/env bash

number_of_words=$1
separator=$2
include_numbers=$3

echo $number_of_words
echo $separator
echo $include_numbers

# URL encode the separator, since it may contain reserved characters like '%'
encoded_separator=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$separator'))")

curl -X GET "https://pmrdq7ob8j.execute-api.us-east-1.amazonaws.com/default/passphrase_generator?number_of_words=$number_of_words&separator=$encoded_separator&include_numbers=$include_numbers"
