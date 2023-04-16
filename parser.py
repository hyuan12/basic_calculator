from typing import Any
import tokenizer
import constant as C


class ast():
    typ: str
    children: tuple[Any, ...]

    def __init__(self, typ: str, *children: Any):
        """
        x || true
        >>> ast('||', ast('var', 'x'), ast('val', True))
        ast('||', ast('var', 'x'), ast('val', True))
        """
        self.typ = typ
        self.children = children

    def __repr__(self):
        return f'ast({self.typ!r}, {", ".join([repr(c) for c in self.children])})'


class parse():
    def __init__(self):
        self.lst = []

    def parse_tokens(self, tokens):
        ts = tokens

        a, i = equal(ts, 0)
        self.lst.append(a)

        if i != len(ts) and i < len(ts):
            ts = ts[i:]
            self.parse_tokens(ts)
            # raise SyntaxError(f"expected EOF, found {ts[i:]!r}")

        return self.lst


def equal(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 + 2')
    ast('+', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected addition, found EOF')

    lhs, i = add(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.EQUAL:
        rhs, i = add(ts, i+1)
        lhs = ast(C.EQUAL, lhs, rhs)

    return lhs, i



def add(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 + 2')
    ast('+', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected addition, found EOF')

    lhs, i = sub(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.ADDITION:
        rhs, i = sub(ts, i+1)
        lhs = ast(C.ADDITION, lhs, rhs)

    return lhs, i


def sub(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 - 2')
    ast('-', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected subtraction, found EOF')

    lhs, i = mul(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.SUBTRACTION:
        rhs, i = mul(ts, i+1)
        lhs = ast(C.SUBTRACTION, lhs, rhs)

    return lhs, i

def mul(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 - 2')
    ast('-', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected subtraction, found EOF')

    lhs, i = div(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.MULTIPLICATION:
        rhs, i = div(ts, i+1)
        lhs = ast(C.MULTIPLICATION, lhs, rhs)

    return lhs, i

def div(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 - 2')
    ast('-', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected subtraction, found EOF')

    lhs, i = mod(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.DIVISION:
        rhs, i = mod(ts, i+1)
        lhs = ast(C.DIVISION, lhs, rhs)

    return lhs, i

def mod(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 - 2')
    ast('-', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected subtraction, found EOF')

    lhs, i = expo(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.MODULUS:
        rhs, i = expo(ts, i+1)
        lhs = ast(C.MODULUS, lhs, rhs)

    return lhs, i

def expo(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('1 - 2')
    ast('-', ast('cons', 1), ast('cons', 2))
    """
    if i >= len(ts):
        raise SyntaxError('expected exponentiation, found EOF')

    lhs, i = disj(ts, i)

    left = i - 1
    # while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == '^':
    #     rhs, i = disj(ts, i+1)
    #     lhs = ast('^', lhs, rhs)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == C.EXPONENTIATION:
        rhs, i = disj(ts, i+1)

    right = i
    if left != right - 1:
        return expo_right(ts[left: right + 1]), right
    else:
        return lhs, i

def expo_right(lst):
    i = len(lst) - 1
    rhs, i = atom(lst, i)
    i -= 2
    while i >= 0 and lst[i].typ == C.OPERATOR and lst[i].val == C.EXPONENTIATION:
        lhs, i = atom(lst, i-1)
        i -= 2
        rhs = ast(C.EXPONENTIATION, lhs, rhs)
    return rhs


def disj(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('true || false')
    ast('||', ast('val', True), ast('val', False))
    """
    if i >= len(ts):
        raise SyntaxError('expected conjunction, found EOF')

    lhs, i = conj(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == '||':
        rhs, i = conj(ts, i+1)
        lhs = ast('||', lhs, rhs)

    return lhs, i

def conj(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('true && false')
    ast('&&', ast('val', True), ast('val', False))
    >>> parse('!x && (a && !false)')
    ast('&&', ast('!', ast('var', 'x')), ast('&&', ast('var', 'a'), ast('!', ast('val', False))))
    >>> parse('!x && a && !false')
    ast('&&', ast('&&', ast('!', ast('var', 'x')), ast('var', 'a')), ast('!', ast('val', False)))
    """
    if i >= len(ts):
        raise SyntaxError('expected conjunction, found EOF')

    lhs, i = neg(ts, i)

    while i < len(ts) and ts[i].typ == C.OPERATOR and ts[i].val == '&&':
        rhs, i = neg(ts, i+1)
        lhs = ast('&&', lhs, rhs)

    return lhs, i

def neg(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('! true')
    ast('!', ast('val', True))
    >>> parse('!! true')
    ast('!', ast('!', ast('val', True)))
    """

    if i >= len(ts):
        raise SyntaxError('expected negation, found EOF')

    if ts[i].typ == C.OPERATOR and ts[i].val == '!':
        a, i = neg(ts, i+1)
        return ast('!', a), i
    else:
        return print(ts, i)

def pre(ts: list[tokenizer], i: int):
    """
    >>> parse('! true')
    ast('!', ast('val', True))
    >>> parse('!! true')
    ast('!', ast('!', ast('val', True)))
    """

    if i >= len(ts):
        raise SyntaxError('expected negation, found EOF')

    if ts[i].typ == C.OPERATOR and ts[i].val == '++':
        a, i = pre(ts, i+1)
        return ast('++', a), i
    elif ts[i].typ == C.OPERATOR and ts[i].val == '--':
        a, i = pre(ts, i+1)
        return ast('--', a), i
    elif ts[i].typ == C.OPERATOR and ts[i].val == '-':
        a, i = pre(ts, i+1)
        return ast('-', a), i
    else:
        return print(ts, i)

def print(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    if i >= len(ts):
        raise SyntaxError('expected print, found EOF')

    if ts[i].typ == C.PRINT:
        ap = ast(C.PRINT,)
        i = i + 1
        while i < len(ts):
            a, i = atom(ts, i)
            if a:
                ap.children = ap.children + (a,)
        return ap, i
    else:
        return atom(ts, i)

def atom(ts: list[tokenizer], i: int) -> tuple[ast, int]:
    """
    >>> parse('x')
    ast('var', 'x')
    >>> parse('true')
    ast('val', True)
    >>> parse('(((false)))')
    ast('val', False)
    """

    t = ts[i]

    if t.typ == C.VARIABLE:
        return ast(C.VARIABLE, t), i+1
    elif t.typ == C.BOOLEAN and t.val in ['true', 'false']:
        return ast(C.BOOLEAN, t), i + 1
    elif t.typ == C.NUMBER:
        return ast(C.NUMBER, t), i + 1
    elif t.typ == C.OPERATOR and t.val == C.LEFT_PARENTHESES:
        a, i = equal(ts, i + 1)

        if i >= len(ts):
            raise SyntaxError(f'expected right paren, got EOF')

        if not (ts[i].typ == C.OPERATOR and ts[i].val == C.RIGHT_PARENTHESES):
            raise SyntaxError(f'expected right paren, got "{ts[i]}"')

        return a, i + 1

    elif t.typ == C.COMMA:
        return None, i + 1
    # elif t.typ == C.OPERATOR and t.val == C.SUBTRACTION:
    #     return ast(C.NUMBER, t), i + 1


    raise SyntaxError(f'expected atom, got "{ts[i]}"')


