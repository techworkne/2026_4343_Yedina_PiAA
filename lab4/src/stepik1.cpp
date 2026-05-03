#include <vector>
#include <string>
#include <iostream>

using namespace std;

vector<int> prefic_func(string str){
    vector<int> p(str.size(), 0);
    p.push_back(0);
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


vector<int> kmp(string p, string t){
    int lengthP = p.size();
    int lengthT = t.size();
    vector<int> ans;

    string combined = p + "#" + t;

    vector<int> pi = prefic_func(combined);
    int count = 0;

    for (int i = lengthP; i < combined.size(); i++){
        if (pi[i] == lengthP){
            int pos = i - 2 * lengthP;
            ans.push_back(pos);
        }
    }
    return ans;
}

int main(){
    string p;
    cin >> p;
    string t;
    cin >> t;
    vector<int> answer = kmp(p, t);
    if (answer.size() > 1){

        for (int i = 0; i < answer.size(); i++){
            cout << answer[i];
            if (i != answer.size() - 1){
                cout << ",";
            }
        }

        cout << endl;
    }else{
        cout << -1 << endl;
    }
}