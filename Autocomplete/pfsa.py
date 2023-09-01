import argparse
import pytest
import json

def getProbabilities(prefix: str, word_list: list)->dict:
    l = dict()
    
    for i in range(len(word_list)):
        if(word_list[i][:len(prefix)] == prefix):
            #if(len(word_list[i]) > i + 1): # Checking if the word that we have found is of greater length than prefix
            if(len(word_list[i]) > len(prefix)):
                next_letter = word_list[i][len(prefix):len(prefix) + 1]
                if(next_letter in l.keys()):
                    l[next_letter] += 1
                else:
                    l[next_letter] = 1
            elif(word_list[i] == prefix):
                l["*"] = 1
    # print(l)

    sum_ = 0
    for i in l.keys():
        sum_ += l[i]
    # print(sum_)
    for i in l.keys():
        l[i] /= sum_
        l[i] = round(l[i], 2)
    # print(l)
    return l;    

def generateKeyValuePair(prefix: str, probabilities: dict)->dict:
    # Gives a dict of only one element. Can there be a more efficient DS for this?
    d = dict()
    d[prefix] = dict()

    for key in probabilities:
        d[prefix][prefix + key] = probabilities[key]
    print(d)
    return d

def genKVPairForStar(word_list: list) -> dict:
    d = dict()
    d["*"] = dict()
    for i in range(len(word_list)):
        letter = word_list[i][0]
        if(letter in d["*"].keys()):
            d["*"][letter] += 1
        else:
            d["*"][letter] = 1

    sum_ = 0
    for i in d["*"].keys():
        sum_ += d["*"][i]
    for i in d["*"].keys():
        d["*"][i] /= sum_
        d["*"][i] = round(d["*"][i], 2)
    # print(d)
    return d;  

# Well I can optimise it possibly but this might work as well.
def isCompleted(d: dict, word_list: list) -> bool:
    for i in word_list:
        if(i not in d.keys()):
            return False

    return True

def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa
    The given example is for the statement "A cat"
    """
    # TODO: FILL IN THIS FUNCTION

    # Pseudocode: Algorithm:
    '''
    Pick a letter that is there in the keys of *
    Then see which all words have their first letter as the chose letter x, then for x make probabilty thing and
    do until the last such thing in the main object does not have any states which are not end states.
    
    '''
    
    pfsa = dict()

    word_list = ["ansh", "hello", "hi", "hungama", "hujhsj", "hu", "hujhjk"]
    pfsa["*"] = genKVPairForStar(word_list)["*"]

    while(not isCompleted(pfsa, word_list)):
        p = list(pfsa.keys())
        
        for i in p:
            for j in pfsa[i].keys():
                if(j not in pfsa):
                    pfsa[j] = generateKeyValuePair(j, getProbabilities(j, word_list))[j]

    # print(pfsa)

    # Then remove the cases where final states are keys:

    pfsakeys = list(pfsa.keys())
    
    for ds in pfsakeys:
        if(ds[-1] == "*"):
            del pfsa[ds]

    print(pfsa)
    
    return {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    }


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa
