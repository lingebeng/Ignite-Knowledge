from sys import stdin

input = lambda:stdin.readline().strip()

def gcd_func(a,b):


T = int(input())

for _ in range(T):
    a,b = map(int,input().split())
    print(gcd_func(a,b))