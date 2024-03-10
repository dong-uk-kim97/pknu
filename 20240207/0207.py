# def hello():
#     print('Hello, world!')

# hello()    

def calc1(x): 
    a, b = int(input().split())
    if x == 1:
        print(a+b)
    elif x==2:
        print(a-b)
    elif x==3:
        print(a*b)
    elif x==4:
        print(a//b)
    else:
        print("That's not a key. Please use 1 or 2 or 3 or 4.")

calc1(5)

# def calc2(a,b):
#     add = a+b
#     ms = a - b
#     mul = a *b
#     div = a//b
#     print(add,ms,mul,div,sep='\n')

# calc(10,20)