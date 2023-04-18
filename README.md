### Group:

Hai Yuan hyuan12@stevens.edu    Thrinath Reddy Adaboina tadaboin@stevens.edu

### GitHub repo:

https://github.com/hyuan12/basic_calculator

### hours we spent on the project

We spent about 50 hours in total

### a description of how you tested your code

I pre-write the test code into a txt file, read the program inside and run it every time the project runs, and judge whether it matches through the output.

### any bugs or issues you could not resolve

1) Handling of negative numbers and priority issues
2) In the gradescope test, it will be stuck for unknown reasons until it times out

### an example of a difficult issue or bug and how you resolved

When learning ast, it is difficult for me to understand the recursive calls between several operator methods, the connection between methods, and the structure of ast nodes. After that, I consulted a lot of information, as well as teaching videos on udemy, and understood that the method in the parse process is based on low priority -> high recursion, the specific composition of ast nodes, how to build a tree structure, and how to evaluate it

### a list of the four extensions you’ve chosen to implement

1) Op-equals

I carry out the implementation of op= for each binary operation op. That is to say, I create +=, -=, *=, /=, %= and ^=. The significance of x op= e ought to be identical to x = x op (e). So, when the input is:

```
a=5
b=6
a-=3
b*=a
b+=8
print a,b
```
the output should be:

```
2.0 20.0
```

2) Relational operations

Perform the implementation of relational operations, namely ==, <=, >=, !=, <, and >, utilizing 0 to denote false and 1 to represent true. As an example, the comparison 5 > 3 would yield the value 1. To maintain consistency in the order of evaluation, relational operators must have lower precedence than arithmetic operators and be left associative. So, when the input is:

```
print 1<2,1>2,1<=1,2<=3
```

the output should be:

```
1 0 1 1
```

3) Control flow

Include functionality for if and while statements in the program. The condition ought to interpret any value that is not equal to zero as true. So, when the input is:

```
n = 5
x = 1
while (n - 1) {
x = x * n
n = n - 1
}
print x
```

the output should be:

```
120.0
```

4) Comments

Comments spanning multiple lines start with /* and end with */, and can contain any number of line breaks in between. The program does not require support for comments nested within other comments.

To create a comment that spans only a single line, use the # character. Anything following the # symbol on the same line will be treated as a comment and ignored by the program. So, when the input is:

```
x = 1
/*
x = 2
y = 3
*/
y = 4
# print 0
print x, y
```
the output should be:

```
1.0 4.0
```


