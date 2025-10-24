
import sys
# Look into iterators


LETTER = 0
DIGIT = 1
UNKNOWN = 99


INT_LIT = 10
IDNET = 11
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
    # Prints array
    # test = file.read()
    # print(test)
    getChar(file)
    lex(file)
    stmtList(file)


# looks good to go
def getChar(file):
    global nextChar
    global charClass
    nextChar = file.read(1)
    print(f"This is the nextChar from getChar: {nextChar}")
    if not nextChar:
        return 0
    if nextChar.isalpha():
        charClass = LETTER
    elif nextChar.isdigit():
        charClass = DIGIT
    else:
        charClass = UNKNOWN
        print(f"This is the charClass from getChar: {charClass}")


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
        lexLen += 1
        # lexeme[lexLen] = nextChar
        lexeme.insert(lexLen, nextChar)
        lexeme.insert(lexLen, '\0')
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
    print(char)
    match char:
        case '(':
            addChar()
            nextToken = LEFT_PAREN
        case ')':
            addChar()
            nextToken = RIGHT_PAREN
        case '+':
            addChar()
            nextToken = ADD_OP
        case '-':
            addChar()
            nextToken = SUB_OP
        case '*':
            addChar()
            nextToken = MULT_OP
        case '/':
            addChar()
            nextToken = DIV_OP
        case '=':
            addChar()
            nextToken = ASSIGN_OP
        case ';':
            addChar()
            nextToken = SEMI_COLON
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
    lexeme = ""
    lexLen = 0
    getNonBlank(file)
    match charClass:
        case LETTER:
            addChar()
            getChar(file)
            while (charClass == LETTER or
                   charClass == DIGIT):
                addChar()
                getChar(file)
            if isPrint():
                nextToken = PRINT
            else:
                nextToken = IDNET
        case DIGIT:
            addChar()
            getChar(file)
            while charClass == DIGIT:
                addChar()
                getChar(file)
            nextToken = INT_LIT
        case UNKNOWN:
            print(f'looking up nextChar{nextChar}')
            lookup(nextChar)
            getChar(file)
        case EOF:
            nextToken = EOF
            lexeme[0] = 'e'
            lexeme[1] = 'o'
            lexeme[2] = 'f'
    # strStmt += lexeme
    strStmt.join(lexeme)
    strStmt + " "
    if nextToken == SEMI_COLON:
        print(f"{strStmt}")
        strStmt = ""
    return nextToken


# correct function
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


def stmtList(file):
    global nextToken
    if nextToken == -1:
        print(">>> Empty .tiny file.")
    else:
        while nextToken != -1:
            stmt(file)


# Something is wrong here CHECK ME
def stmt(file):
    global nextToken
    global lexeme
    global expValue

    print(f"This is the nextToken in stmt(): {nextToken}")
    if nextToken == IDNET:
        var = lexeme
        lex(file)
        if nextToken == ASSIGN_OP:
            lex(file)
            expValue = expr(file)
            updateVar(var, expValue)
    elif nextToken == PRINT:
        lex(file)
        expValue = expr(file)
        if nextToken == SEMI_COLON:
            print(f'>>> {expValue}')

    if nextToken == SEMI_COLON:
        lex(file)
    else:
        print('Stmt():missing ";".')


def expr(file):
    global nextToken
    ret1 = term(file)
    while (nextToken == ADD_OP or
           nextToken == SUB_OP):
        token = nextToken
        lex(file)
        ret2 = term(file)
        if token == ADD_OP:
            ret1 += ret2
        else:
            ret1 = ret1 - ret2

    return ret1


def term(file):
    global nextToken
    ret1 = factor(file)
    while (nextToken == MULT_OP or
           nextToken == DIV_OP):
        token = nextToken
        lex(file)
        ret2 = factor(file)
        if token == MULT_OP:
            ret1 = ret1 * ret2
        else:
            ret1 = ret1 / ret2

    return ret1


def factor(file):
    global nextToken
    global lexeme
    global expValue
    if (nextToken == IDNET or nextToken == INT_LIT):
        var = lexeme
        token = nextToken
        if token == IDNET:
            if not getVarValue(var, expValue):
                print(f'factor() point 3: The Identifier {var} is not defined')
        else:
            expValue = int(var)
        lex(file)
    else:
        if (nextToken == LEFT_PAREN):
            lex(file)
            expValue = expr(file)
            if nextToken == RIGHT_PAREN:
                lex(file)
            else:
                print('factor() point 1')
        else:
            print('factor() point 2')
    return expValue


if __name__ == "__main__":
    main()
