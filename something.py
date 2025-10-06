
from enum import Enum
import sys


class Characters(Enum):
    LETTER = 0
    DIGIT = 1
    UNKNOWN = 99


class Token(Enum):
    INT_LIT = 10
    IDNET = 11
    ASSIGN_OP = 20
    ADD_OP = 21
    SUB_OP = 21
    MULT_OP = 23
    DIV_OP = 24
    LEFT_PAREN = 25
    RIGHT_PAREN = 26
    SEMI_COLON = 27
    PRINT = 28


charClass = int()
lexeme = []
nextChar = ""
lexLen = int()
nextToken = int()
expValue = float()
strStmt = ""
varMap = dict()


def main():
    if len(sys.argv) < 2:
        print("Usage: parse input_file")
        return -1
    try:
        file = open(sys.argv[1], "r")
    except FileNotFoundError:
        print("File was not found")
    getChar(file)
    lex(file)


def getChar(file):
    nextChar = file.read(1)
    if not nextChar:
        return 0
    if nextChar.isalpha():
        charClass = Characters.LETTER.value
    elif nextChar.isdigit():
        charClass = Characters.DIGIT.value
    else:
        charClass = Characters.UNKNOWN.value


def isspace(file):
    if nextChar == ' ':
        return True
    else:
        return False


def getNonBlank(file):
    while isspace(nextChar):
        getChar(file)


def addChar():
    global lexLen
    global lexeme
    if lexLen <= 98:
        lexeme[lexLen + 1] = nextChar
        lexeme[lexLen] = 0
    else:
        print("Error lexeme is too long")


def lex(file):
    global lexLen
    global nextToken
    lexLen = 0
    match charClass:
        case Characters.LETTER.value:
            addChar()
            getChar(file)
            while charClass == Characters.LETTER.value or charClass == Characters.DIGIT.value:
                addChar()
                getChar(file)
            if isPrint():
                nextToken = Token.PRINT.value
            else:
                nextToken = Token.IDNET.value
        case Characters.DIGIT.value:
            addChar()
            getChar(file)
            while charClass == Characters.DIGIT.value:
                addChar()
                getChar(file)
            nextToken = Token.INT_LIT.value
        case Characters.UNKNOWN.value:
            lookup(nextChar)
            getChar(file)
        case EOF:
            nextToken = EOF
            lexeme[0] = 'E'
            lexeme[1] = 'O'
            lexeme[2] = 'F'
            lexeme[3] = 0


if __name__ == "__main__":
    main()
