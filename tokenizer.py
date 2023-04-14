import constant as C


class token():
    typ: str
    val: str

    def __init__(self, typ, val):

        self.typ = typ
        self.val = val

    def __repr__(self):
        return f'token({self.typ!r}, {self.val!r})'


def lex(s: str) -> list[token]:

    tokens = []
    i = 0
    while i < len(s):
        if s[i].isspace():
            i += 1
        elif s[i].isalpha():
            end = i + 1
            while end < len(s) and (s[end].isalnum() or s[end] == '_'):
                end += 1
            assert end >= len(s) or not (s[end].isalnum() or s[end] == '_')

            word = s[i:end]

            if word in ['true', 'false']:
                tokens.append(token(C.BOOLEAN, word))
            else:
                tokens.append(token(C.VARIABLE, word))

            i = end
        elif s[i] == '!':
            tokens.append(token(C.OPERATOR, '!'))
            i += 1
        elif s[i] == '(':
            tokens.append(token(C.OPERATOR, '('))
            i += 1
        elif s[i] == ')':
            tokens.append(token(C.OPERATOR, ')'))
            i += 1
        elif s[i:i+2] == '||':
            tokens.append(token(C.OPERATOR, '||'))
            i += 2
        elif s[i:i+2] == '&&':
            tokens.append(token(C.OPERATOR, '&&'))
            i += 2
        # expressions
        elif s[i:i+2] == "++":
            tokens.append(token(C.OPERATOR, '++'))
            i += 1
        elif s[i:i+2] == "--":
            tokens.append(token(C.OPERATOR, '--'))
            i += 1
        elif s[i] == "+":
            tokens.append(token(C.OPERATOR, '+'))
            i += 1
        elif s[i] == "-":
            tokens.append(token(C.OPERATOR, '-'))
            i += 1
        elif s[i] == "*":
            tokens.append(token(C.OPERATOR, '*'))
            i += 1
        elif s[i] == "/":
            tokens.append(token(C.OPERATOR, '/'))
            i += 1
        elif s[i] == "%":
            tokens.append(token(C.OPERATOR, '%'))
            i += 1
        elif s[i] == "^":
            tokens.append(token(C.OPERATOR, '^'))
            i += 1
        elif s[i].isnumeric():
            end = i + 1
            while end < len(s) and (s[end].isnumeric() or s[end] == '.'):
                end += 1
            assert end >= len(s) or not (s[end].isnumeric() or s[end] == '.')

            word = s[i:end]
            tokens.append(token(C.NUMBER, float_str(word)))
            i = end
        elif s[i] == "=":
            tokens.append(token(C.OPERATOR, '='))
            i += 1
        elif s[i] == "\n":
            tokens.append(token(C.NEWLINE, '\n'))
            i += 1
        else:
            raise SyntaxError(f'unexpected character {s[i]}')

    return tokens


# convert input string to a float-type string
def float_str(string):
    try:
        float(string)
        return string if "." in string else string + ".0"
    except ValueError:
        raise ValueError(f"is not numeric {string}")