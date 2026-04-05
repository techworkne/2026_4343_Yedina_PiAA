#stepik
import sys


def solve():
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return

    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
    except StopIteration:
        return

    graph = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int(next(iterator)))
        graph.append(row)

    INF = float('inf')
    memo = {}
    parents = {}

    def dp(mask, last):
        if mask == 1:
            if last == 0:
                return 0
            else:
                return INF

        state = (mask, last)
        if state in memo:
            return memo[state]

        prev_mask = mask ^ (1 << last)
        min_cost = INF
        best_prev = -1

        for prev in range(n):
            if (prev_mask >> prev) & 1:
                if prev != last and graph[prev][last] != 0:
                    cost = dp(prev_mask, prev) + graph[prev][last]
                    if cost < min_cost:
                        min_cost = cost
                        best_prev = prev

        memo[state] = min_cost
        if best_prev != -1:
            parents[state] = best_prev
            
        return min_cost

    full_mask = (1 << n) - 1
    min_total_cost = INF
    last_city = -1

    for i in range(1, n):
        if graph[i][0] != 0:
            cost = dp(full_mask, i) + graph[i][0]
            if cost < min_total_cost:
                min_total_cost = cost
                last_city = i

    if min_total_cost == INF:
        print("no path")
    else:
        print(min_total_cost)
        path = []
        curr_mask = full_mask
        curr = last_city
        
        path.append(0)
        
        while curr_mask > 1:
            path.append(curr)
            prev = parents[(curr_mask, curr)]
            curr_mask ^= (1 << curr)
            curr = prev
            
        path.append(0)
        
        print(*(path[::-1]))

if __name__ == '__main__':
    solve()