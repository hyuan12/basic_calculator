import constant as C


class evaluate:
    def __init__(self):
        self.variables = {}

    def eva(self, ast):
        if ast.typ == C.NUMBER:
            return ast.children[0].val

        elif ast.typ == C.VARIABLE:
            var = ast.children[0].val
            if var in self.variables.keys():
                return self.variables[var]
            return var
            # return self.variables.get(var, 0.0)

        elif ast.typ == C.EQUAL:
            var = self.eva(ast.children[0])
            val = self.eva(ast.children[1])
            self.variables[var] = val
            # print(var, val)

        elif ast.typ in (C.SUBTRACTION, ) and len(ast.children): # and...
            exp = self.eva(ast.children[0])

            if ast.typ == C.SUBTRACTION:
                return -exp



        elif ast.typ in (C.ADDITION, C.DIVISION, C.MULTIPLICATION, C.SUBTRACTION, C.MODULUS, C.EXPONENTIATION):
            left = float(self.eva(ast.children[0]))
            right = float(self.eva(ast.children[1]))

            if ast.typ == C.ADDITION:
                return str(left + right)
            elif ast.typ == C.SUBTRACTION:
                return str(left - right)
            elif ast.typ == C.MULTIPLICATION:
                return str(left * right)
            elif ast.typ == C.DIVISION:

                if not right:
                    return "parse error"
                elif right == 0:
                    return "divide by zero"
                return str(left / right)

            elif ast.typ == C.EXPONENTIATION:
                return str(left ** right)

        # elif ast.typ in (C.SUBTRACTION, C.INCREMENT, C.DECREMENT):

        elif ast.typ == C.PRINT:
            res = [self.eva(item) for item in ast.children]
            return " ".join(str(result) for result in res)
        else:
            raise ValueError(f"Unknown AST node type: {ast.typ}")

