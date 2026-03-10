#include <iostream>
#include <algorithm>
#include <vector>
#include <stack>
#include <cstring>

using namespace std;
#define OUTPUT true

long long operations = 0;
int N;
struct strokes{int x, y, w;};
struct config{
    vector <strokes> current_sol;
    int board[20][20];
    int empty_count;

    config(){
        memset(board, 0, sizeof(board));
        empty_count = N*N;
    }

    inline bool find_empty(int &x, int &y){
        for (int i = 0 ; i < N; i++){
            for(int j = 0; j < N; j++){
                operations++;
                if (board[i][j] == 0){
                    x = i, y = j;
                    return true;
                }
            }
        }
        return false;
    }

    inline bool can_place(int x, int y, int side){
        operations++;
        if (side > N - 1) return false;
        if (x + side > N || y + side > N) return false;
        
        for (int i = 0; i < side; i++){
            for (int j = 0; j < side; j++){
                operations++;
                if (board[x+i][y+j] != 0) return false;
            }
        }
        return true;
    }

    inline void set_square(int x, int y, int side){
        for (int i = 0; i < side; i++){
            for (int j = 0; j < side; j++){
                operations++;
                board[x+i][y+j] = 1;
            }
            
        }
        empty_count -= side*side;
    }
};

vector <strokes> best_sol;

void print_sol(vector<strokes> solution){
    cout << solution.size() << endl;
    for (auto& i : solution){
        cout << i.x + 1 << " " << i.y + 1 << " " << i.w << "\n";
    }
}

vector <strokes> initial_sol(){
    vector <strokes> sol;
    sol.push_back({0, 0, N - 1});
    operations++;
    for (int i = 0; i < N; i++){
        sol.push_back({N-1, i, 1});
        operations++;
    }
    for (int i = 0; i < N-1; i++){
        sol.push_back({i, N-1, 1});
        operations++;
    }
    return sol;
}


int backtracking(bool draw=false){
    if (N%2 == 0){
        if (OUTPUT) cout << "[EVEN] N=" << N << " 4 квадрата размера " << N/2 << endl;
        vector <strokes> sol;
        int side = N/2;
        sol.push_back({0, 0, side});
        sol.push_back({0, side, side});
        sol.push_back({side, 0, side});
        sol.push_back({side, side, side});
        operations += 4;
        // print_sol(sol);
        return 0;
    }

    stack<config> st;
    config start;
    st.push(start);
    
    best_sol = initial_sol();

    while(!st.empty()){
        config cur = st.top();
        st.pop();
        operations++;

        if (draw && OUTPUT){
            cout << "достали новое состояние из стека:";
            cout << "\n\n";
            cout << "\nКвадратов: " << cur.current_sol.size()<< ", Пустых: " << cur.empty_count << "\n";
            int color = 1;
            for (const auto& square : cur.current_sol) {
                int x = square.x;
                int y = square.y;
                int size = square.w;
                for (int i = x; i < x + size; ++i) {
                    for (int j = y; j < y + size; ++j) {
                        cur.board[i][j] = color;
                    }
                }
                color++;
            }

            for (int i = 0; i < N; ++i) {
                for (int j = 0; j < N; ++j) {
                    cout << cur.board[j][i] << " ";
                }
                cout << endl;
            }
            cout << "\n\n";

        }


        int x, y;
        if (!cur.find_empty(x, y)) {
            if (cur.current_sol.size() < best_sol.size()){
                if (OUTPUT){
                    cout << "новое лучшее решение: " << cur.current_sol.size() << " квадратов" << endl;
                }
                best_sol = cur.current_sol;
            }
            operations++;
            continue;
        }
        
        if (cur.current_sol.size() >= best_sol.size()){
            if (OUTPUT) {
                cout << "отсекли: уже " << cur.current_sol.size() << " квадратов (рекорд: " << best_sol.size() << ")" << endl;
            }
            operations++;
            continue;
        }

        int max_size = min(N-x, N-y);
        if (max_size > N - 1) max_size = N-1;
        if (cur.current_sol.size() + cur.empty_count / (max_size*max_size) >= best_sol.size() ){
            if (OUTPUT) {
                cout << "отсекли по оценке. Даже заполнив самым лучшим образом рекорд не улучшить" << endl;
            }
            operations++;
            continue;
        }
        int min_size = (cur.current_sol.empty()) ? N / 2 : 0;
        
        while (max_size > 0 && !cur.can_place(x, y, max_size)) {
            operations++;
            max_size--;
        }
        
        if (OUTPUT && cur.current_sol.empty()) {
            cout << "Начинаем с клетки (" << x+1 << "," << y+1 << "), пробуем размеры от " << max_size << " до " << min_size+1 << endl;
        }

        for (int size = max_size; size > min_size; size--){
            operations++;   
            
            if (cur.can_place(x, y, size)){
                if (OUTPUT) {
                    cout << "квадрат " << size << "×" << size << " в (" << x+1 << "," << y+1 << ")" << endl;
                }
                config next = cur;
                next.set_square(x, y, size);
                next.current_sol.push_back({x, y, size});
                st.push(next);
                operations++;
            }
            if(cur.current_sol.size() == 0){
                int side = N - size;
                if (OUTPUT && cur.can_place(x, y, size)) {
                    cout << "эвристика: сразу 3 квадрата (" << size << "×" << size << ", " << side << "×" << side << ", " << side << "×" << side << ")" << endl;
                }
                config next_next;
                next_next.set_square(0, 0, size);
                next_next.set_square(size, 0, side);
                next_next.set_square(0, size, side);
                next_next.current_sol.push_back({x, y, size});
                next_next.current_sol.push_back({size, 0, side});
                next_next.current_sol.push_back({0, size, side});
                st.push(next_next);
                operations += 3;
            }
        }
    }

    if (draw){
        cout << "\n";
        config cur;
        int color = 1;
        for (const auto& square : best_sol) {
            int x = square.x;
            int y = square.y;
            int size = square.w;
            for (int i = x; i < x + size; ++i) {
                for (int j = y; j < y + size; ++j) {
                    cur.board[i][j] = color;
                }
            }
            color++;
        }

        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                cout << cur.board[j][i] << " ";
            }
            cout << endl;
        }
        cout << "\n\n";

    }

    print_sol(best_sol);
    return 0;
}

void testing(){
    // N = 2;
    // backtracking(true);
    // N = 20;
    // backtracking(true);
    // N = 5;
    // backtracking(true);
    // N = 7;
    // backtracking(true);

    // N = 2;
    // backtracking();
    // cout << "\n============" << " N = " << N << ". Operations: " << operations << "  ============\n";
    // operations = 0;


    N = 5;
    backtracking(true);
    cout << "\n============" << " N = " << N << ". Operations: " << operations << "  ============\n";
    operations = 0;

    
    // N = 6;
    // backtracking();
    // cout << "\n============" << " N = " << N << ". Operations: " << operations << "  ============\n";
    // operations = 0;


    // N = 7;
    // backtracking();
    // cout << "\n============" << " N = " << N << ". Operations: " << operations << "  ============\n";
    // operations = 0;


    // N = 19;
    // backtracking();
    // cout << "\n============" << " N = " << N << ". Operations: " << operations << "  ============\n";
    // operations = 0;
    // for (int i = 2; i < 20; i++)
    // {
    //     N = i;
    //     backtracking();
    //     cout << "\n============" << " N = " << N << ". Operations: " << operations << "  ============\n";
    //     operations = 0;
    // }
    
}

int main(){
    // cin >> N;
    // backtracking();
    testing();
    return 0;
}