#include <bits/stdc++.h>

using namespace std;

bool chk (int num){
    int cnt = 0;
    while (num){
        if (cnt >= 3) break;
        if (num%10 == 6) cnt++;
        else cnt = 0;
        num /= 10;
    }
    if (cnt >= 3) return true;
    return false;
}

int main(){
    int N;
    cin >> N;
    int cnt = 0;
    long long num = 1;
    while (cnt < N){
        if (chk(num)) cnt++;
        num++;
    }
    cout << num - 1;
}