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

# defining error types:
# 1. else before if
# 2. Only else, no if
# 3. empty initial statement
# 4. condition statement after `if` is not valid
# 5. Empty statement where a statement was expected
# So how about just having a few flags for this

else_before_if = 0
only_else_no_if = 0
empty_init_statement = 0
condition_statement_after_if_not_valid = 0
em_st_wh_a_st_wa_ex = 0

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

def isYConcat(string) -> bool:
##    for i in string.split(' '):
##        if(isStatementAlphabet(i) == 0 and len(i) > 0):
##            return 0
##    return 1
    tokens = tokenize(string)
    for i in tokens:
        if(i[1] == "if" or i[1] == "else"):
            return 0
        if(i[0] == TokenType.IDENTIFIER or i[0] == TokenType.KEYWORD or i[0].isnumeric()):
            continue
    return 1
    
def checkAndGetCondPartEnd(string: str) -> list:
    # first should be an x
    # Then if an operator is next
    # Go next and confirm that there is an x that is next
    # Go on until there is a case where there is an x and then put a mark there

    tokens = tokenize(string)
    print("1234:", tokens)
    valid = 1

    count = 0

    end_token = ""
    
    for i in tokens:
        if(count % 2 == 0):
            if(not isx(i[1])):
                valid = 0
                print("h1")
                break
        if(count % 2 == 1):
            if(i[1] not in symbols):
                print("h2")
                end_token = i
                valid = 1
                break
        end_token = i
        count += 1
    f = 0
    if(valid):  
        f = string.find(end_token[1]) #+ len(end_token[1])
    
    return [valid, f]
    
def checkGrammar(source_code, tokens) -> bool:
    # write the code the syntactical analysis in this function
    # You CAN use other helper functions and create your own helper functions if needed

##    source_code = ' '.join([i[1] for i in tokens])

    if(len(source_code.replace(' ', '')) == 0):
        print("SyntaxError: Source Code cannot be all spaces or empty.")
        return 0
##        raise SyntaxError("Source Code cannot be all spaces or empty.")
    
    Q = [source_code]

    while(len(Q) != 0):
        print(Q)
        s = Q.pop(0)

        s = " " + s + " " # doing this to avoid find malfunctionality just in case
        print(s)
        find_result_if = s.find(" if ") # length is 4
        if(find_result_if == -1):
            if(isYConcat(s)):
                continue
##            if(" else " in s):
##                only_else_no_if = 1
##                print("SyntaxError: An if was not found before an else.")
            return 0
        
        statement1 = s[:find_result_if]
        statement2 = s[find_result_if + 4:]
        statement1 = " " + statement1 + " "
        # if len(statement1.replace(' ', '')) != 0:
        Q.append(statement1)
        statement2 = " " + statement2 + " "
        #if len(statement2.replace(' ', '')) != 0:
        Q.append(statement2)
        print("S1:", statement1)
        print("S2:", statement2)
        
        find_result_else = statement2.rfind(" else ")
        
        if(find_result_else != -1):
            statement3 = statement2[find_result_else + 6:]
            Q.append(statement3)
            statement2 = statement2[:find_result_else]
            print("S3:", statement3)
            print("S2:", statement2)

        print("70115:", statement2)
        condPartEnd = checkAndGetCondPartEnd(statement2)
        print("03797:", condPartEnd)
        if(condPartEnd[0] == 0):
            condition_statement_after_if_not_valid = 1
            print("SyntaxError: Condition statement after if is not valid/present")
            return 0
        
        print("84460:", statement2[condPartEnd[1]:])
        if(condPartEnd[0] == 1):
            Q.append(statement2[condPartEnd[1]:])
        

    return 1
            
# Test the tokenizer
if __name__ == "__main__":
    # source_code = "if 2+xi > 0 print 2.0 else print -1;"
    source_code = input()
    tokens = tokenize(source_code)

    for token in tokens:
        print(f"Token Type: {token[0]}, Token Value: {token[1]}")

    logs = checkGrammar(source_code, tokens)  # You are tasked with implementing the function checkGrammar
    if(logs == 1):
        print("Yes, ok!")
    else:
        print("Not ok")
