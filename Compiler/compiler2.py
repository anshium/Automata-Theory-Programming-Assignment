##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
from secrets import token_urlsafe


class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char=='_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position+1]
                        if next_next_char.isdigit():
                            is_float = True

                # checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens

########################## BOILERPLATE ENDS ###########################

symbols = ['+', '-', '*', '/', '^', '<', '>', '=']

def isStatementAlphabet(smtg: str) -> bool:
    if(smtg == 'if' or smtg == 'else'):
        return 0
    if(smtg.isnumeric()):
        return 1
    if(smtg in token_hierarchy):
        return 1
    if(is_valid_identifier(smtg)):
        return 1
    return 0

def isx(string: str) -> bool:
    # x ko main detect karne ke liye x->cond wali statement na bhi daalun to chalega
    # because I am considering condition -> x(op1)x(op1)x(op1)x...
    if(string.isnumeric() or isStatementAlphabet(string)):
        return 1
    return 0

def isCond(string: str) -> bool:
    # A condition can be identified if it is of the form when the even indices (0-indexed) are xs and the odd ones are symbols

    # y cannot be null (is my assumption) <<<

    # count number of non space characters
    num_chars = 0
    for i in string:
        if(i != ' '):
            num_chars += 1

    if(num_chars % 2 == 0):
        return 0

    string = string.replace(' ', '')

    for i in len(string):
        if(i % 2 == 0):
            if(not isx(string[i])):
                return 0
        if(i % 2 == 1):
            if(string[i] not in symbols): # symbols === op1
                return 0

    return 1       

# I thought about the grammar and found that I can have a queue using a list in py and then I can split at if
# and then 

# Case 1: no if [Passed!]
def checkGrammar(tokens) -> bool:
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed

    if_present = 0
    # Check for case 1
    for i in tokens:
        if(i[1] == "if"):
            if_present = 1
    
    if(not if_present):
        for i in tokens:
            print(i[1])
            if(isStatementAlphabet(i[1]) == 0):
                return 0
        return 1
    else:
        return 1

# Test the tokenizer
if __name__ == "__main__":
	# source_code = "if 2+xi > 0 print 2.0 else print -1;"
	source_code = input()
	tokens = tokenize(source_code)

	for token in tokens:
		print(f"Token Type: {token[0]}, Token Value: {token[1]}")

	logs = checkGrammar(tokens)  # You are tasked with implementing the function checkGrammar
	if(logs == 1):
		print("Yes, ok!")
	else:
		print("Not ok")
