#include <bits/stdc++.h>

using namespace std;

int main(){
    int N;
    cin >> N;

    int tot = 0;
    tot += N/5 + N/25 + N/125;

    cout << tot;
}