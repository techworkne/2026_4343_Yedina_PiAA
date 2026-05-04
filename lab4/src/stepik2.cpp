#include <vector>
#include <string>
#include <iostream>

using namespace std;

vector<int> prefic_func(string str){
    vector<int> p(str.size(), 0);
    for (int i = 1; i < str.size(); i++){
        int k = p[i - 1];
        while (k > 0 and str[i] != str[k]){
            k = p[k - 1];
        }
        if (str[i] == str[k]){
            k++;
        }
        p[i] = k;
    }
    return p;
}


int kmp_cycle(string A, string B){
    int lengthB = B.size();
    vector<int> ans;
    
    vector<int> pi = prefic_func(B);
    int k = 0; // нынешнее состояния совпадения
    int n = A.size();

    for (int i = 0; i < 2*n ; i++)
    {
        // с помощью модульнрой арифметики избегаю создания 2А. abcabc
        // a -> i = 0 -> 0%3 = 0; 1%3=1; 2%3=2; 3%3=0; 4%3=1 ...
        char current_char = A[i % n];

        while (k > 0 && current_char != B[k]){
            k = pi[k - 1];
        }
        if (current_char == B[k]){
            k++;
        }

        if (k == n){
            int pos = i - n + 1;
            if (pos < n) return pos;
            else
                return -1;
        }
    }

    return -1;
}

int main(){
    string A, B;
    cin >> A >> B;

    if (A.size() != B.size()){
        cout << -1 << endl;
        return 0;
    }

    int answer = kmp_cycle(A, B);

    cout << answer << endl;
    return 0;
}