import sys
from functools import lru_cache

DEBUG = True

def log(message):
    if DEBUG:
        print(message)

def solve_tsp_exact_dp(matrix):
    n = len(matrix)
    all_visited_mask = (1 << n) - 1

    @lru_cache(None)
    def visit(current_city, visited_mask):
        if visited_mask == all_visited_mask:
            return_cost = matrix[current_city][0]
            if return_cost == 0:
                log(f"Все посещены. Тупик: нет пути из {current_city} в 0.")
                return float('inf'), []
            
            log(f"Все посещены. Возврат {current_city} -> 0. Вес: {return_cost}")
            return return_cost, [0]

        min_cost = float('inf')
        best_path_suffix = []

        log(f"Город={current_city}, Маска={bin(visited_mask)}")

        for next_city in range(n):
            city_not_visited = not (visited_mask & (1 << next_city))
            path_exists = matrix[current_city][next_city] != 0

            if city_not_visited and path_exists:
                edge_cost = matrix[current_city][next_city]
                new_visited_mask = visited_mask | (1 << next_city)
                log(f"  --> Пытаемся перейти: {current_city} -> {next_city} (вес ребра {edge_cost})")
                remaining_cost, remaining_path = visit(next_city, new_visited_mask)
                total_cost = edge_cost + remaining_cost
                
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_path_suffix = [next_city] + remaining_path

        log(f"[ИТОГ] Город={current_city}, Маска={bin(visited_mask)} -> Мин. стоимость={min_cost}")
        return min_cost, best_path_suffix

    optimal_cost, optimal_path_suffix = visit(0, 1)

    if optimal_cost == float('inf'):
        return None, None

    full_path = [0] + optimal_path_suffix
    return optimal_cost, full_path


def get_heuristic_L(matrix, visited, current_city):
    n = len(matrix)
    min_enter = float('inf')
    min_exit = float('inf')

    for u in range(n):
        if not visited[u]:
            if matrix[u][current_city] != 0 and matrix[u][current_city] < min_enter:
                min_enter = matrix[u][current_city]
            if matrix[current_city][u] != 0 and matrix[current_city][u] < min_exit:
                min_exit = matrix[current_city][u]

    if min_enter == float('inf') or min_exit == float('inf'):
        return float('inf')

    return (min_enter + min_exit) / 2.0


def solve_tsp_approx_alsh1(matrix):
    n = len(matrix)
    visited = [False] * n
    path = [0]
    visited[0] = True
    current_cost = 0.0
    current_city = 0

    log("\n--- ЗАПУСК АЛШ-1 ---")

    while len(path) < n:
        best_value = float('inf')
        best_next_city = -1
        best_edge_cost = 0

        if len(path) == n - 1:
            for i in range(n):
                if not visited[i]:
                    best_next_city = i
                    best_edge_cost = matrix[current_city][i]
                    break
        else:
            for candidate_city in range(n):
                if not visited[candidate_city] and matrix[current_city][candidate_city] != 0:
                    s = matrix[current_city][candidate_city]
                    
                    visited[candidate_city] = True
                    L = get_heuristic_L(matrix, visited, candidate_city)
                    visited[candidate_city] = False

                    value = s + L
                    log(f"  Кандидат {candidate_city}: s={s}, L={L}, s+L={value}")

                    if value < best_value:
                        best_value = value
                        best_next_city = candidate_city
                        best_edge_cost = s

        if best_next_city == -1 or best_edge_cost == 0:
            log("  Тупик! Нет доступных городов.")
            return None, None

        path.append(best_next_city)
        visited[best_next_city] = True
        current_cost += best_edge_cost
        current_city = best_next_city
        log(f"-> Выбран город {current_city}, стоимость шага: {best_edge_cost}")

    closing_cost = matrix[current_city][0]
    if closing_cost == 0:
        log("  Тупик! Нет пути в начальный город.")
        return None, None
        
    current_cost += closing_cost
    path.append(0)
    log(f"-> Замыкание цикла в 0, стоимость: {closing_cost}\n")

    return current_cost, path


def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    matrix = []
    idx = 1
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append(int(input_data[idx]))
            idx += 1
        matrix.append(row)

    cost, path = solve_tsp_exact_dp(matrix)

    if DEBUG:
        approx_cost, approx_path = solve_tsp_approx_alsh1(matrix)
        print("=== РЕЗУЛЬТАТЫ ПРИБЛИЖЕННОГО АЛГОРИТМА (АЛШ-1) ===")
        if approx_cost is None:
            print("no path\n")
        else:
            print(f"Стоимость: {approx_cost}")
            print(f"Путь: {' '.join(map(str, approx_path))}\n")
        print("=== РЕЗУЛЬТАТЫ ТОЧНОГО АЛГОРИТМА (ДП) ===")

    if cost is None:
        print("no path")
    else:
        print(cost)
        print(" ".join(map(str, path)))

if __name__ == "__main__":
    main()