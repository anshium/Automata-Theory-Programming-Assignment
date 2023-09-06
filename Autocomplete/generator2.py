import argparse
import pytest
import json
import random

def getRandomPrefix(pfsa: dict[str, dict[str, float]], key: str) -> str:
    result = random.choices([i for i in list(pfsa[key].keys())], weights = [pfsa[key][i] for i in list(pfsa[key].keys())])

    return result

def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    """Takes in the PFSA and generates a string of `word_count` number of words
    The following string is when the input has only "Cat" as in it's PFSA with
    count of 4.
    """

    returnString = str()
    for i in range(word_count):
        firstChoice = random.choices([i for i in list(pfsa["*"].keys())], weights = [pfsa["*"][i] for i in list(pfsa["*"].keys())])

        key = firstChoice[0]
        word = key
        while(word[-1] != "*"):
            word = getRandomPrefix(pfsa, key)[0]
            key = word
        
        word = word[:len(word) - 1]

        returnString += word + " "
    returnString = returnString.strip()
    
    return returnString

def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    parser.add_argument("count", type=int, help="Sample size to gen")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    assert result == string
