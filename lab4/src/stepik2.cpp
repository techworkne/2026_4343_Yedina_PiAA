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
    string doubleA = A + A;

    string combined = B + "#" + doubleA;
    vector<int> pi = prefic_func(combined);
    int firstPos = -1;

    for (int i = lengthB + 1; i < combined.size(); i++)
    {
        if (pi[i] == lengthB){
            int pos = i - 2 * lengthB;
            if (firstPos == -1) {
                firstPos = pos;
            }
            break;
        }
    }

    if (firstPos != -1 && firstPos < A.size()) {
        return firstPos;
    } else {
        return -1;
    }
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