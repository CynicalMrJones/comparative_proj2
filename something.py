
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
# array of chars
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
    global nextChar
    global charClass
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
    global nextChar
    if nextChar == ' ':
        return True
    else:
        return False


def getNonBlank(file):
    global nextChar
    while isspace(nextChar):
        getChar(file)


def addChar():
    global lexLen
    global lexeme
    global nextChar
    if lexLen <= 98:
        lexeme[lexLen + 1] = nextChar
        lexeme[lexLen] = 0
    else:
        print("Error lexeme is too long")


def isPrint():
    global lexeme
    if (lexeme[0] == 'P' and
        lexeme[1] == 'R' and
        lexeme[2] == 'I' and
        lexeme[3] == 'N' and
        lexeme[4] == 'T' and
        lexeme[5] == '\0'):
        return True
    else:
        return False


def lookup(char):
    global nextToken
    match char:
        case '(':
            addChar()
            nextToken = Token.LEFT_PAREN.value
        case ')':
            addChar()
            nextToken = Token.RIGHT_PAREN.value
        case '+':
            addChar()
            nextToken = Token.ADD_OP.value
        case '-':
            addChar()
            nextToken = Token.SUB_OP.value
        case '*':
            addChar()
            nextToken = Token.MULT_OP.value
        case '/':
            addChar()
            nextToken = Token.DIV_OP.value
        case '=':
            addChar()
            nextToken = Token.ASSIGN_OP.value
        case ';':
            addChar()
            nextToken = Token.SEMI_COLON.value
        case _:
            addChar()
            nextToken = -1
    return nextToken


def lex(file):
    global lexLen
    global nextToken
    global charClass
    global strStmt
    lexLen = 0
    getNonBlank(file)
    match charClass:
        case Characters.LETTER.value:
            addChar()
            getChar(file)
            while (charClass == Characters.LETTER.value or
                   charClass == Characters.DIGIT.value):
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
    strStmt += lexeme
    strStmt += " "
    if nextToken == Token.SEMI_COLON.value:
        print(f"{strStmt}")
        strStmt = ""
    return nextToken


def updateVar(var, value):
    global varMap
    varMap[var] = value


def getVarValue(var, val):
    global varMap
    global expValue
    test = varMap.get(var)
    if var == test:
        return True
    else:
        expValue = -1
        return False


def stmtList():
    global nextToken
    if nextToken == -1:
        print(">>> Empty .tiny file.")
    else:
        while nextToken != -1:
            stmt()


def stmt(file):
    global nextToken
    global lexeme
    global expValue
    if nextToken == Token.IDENT.value:
        var = lexeme
        lex(file)
        if nextToken == Token.ASSIGN_OP:
            lex(file)
            expValue = expr(file)
            updateVar()
    elif nextToken == Token.PRINT.value:
        lex()
        expValue = expr(file)
        if nextToken == Token.SEMI_COLON.value:
            print(f'>>> {expValue}')

    if nextToken == Token.SEMI_COLON.value:
        lex()
    else:
        print('Stmt():missing ";".')


def expr(file):
    global nextToken
    ret1 = term(file)
    while (nextToken == Token.ADD_OP.value or
           nextToken == Token.SUB_OP.value):
        token = nextToken
        lex()
        ret2 = term(file)
        if token == Token.ADD_OP.value:
            ret1 += ret2
        else:
            ret1 = ret1 - ret2

    return ret1


def term(file):
    global nextToken
    ret1 = factor(file)
    while (nextToken == Token.MUL_OP.value or
           nextToken == Token.DIV_OP.value):
        token = nextToken
        lex()
        ret2 = factor(file)
        if token == Token.MUL_OP.value:
            ret1 = ret1 * ret2
        else:
            ret1 = ret1 / ret2

    return ret1


def factor(file):
    global nextToken
    global lexeme
    global expValue
    if (nextToken == Token.IDENT.value or nextToken == Token.INT_LIT.value):
        var = lexeme
        token = nextToken
        if token == Token.IDNET.value:
            if not getVarValue(var, expValue):
                print(f'factor() point 3: The Identifier {var} is not defined')
        else:
            expValue = int(var)
        lex(file)
    else:
        if (nextToken == Token.LEFT_PAREN.value):
            lex(file)
            expValue = expr(file)
            if nextToken == Token.RIGHT_PAREN.value:
                lex(file)
            else:
                print('factor() point 1')
        else:
            print('factor() point 2')
    return expValue


if __name__ == "__main__":
    main()
