from sys import stdin

input = lambda:stdin.readline().strip()

def solve(n):
    row,col = [0] * n,[0] * n
    diag,rdiag = [0] * (2 * n - 1),[0] * (2 * n - 1)
    ans = []
    def dfs(r):
        if r == n:
            tmp = []
            for i in range(n):
                tmp.append("." * col[i] + "Q" + "." * (n - col[i] - 1))
            ans.append(tmp)
            return
        for c in range(n):
            x,rx = r + c,r + n - 1 - c
            if not(row[c] or diag[x] or rdiag[rx]):
                col[r] = c
                row[c],diag[x],rdiag[rx] = 1,1,1
                dfs(r + 1)
                row[c],diag[x],rdiag[rx] = 0,0,0
    dfs(0)
    return ans

T = int(input())

for _ in range(T):
    n = int(input())
    print(solve(n))
    