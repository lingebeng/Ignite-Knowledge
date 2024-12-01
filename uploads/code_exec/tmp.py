from sys import stdin

input = lambda:stdin.readline().strip()

def gcd(a,b):
    return a if b == 0 else gcd(b,a % b)

def gcd_func(a,b):
    return gcd(a,b)

T = int(input())

for _ in range(T):
    a,b = map(int,input().split())
    print(gcd_func(a,b))