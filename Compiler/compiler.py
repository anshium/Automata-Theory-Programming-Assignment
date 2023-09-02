##################### BOILERPLATE BEGINS ############################

# Token types enumeration
##################### YOU CAN CHANGE THE ENUMERATION IF YOU WANT #######################
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
    # Kya matlab? 
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

def isStatementAlphabet(smtg: str) -> bool:
    if(smtg == 'if' or smtg == 'else'):
        return 0
    if(smtg.isnumeric()):
        return 1
    if(token_hierarchy[smtg] == TokenType.KEYWORD):
        return 1
    if(is_valid_identifier(smtg)):
        return 1
    return 0
    
states = [
    1,              # Statement
    2,              # if A
    3,              # (statement)(statement)
    4,              # y
    5,              # A (special statement inside if
    6,              # (cond)(statement)
    7,              # (cond)(statement)(else)(statement)
    8,              # (cond)
    9,              # (x)(op1)(x)
    10,             # x
    11,             # op1
    12,             # set 12 [+, -, *, /, ^, <, >, =] <-- Hey last mein smiley ban gayi
    13,             # R (Real numbers)

]

# Now I need transitions and mechanisms to check if a particular string is within that state

# Second part looks more interesting at this point of time, let's do that first.
class StateChecker():
    def inState1(self, string: str) -> bool:
        # C'mon man string would be a string
        return 1
    def inState13(self, string: str) -> bool:
        if(string.isnumeric()):
            return 1
        return 0
    def inState12(self, string: str) -> bool:
        if(string in ['+', '-', '*', '/', '^', '<', '>', '=']):
            return 1
        return 0
    # Hmm, redundant state then
    def inState11(self, string: str) -> bool:
        return self.inState12()

    # State 4
    def isStatementAlphabet(self, smtg: str) -> bool:
        if(smtg == 'if' or smtg == 'else'):
            return 0
        if(smtg.isnumeric()):
            return 1
        if(token_hierarchy[smtg] == TokenType.KEYWORD):
            return 1
        if(is_valid_identifier(smtg)):
            return 1
        return 0

    # x
    def inState10(self, string: str) -> bool:
        if(self.inState13(string) or self.isStatementAlphabet(string) or 0):
            return 1
        return 0

    # 

# Transitions


def checkGrammar(tokens):
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed
    pass
    


# Test the tokenizer
if __name__ == "__main__":
    s = StateChecker()
    print(s.inState13("123"))
    source_code = "if 2+xi > 0 print 2.0 else print -1;"
    tokens = tokenize(source_code)

    for token in tokens:
        print(f"Token Type: {token[0]}, Token Value: {token[1]}")

    logs = checkGrammar(tokens)  # You are tasked with implementing the function checkGrammar
