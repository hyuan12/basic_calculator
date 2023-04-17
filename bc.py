import sys
import traceback
from enum import Enum
import typing
import heapq


class Tokens(Enum):
    VARIABLE=0 #abc
    FUNCTION=1# abc
    NUMBER=2#  12355
    NL=3#\n

    ADD=4#+
    ADD_ASSIGN=5#+=

    MUL=6#*
    MUL_ASSIGN=7#*=

    SUB=8#-
    SUB_ASSIGN=9#-=

    DIV=10#/=
    DIV_ASSIGN=11#/=

    MOD=12#%
    MOD_ASSIGN=13#%=

    POWER=14#^
    POWER_ASSIGN=15#^=

    INCREMENT=16#++
    DECREMENT=17#--

    ASSIGN=18#=
    EQUALITY=19#==

    LESS_EQUALITY=20#<=
    GREATER_EQUALITY=21#>=
    LESS=22#<
    GREATER=23#>
    NOT_EQUALITY=24#!=
    NOT=25#!
    AND=26# &&
    OR=27#||

    COMMENT=28# #
    COMMENT_START=29#/*
    COMMENT_END=30#*/


    DEFINE=31#define xxx
    LPAREN=32#(
    RPAREN=33#)
    LBRACE=34#{
    RBRACE=35#}
    COMMA=36#,
    IF=37#if
    WHILE=38#while
    RETURN=39#return

    PRINT=40

    END=41

    ELES=42



class ParseError(Exception):
    pass


class Token:
    def __init__(self,type:Tokens,value):
        self.type = type
        self.value = value
    def __repr__(self):
        return f"{self.type} '{self.value}'"


class Expression():
    def __init__(self,left=None,right=None):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Expr({self.left},{self.right})"

class AssignmentExpression(Expression):
    def __init__(self,op:Tokens,var:Token,expr:Expression):
        self.var=var
        self.expr=expr
        self.op=op
    def __repr__(self):
        return f"{self.var.value} {self.op} {self.expr}"

class OperatorExpression(Expression):
    def __init__(self,op:Tokens=None,left:Expression=None,right:Expression=None):
        self.op=op
        self.left=left
        self.right=right
    def __repr__(self):
        return f"{self.left} { self.op} {self.right}"

class BlockExpression(Expression):
    def __init__(self,expressions:typing.List[Expression]):
        self.exprs=expressions
    def __repr__(self):
        s="{\n"
        for i in self.exprs:
            s+="\t"+repr(i)+"\n"
        s+="}"
        return s

class VariableExpression(Expression):
    def __init__(self,var:Token):
        self.var=var
    def __repr__(self):
        return f"{self.var}"
class NumberExpression(Expression):
    def __init__(self,number:Token):
        self.var=number

    def __repr__(self):
        return f"{self.var.value}"
class ArgumentExpression(Expression):
    def __init__(self,arguments:typing.List[Expression]):
        self.args=arguments
    def __repr__(self):
        s="("
        for i in self.args:
            s+=repr(i)
            if i!=self.args[-1]:
                s+=','
        s+=")"
        return s

class PrintExpression(Expression):
    def __init__(self,exprs):
        self.exprs=exprs
    def __repr__(self):
        s = "{\n"
        for i in self.exprs:
            s += "\t" + repr(i) + "\n"
        s += "}"
        return s

class IFExpression(Expression):
    def __init__(self,rel_op:Expression,block:BlockExpression,eblock:BlockExpression=None):
        self.cond=rel_op
        self.block=block
        self.eblock=eblock

    def __repr__(self):
        if self.eblock:
            return f"if({self.cond}) {self.block}"
        else:
            return f"if({self.cond}) {self.block} else {self.eblock}"
class WhileExpression(Expression):
    def __init__(self,rel_op:Expression,block:BlockExpression):
        self.cond=rel_op
        self.block=block

    def __repr__(self):
        return f"if({self.cond}) {self.block}"

class Parser():
    def __init__(self,tokens):
        self.tokens:typing.List[Token]=tokens
        self.current=0


    @property
    def token(self):
        return self.tokens[self.current]
    def precedence(self, type:Tokens):
        if type==Tokens.LPAREN:
            return 0
        elif type==Tokens.INCREMENT or type==Tokens.DECREMENT:
            return 1
        elif type==Tokens.MUL or type==Tokens.MOD or type==Tokens.DIV or type==Tokens.POWER:
            return 2
        elif type==Tokens.ADD or type==Tokens.SUB:
            return 3
        elif type == Tokens.EQUALITY or type == Tokens.LESS or type == Tokens.GREATER or type == Tokens.LESS_EQUALITY or type == Tokens.GREATER_EQUALITY or type == Tokens.AND or type==Tokens.OR:
            return 4
        return 999
    def parse_argument(self):
        if self.next(Tokens.LPAREN):
            arg=ArgumentExpression([])
            while self.token.type!=Tokens.RPAREN and self.token.type!=Tokens.END:
                self.current+=1
                if self.token.type!=Tokens.COMMA:
                    o=self.parse_expression()
                    if o:
                        arg.args.append(o)
            self.current+=1
            return arg
    def parse_term(self):
        if self.next(Tokens.NUMBER):
            self.current+=1
            return NumberExpression(self.token)
        elif self.next(Tokens.VARIABLE):
            self.current+=1
            return VariableExpression(self.token)
        elif self.next(Tokens.LPAREN):
            self.current+=1
            e=self.parse_expression()
            self.current+=1
            return e

    def parse_expression(self):
        left = self.parse_term()
        while self.next(Tokens.ADD) or self.next(Tokens.SUB) or self.next(Tokens.MUL) or self.next(
                Tokens.DIV) or self.next(Tokens.POWER) or self.next(Tokens.MOD) or self.next(
                Tokens.EQUALITY) or self.next(Tokens.LESS_EQUALITY) or self.next(Tokens.GREATER_EQUALITY) or self.next(
                Tokens.LESS) or self.next(
                Tokens.GREATER) or self.next(Tokens.AND) or self.next(Tokens.OR):
            # if self.tokens[self.current ].type != Tokens.NUMBER and self.tokens[
            #     self.current].type != Tokens.VARIABLE and self.next(Tokens.SUB) and not self.next(Tokens.LPAREN):
            #     self.current+=1
            #     if left==None:
            #         l=self.parse_term()
            #         l.var.value=str(float(l.var.value)*-1)
            #         self.current-=1
            #         return self.parse_expression()
            #     else:
            #         l = self.parse_term()
            #         l.var.value = str(float(l.var.value)*-1)
            #         left.right=NumberExpression(l.var)
            #         return left
            self.current += 1
            op = self.token
            right = self.parse_term()
            while self.next(Tokens.POWER):
                self.current += 1
                op2 = self.token
                right2 = self.parse_term()
                right = OperatorExpression(op2, right, right2)
            while self.next(Tokens.MUL) or self.next(Tokens.DIV) or self.next(Tokens.MOD):
                self.current += 1
                op2 = self.token
                right2 = self.parse_term()
                right = OperatorExpression(op2, right, right2)
            left = OperatorExpression(op, left, right)
        return left

    def assignment_statement(self):
        if self.next(Tokens.ASSIGN) or self.next(Tokens.ADD_ASSIGN) or self.next(Tokens.SUB_ASSIGN) or self.next(Tokens.MOD_ASSIGN) or self.next(Tokens.MUL_ASSIGN)or self.next(Tokens.DIV_ASSIGN) or self.next(Tokens.POWER_ASSIGN) or self.next(Tokens.INCREMENT) or self.next(Tokens.DECREMENT):
            self.current+=1
            return AssignmentExpression(
                self.tokens[self.current],
                self.tokens[self.current-1],
                self.parse_expression()
            )
    def next_operator_predicate(self):
        c=self.current
        while self.tokens[c].type!=Tokens.END and self.tokens[c].type!=Tokens.NL:
            c=self.tokens[c]
            if c.type in (Tokens.AND,Tokens.SUB,Tokens.MUL,Tokens.MOD,Tokens.DIV,Tokens.POWER):
                return self.precedence(c.type)
        return 999

    def parse_block(self):
        block=BlockExpression([])
        self.current += 1
        while self.token.type!=Tokens.RBRACE and self.token.type!=Tokens.END:
            stmt=self.parse_statement()
            if stmt:
                block.exprs.append(stmt)
            else:
                self.current+=1
        return block
    def next(self,token:Tokens,num=1):
        if self.tokens[self.current+num].type!=Tokens.END:
            if self.tokens[self.current+num].type==token:
                return self.tokens[self.current+num]
    def parse_statement(self):
        if self.token.type==Tokens.PRINT:
            exprs=[]
            while not self.next(Tokens.NL) and not self.next(Tokens.COMMENT):
                if self.assignment_statement():
                    raise ParseError()
                exprs.append(self.parse_expression())
                if self.next(Tokens.COMMA):
                    self.current+=1
            return PrintExpression(exprs)
        elif self.token.type==Tokens.DEFINE:
            pass
        elif self.token.type==Tokens.IF:
            i=IFExpression(
                self.parse_argument(),
                self.parse_block(),
            )
            if self.next(Tokens.ELES):
                self.current+=1
                i.eblock=self.parse_block()
            return i
        elif self.token.type==Tokens.WHILE:
            return WhileExpression(
                self.parse_argument(),
                self.parse_block(),
            )
        elif self.token.type==Tokens.LBRACE:
            return self.parse_block()
        elif self.token.type==Tokens.COMMENT:
            while self.token.type!=Tokens.NL:
                self.current+=1
        elif self.token.type==Tokens.COMMENT_START:
            while self.token.type!=Tokens.COMMENT_END:
                self.current += 1
                if self.token.type==Tokens.COMMENT_START:
                    self.parse_statement()
            self.current+=1
        elif self.token.type==Tokens.NUMBER:
            return self.parse_expression()
        elif self.token.type==Tokens.VARIABLE:
            s=self.assignment_statement()
            if s:
                return s
            raise ParseError()
        elif self.token.type==Tokens.NL:
            pass
        else:
            raise ParseError()
    def print_expr(self,expr:Expression,indent=0):
        if expr.__class__==Expression:
            print("\t|"*indent,"Expression")
            print("\t|"*indent,"Left:")
            self.print_expr(expr.left,indent+1)
            print("\t|"*indent,"Right:")
            self.print_expr(expr.right,indent+1)
        elif expr.__class__==OperatorExpression:
            print("\t|"*indent,"OperatorExpression ",expr.op)
            print("\t|"*indent,"Left:")
            self.print_expr(expr.left,indent+1)
            print("\t|"*indent,"Right:")
            self.print_expr(expr.right,indent+1)
        elif expr.__class__==NumberExpression:
            print("\t|" * indent, "NumberExpression ")
            print("\t|" * indent, "\tValue:",expr.var.value)
        elif expr.__class__==AssignmentExpression:
            print("\t|" * indent, "AssignmentExpression ")
            print("\t|" * indent, "\tOP:", expr.op)
            print("\t|" * indent, "\tVar:", expr.var)
            self.print_expr(expr.expr,indent+1)
        elif expr.__class__==IFExpression:
            print("\t|" * indent, "IFExpression")
            print("\t|" * indent, "\tCOND:", expr.cond)
            self.print_expr(expr.block,indent+1)
        elif expr.__class__==WhileExpression:
            print("\t|" * indent, "WhileExpression")
            print("\t|" * indent, "\tCOND:", expr.cond)
            self.print_expr(expr.block,indent+1)
        elif expr.__class__==BlockExpression:
            print("\t|" * indent, "BlockExpression")
            for e in expr.exprs:
                print("\t|" * indent, "\tExpr:", e)
        elif expr.__class__==PrintExpression:
            print("\t|" * indent, "PrintExpression")
            for e in expr.exprs:
                self.print_expr(e,indent+1)
        else:
            print("\t|" * indent, expr)
    def parse(self):
        program = {"type": "Program", "body": []}
        self.validate()
        while self.token.type!=Tokens.END:
            stmt=self.parse_statement()
            # self.print_expr(stmt)
            if stmt:
                program['body'].append(stmt)
            self.current+=1
        return program
    def validate(self):
        stack = []
        try:
            for i in self.tokens:
                if i.type in [Tokens.LPAREN, Tokens.LBRACE]:
                    stack.append(i)
                elif i.type == Tokens.RPAREN:
                    if stack and stack[-1].type == Tokens.LPAREN:
                        stack.pop()
                    else:
                        raise ParseError
                elif i.type == Tokens.RBRACE:
                    if stack and stack[-1].type == Tokens.LBRACE:
                        stack.pop()
                    else:
                        raise ParseError
            if stack:
                raise ParseError
        except:
            raise ParseError


class EvalProgram():
    def __init__(self,program):
        self.program=program
        self.statements = program['body']
        self.vars={}
    def eval(self):
        for stmt in self.statements:
            self.eval_statements(stmt)
    def eval_expr(self,expr):
        if expr.__class__==NumberExpression:
            return float(expr.var.value)
        elif expr.__class__==VariableExpression:
            return self.vars.get(expr.var.value,0)
        elif expr.__class__==OperatorExpression:
            l = self.eval_expr(expr.left)
            r = self.eval_expr(expr.right)
            if r==None or expr.right==None:
                raise ParseError()
            if expr.op.type==Tokens.ADD:
                return l+r
            elif expr.op.type==Tokens.SUB:
                if l==None:
                    return r*-1
                return l-r
            elif expr.op.type==Tokens.MOD:
                return l%r
            elif expr.op.type==Tokens.MUL:
                return l*r
            elif expr.op.type==Tokens.DIV:
                if r==0:
                    return "divide by zero"
                return l/r
            elif expr.op.type==Tokens.POWER:
                return l**r
            elif expr.op.type==Tokens.EQUALITY:
                return int(l==r)
            elif expr.op.type==Tokens.LESS:
                return int(l<r)
            elif expr.op.type==Tokens.LESS_EQUALITY:
                return int(l<=r)
            elif expr.op.type==Tokens.GREATER:
                return int(l>r)
            elif expr.op.type==Tokens.GREATER_EQUALITY:
                return int(l>=r)
            elif expr.op.type==Tokens.AND:
                if l and r:
                    return 1
                else:
                    return 0
            elif expr.op.type==Tokens.OR:
                if l or r:
                    return 1
                else:
                    return 0

    def eval_statements(self,stmt):
        if stmt.__class__==AssignmentExpression:
            if stmt.op.type==Tokens.ASSIGN:
                self.vars[stmt.var.value]=self.eval_expr(stmt.expr)
            elif stmt.op.type==Tokens.ADD_ASSIGN:
                self.vars[stmt.var.value]+=self.eval_expr(stmt.expr)
            elif stmt.op.type==Tokens.POWER_ASSIGN:
                self.vars[stmt.var.value]=self.vars.get(stmt.var.value)**self.eval_expr(stmt.expr)
            elif stmt.op.type==Tokens.SUB_ASSIGN:
                self.vars[stmt.var.value]-=self.eval_expr(stmt.expr)
            elif stmt.op.type==Tokens.MUL_ASSIGN:
                self.vars[stmt.var.value]*=self.eval_expr(stmt.expr)
            elif stmt.op.type==Tokens.MOD_ASSIGN:
                self.vars[stmt.var.value]%=self.eval_expr(stmt.expr)
            elif stmt.op.type==Tokens.DIV_ASSIGN:
                v=self.eval_expr(stmt.expr)
                if v==0:
                    raise ZeroDivisionError
                self.vars[stmt.var.value]/=v
            elif stmt.op.type==Tokens.INCREMENT:
                self.vars[stmt.var.value] +=1
            elif stmt.op.type==Tokens.DECREMENT:
                self.vars[stmt.var.value] -=1
        elif stmt.__class__==PrintExpression:
            res=[]
            if stmt.exprs:
                for e in stmt.exprs:
                    res.append(self.eval_expr(e))
                print(*res)
            else:
                raise ParseError()
        elif stmt.__class__==OperatorExpression:
            v=self.eval_expr(stmt)
            if v=="divide by zero":
                raise ZeroDivisionError
        elif stmt.__class__==IFExpression:
            if self.eval_expr(stmt.cond.args[0]):
                for expr in stmt.block.exprs:
                    self.eval_statements(expr)
            elif stmt.eblock:
                for expr in stmt.eblock.exprs:
                    self.eval_statements(expr)
        elif stmt.__class__==WhileExpression:
            while self.eval_expr(stmt.cond.args[0]):
                for expr in stmt.block.exprs:
                    self.eval_statements(expr)
        # print("Vars",self.vars)
def Lexer(program:str)->typing.List[Token]:
    program+='\n\0'
    tokens=[]
    current=0
    name=""
    while len(program)>current:
        if program[current]=="\n":
            current+=1
            tokens.append(Token(Tokens.NL, ""))
        if program[current].isspace():
            current+=1
        if program[current].isalpha():
            while program[current].isalpha() or program[current].isdigit():
                name+=program[current]
                current+=1
                if len(program) <= current:
                    break
            if name=="define":
                tokens.append(Token(Tokens.DEFINE,name))
            elif name=="if":
                tokens.append(Token(Tokens.IF,name))
            elif name=="else":
                tokens.append(Token(Tokens.ELES,name))
            elif name=="while":
                tokens.append(Token(Tokens.WHILE,name))
            elif name=="return":
                tokens.append(Token(Tokens.RETURN,name))
            elif name=="print":
                tokens.append(Token(Tokens.PRINT,name))
            else:
                tokens.append(Token(Tokens.VARIABLE, name))
            name=""
        elif program[current].isnumeric():
            dot=0
            while program[current]=="." or program[current].isnumeric():
                if program[current]==".":
                    if dot:
                        raise ParseError()
                    dot=1
                name+=program[current]
                current+=1
                if len(program) <= current:
                    break
            tokens.append(Token(Tokens.NUMBER, name))
            name = ""
        elif program[current]==",":
            current+=1
            tokens.append(Token(Tokens.COMMA,","))
        elif program[current]=="(":
            current+=1
            tokens.append(Token(Tokens.LPAREN,"("))
        elif program[current]==")":
            current+=1
            tokens.append(Token(Tokens.RPAREN,")"))
        elif program[current]=="{":
            current+=1
            tokens.append(Token(Tokens.LBRACE,"{"))
        elif program[current]=="}":
            current+=1
            tokens.append(Token(Tokens.RBRACE,"}"))
        elif program[current]=="=":
            if len(program) > current:
                if program[current+1]=="=":
                    current+=2
                    tokens.append(Token(Tokens.EQUALITY,"=="))
                else:
                    current+=1
                    tokens.append(Token(Tokens.ASSIGN,"="))
            else:
                current += 1
                tokens.append(Token(Tokens.ASSIGN,"="))
        elif program[current]=="#":
            tokens.append(Token(Tokens.COMMENT,"#"))
            current+=1
        elif program[current]=="+":
            if len(program) > current:
                if program[current+1]=="=":
                    current+=2
                    tokens.append(Token(Tokens.ADD_ASSIGN,"+="))
                elif program[current+1]=="+":
                    current += 2
                    tokens.append(Token(Tokens.INCREMENT, "++"))
                else:
                    current+=1
                    tokens.append(Token(Tokens.ADD,"+"))
            else:
                current += 1
                tokens.append(Token(Tokens.ADD,"+"))
        elif program[current]=="-":
            if len(program) > current:
                if program[current+1]=="=":
                    current+=2
                    tokens.append(Token(Tokens.SUB_ASSIGN,"-="))
                elif program[current+1]=="-":
                    current += 2
                    tokens.append(Token(Tokens.DECREMENT, "--"))
                else:
                    current+=1
                    tokens.append(Token(Tokens.SUB,"-"))
            else:
                current += 1
                tokens.append(Token(Tokens.SUB,"-"))
        elif program[current]=="*":
            if len(program) > current:
                if program[current+1]=="=":
                    current+=2
                    tokens.append(Token(Tokens.MUL_ASSIGN,"*="))
                elif program[current+1]=="/":
                    current += 2
                    tokens.append(Token(Tokens.COMMENT_END, "*/"))
                else:
                    current+=1
                    tokens.append(Token(Tokens.MUL,"*"))
            else:
                current += 1
                tokens.append(Token(Tokens.MUL,"*"))
        elif program[current]=="/":
            if len(program) > current:
                if program[current+1]=="=":
                    current+=2
                    tokens.append(Token(Tokens.DIV_ASSIGN,"/="))
                elif program[current+1]=="*":
                    current += 2
                    tokens.append(Token(Tokens.COMMENT_START, "/*"))
                else:
                    current+=1
                    tokens.append(Token(Tokens.DIV,"/"))
            else:
                current += 1
                tokens.append(Token(Tokens.DIV,"/"))
        elif program[current]=="%":
            if len(program) > current:
                if program[current+1]=="=":
                    current+=2
                    tokens.append(Token(Tokens.MOD_ASSIGN,"%="))
                else:
                    current+=1
                    tokens.append(Token(Tokens.MOD,"%"))
            else:
                current += 1
                tokens.append(Token(Tokens.MOD,"%"))
        elif program[current] == "^":
            if len(program) > current:
                if program[current + 1] == "=":
                    current += 2
                    tokens.append(Token(Tokens.POWER_ASSIGN, "^="))
                else:
                    current += 1
                    tokens.append(Token(Tokens.POWER, "^"))
            else:
                current += 1
                tokens.append(Token(Tokens.POWER, "^"))
        elif program[current] == "<":
            if len(program) > current:
                if program[current + 1] == "=":
                    current += 2
                    tokens.append(Token(Tokens.LESS_EQUALITY, "<="))
                else:
                    current += 1
                    tokens.append(Token(Tokens.LESS, "<"))
            else:
                current += 1
                tokens.append(Token(Tokens.LESS, "<"))
        elif program[current] == ">":
            if len(program) > current:
                if program[current + 1] == "=":
                    current += 2
                    tokens.append(Token(Tokens.GREATER_EQUALITY, ">="))
                else:
                    current += 1
                    tokens.append(Token(Tokens.GREATER, ">"))
            else:
                current += 1
                tokens.append(Token(Tokens.GREATER, ">"))
        elif program[current] == "!":
            if len(program) > current:
                if program[current + 1] == "=":
                    current += 2
                    tokens.append(Token(Tokens.NOT_EQUALITY, "!="))
                else:
                    current += 1
                    tokens.append(Token(Tokens.NOT, "!"))
            else:
                current += 1
                tokens.append(Token(Tokens.NOT, "!"))
        elif program[current] == "&":
            if len(program) > current:
                if program[current + 1] == "&":
                    current += 2
                    tokens.append(Token(Tokens.AND, "&&"))
                else:
                    raise ParseError
            else:
                raise ParseError
        elif program[current] == "|":
            if len(program) > current:
                if program[current + 1] == "|":
                    current += 2
                    tokens.append(Token(Tokens.OR, "||"))
                else:
                    raise ParseError
            else:
                raise ParseError
        elif program[current]=='"':
            raise ParseError
        elif program[current]=="'":
            raise ParseError
        else:
            current+=1
    tokens.append(Token(Tokens.END,"\0"))
    return tokens

if __name__ == '__main__':
    # input_text=input()
    import threading
    import time
    import os
    input_text=None
    if os.path.exists("program.txt"):
        input_text = open("program.txt").read()


    def f():
        time.sleep(1)
        os._exit(0)
    threading.Thread(target=f).start()
    try:
        if input_text==None:
            input_text = sys.stdin.read()
        tokens = Lexer(input_text)
        p = Parser(tokens)
        ast=p.parse()
        if ast['body']:
            EvalProgram(ast).eval()
        else:
            print('parse error')
    except ParseError:
        print("parse error")
    except ZeroDivisionError:
        print("divide by zero")
    except:
        print("parse error")



