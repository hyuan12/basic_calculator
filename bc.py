from parser import parse
from evaluator import evaluate
import tokenizer
def main():
    e = evaluate()
    res = []
    try:
        while True:
            line = input('-> ') + '\n'
            # line = input() + '\n'
            # tokenize
            ts = tokenizer.lex(line)
            print(ts)

            # parse
            p = parse()
            lst = p.parse_tokens(ts)
            print(lst, len(lst))

            # evaluate
            for ast in lst:
                output = e.eva(ast)
                if output:
                    res.append(output)
            # print(res)
    except EOFError:
        for _ in res:
            print(_)



if __name__ == '__main__':
    main()