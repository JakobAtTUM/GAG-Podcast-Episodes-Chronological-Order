import re

def extract_integers(input_string):
    # Use regular expression to find all integers in the string
    numbers = re.findall(r'\d+', input_string)
    # Convert the found strings to integers
    return [int(num) for num in numbers]