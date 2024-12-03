#include<bits/stdc++.h>
using namespace std;

int gcd(int a, int b) {
    if (a == 0) return b;  // 基本递归条件
    return gcd(b % a, a);  // 递归调用gcd
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        int x, y;
        cin >> x >> y;
        cout << gcd(x, y) << '\n';  // 输出gcd结果
    }
    return 0;
}