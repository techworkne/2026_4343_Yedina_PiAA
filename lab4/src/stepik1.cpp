#include <vector>
#include <string>
#include <iostream>

using namespace std;

vector<int> prefic_func(string str){
    cout << "\nвычисление префикс-функции для строки: " << str << "\n";
    vector<int> p(str.size(), 0);
    for (int i = 1; i < str.size(); i++){
        int k = p[i - 1];
        cout << "\ni = " << i << ", символ '" << str[i] << "', начальное k = " << k << endl;
        while (k > 0 && str[i] != str[k]){
            cout << "    несовпадение '" << str[i] << "' != '" << str[k] << "', k = p[" << k-1 << "] = " << p[k-1] << endl;
            k = p[k - 1];
        }
        if (str[i] == str[k]){
            cout << "    совпадение '" << str[i] << "' == '" << str[k] << "', k++ => " << k+1 << endl;
            k++;
        } else {
            cout << "    нет совпадения, k остаётся " << k << endl;
        }
        p[i] = k;
        cout << "  p[" << i << "] = " << k << endl;
    }
    cout << "префикс-функция: ";
    for (int v : p) cout << v << " ";
    cout << endl;
    return p;
}


vector<int> kmp(string p, string t){
    int lengthP = p.size();
    int lengthT = t.size();
    vector<int> ans;

    string combined = p + "#" + t;

    cout << "\nформирование комбинированной строки: " << combined << "\n";
    cout << "длина шаблона = " << lengthP << endl;

    vector<int> pi = prefic_func(combined);
    int count = 0;

    cout << "\nпоиск вхождений (позиции pi[i] == " << lengthP << ")\n";

    for (int i = lengthP; i < combined.size(); i++){
        cout << "i = " << i << ", pi[" << i << "] = " << pi[i] << " (символ '" << combined[i] << "')";
        if (pi[i] == lengthP){
            int pos = i - 2 * lengthP;
            cout << " найдено вхождение. позиция в тексте = " << pos << endl;
            ans.push_back(pos);
        } else {
            cout << endl;
        }
    }
    return ans;
}

int main(){
    string p, t;
    cin >> p >> t;
    vector<int> answer = kmp(p, t);
    if (!answer.empty()){

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
