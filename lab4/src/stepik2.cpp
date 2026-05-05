#include <vector>
#include <string>
#include <iostream>

using namespace std;

vector<int> prefic_func(string str){
    cout << "\nпрефикс-функция для строки B = \"" << str << "\"\n";
    vector<int> p(str.size(), 0);
    for (int i = 1; i < str.size(); i++){
        int k = p[i - 1];
        cout << "  i=" << i << " char='" << str[i] << "' k=" << k;
        while (k > 0 && str[i] != str[k]){
            cout << "    несовпадение '" << str[i] << "' != '" << str[k] << "', k = p[" << k-1 << "] = " << p[k-1] << endl;
            k = p[k - 1];
        }
        if (str[i] == str[k]){
            k++;
            cout << " -> совпадение, k=" << k;
        } else {
            cout << " -> нет совпадения, k=" << k;
        }
        p[i] = k;
        cout << " -> p[" << i << "]=" << k << endl;
    }
    cout << "итоговая префикс-функция: ";
    for (int v : p) cout << v << " ";
    cout << endl;
    return p;
}


int kmp_cycle(string A, string B){
    vector<int> ans;

    vector<int> pi = prefic_func(B);
    int k = 0; // нынешнее состояния совпадения
    int n = A.size();

    cout << "A = " << A << ", B = " << B << ", длина n = " << n << endl;

    cout << "\nпроход по удвоенной строке A\n";
    for (int i = 0; i < 2*n ; i++)
    {
        // с помощью модульнрой арифметики избегаю создания 2А. abcabc
        // a -> i = 0 -> 0%3 = 0; 1%3=1; 2%3=2; 3%3=0; 4%3=1 ...
        char current_char = A[i % n];
        cout << "\nшаг i=" << i << " (символ A[" << i % n << "] = '" << current_char
             << "'), текущее совпадение k=" << k;

        while (k > 0 && current_char != B[k]){
            cout << " -> несовпадение с B[" << k << "]='" << B[k] << "', переходим k=pi[" << k-1 << "]=" << pi[k-1];
            k = pi[k - 1];
        }
        if (current_char == B[k]){
            k++;
            cout << " -> символы совпали (B[" << k-1 << "]='" << B[k-1] << "'), k++ => " << k;
        } else {
            cout << " -> нет совпадения, k остаётся " << k;
        }

        if (k == n){
            int pos = i - n + 1;
            cout << "позиция начала вхождения в строке: pos = " << i << " - " << n << " + 1 = " << pos << endl;
            if (pos < n){
                cout << "pos < n => возвращаем " << pos << " (циклический сдвиг на " << pos << " влево)\n";
                return pos;
            }else{
                cout << "pos >= n, но такого не должно случиться, возвращаем -1\n";
                return -1;
            }
        }
    }
    cout << "\nциклический сдвиг не найден за 2n итераций\n";
    return -1;
}

int main(){
    string A, B;
    cin >> A >> B;

    if (A.size() != B.size()){
        cout << "строки разной длины => -1\n";
        cout << -1 << endl;
        return 0;
    }

    int answer = kmp_cycle(A, B);

    cout << answer << endl;
    return 0;
}
