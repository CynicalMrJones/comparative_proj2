
from enum import Enum
import sys
# Look into iterators


class Characters(Enum):
    LETTER = 0
    DIGIT = 1
    UNKNOWN = 99


class Token(Enum):
    INT_LIT = 10
    IDENT = 11
    ASSIGN_OP = 20
    ADD_OP = 21
    SUB_OP = 22
    MULT_OP = 23
    DIV_OP = 24
    LEFT_PAREN = 25
    RIGHT_PAREN = 26
    SEMI_COLON = 27
    PRINT = 28
    EOF = -1


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
    stmtList(file)


# looks good to go
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


def getNonBlank(file):
    global nextChar
    while nextChar.isspace():
        getChar(file)


def addChar():
    global lexLen
    global lexeme
    global nextChar
    if lexLen <= 98:
        lexLen += 1
        lexeme += nextChar
    else:
        print("Error lexeme is too long")


def isPrint():
    global lexeme
    if lexeme == 'print':
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
    global nextChar
    global lexeme
    lexeme = ""
    lexLen = 0
    getNonBlank(file)
    if charClass == Characters.LETTER.value:
        addChar()
        getChar(file)
        while (charClass == Characters.LETTER.value or
               charClass == Characters.DIGIT.value):
            addChar()
            getChar(file)
        if isPrint():
            nextToken = Token.PRINT.value
        else:
            nextToken = Token.IDENT.value
    elif charClass == Characters.DIGIT.value:
        addChar()
        getChar(file)
        while charClass == Characters.DIGIT.value:
            addChar()
            getChar(file)
        nextToken = Token.INT_LIT.value
    elif charClass == Characters.UNKNOWN.value:
        lookup(nextChar)
        getChar(file)
    elif charClass == Token.EOF.value:
        nextToken = Token.EOF.value
        lexeme = 'EOF'
    for c in lexeme:
        strStmt += c
        strStmt += ' '
    if nextToken == Token.SEMI_COLON.value:
        print(strStmt)
        strStmt = ""
    return nextToken


# correct function
def updateVar(var, value):
    global varMap
    varMap[var] = value


def getVarValue(var, val):
    global varMap
    global expValue
    it = varMap.get(var)
    if it:
        expValue = it
        return True
    else:
        expValue = -1
        return False


def stmtList(file):
    global nextToken
    if nextToken == Token.EOF.value:
        print(">>> Empty .tiny file.")
    else:
        while nextToken != Token.EOF.value:
            stmt(file)


# Something is wrong here CHECK ME
def stmt(file):
    global nextToken
    global lexeme
    global expValue

    if nextToken == Token.IDENT.value:
        var = lexeme
        lex(file)
        if nextToken == Token.ASSIGN_OP.value:
            lex(file)
            expValue = expr(file)
            updateVar(var, expValue)
    elif nextToken == Token.PRINT.value:
        lex(file)
        expValue = expr(file)
        if nextToken == Token.SEMI_COLON.value:
            print(f'>>> {expValue}')

    if nextToken == Token.SEMI_COLON.value:
        lex(file)
    else:
        print('Stmt():missing ";".')


def expr(file):
    global nextToken
    ret1 = term(file)
    while (nextToken == Token.ADD_OP.value or
           nextToken == Token.SUB_OP.value):
        token = nextToken
        lex(file)
        ret2 = term(file)
        if token == Token.ADD_OP.value:
            ret1 = ret1 + ret2
        else:
            ret1 = ret1 - ret2

    return ret1


def term(file):
    global nextToken
    ret1 = factor(file)
    while (nextToken == Token.MULT_OP.value or
           nextToken == Token.DIV_OP.value):
        token = nextToken
        lex(file)
        ret2 = factor(file)
        if token == Token.MULT_OP.value:
            ret1 = ret1 * ret2
        else:
            ret1 = ret1 / ret2

    return ret1


def factor(file):
    global nextToken
    global lexeme
    global expValue
    if (nextToken == Token.IDENT.value or nextToken == Token.INT_LIT.value):
        var = ''
        for c in lexeme:
            var += c
        token = nextToken
        if token == Token.IDENT.value:
            if not (getVarValue(var, expValue)):
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
