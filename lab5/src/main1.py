class Vertex:
    def __init__(self, id, road_char, alpha=5):
        self.id = id
        self.road_char = road_char
        self.next = [None] * alpha  # список переходов в боре
        self.go = [None] * alpha  # список переходов в автомате
        self.sufflink = None
        self.dict_link = None
        self.pattern_ids = []


def num(c):
    return "ACGTN".index(c)


def build(patterns):
    root = Vertex(id=0, road_char="root")
    nodes = []
    counter = 1

    for idx, p in enumerate(patterns, start=1):
        v = root

        for i in p:

            if v.next[num(i)] is None:
                v.next[num(i)] = Vertex(id=counter, road_char=i)
                nodes.append(v.next[num(i)])
                counter += 1

            v = v.next[num(i)]
        v.pattern_ids.append(idx)

    from collections import deque
    queue = deque([root])
    root.sufflink = root
    root.dict_link = root

    while queue:
        v = queue.popleft()

        for c in range(5):
            child = v.next[c]
            if child:
                # cуффиксная ссылка для ребенка
                if v == root:
                    child.sufflink = root
                else:
                    child.sufflink = v.sufflink.go[c]

                # ближайший терминальный узел в цепочке суффиксов
                if child.sufflink.pattern_ids:
                    child.dict_link = child.sufflink
                else:
                    child.dict_link = child.sufflink.dict_link

                child.go[c] = child
                queue.append(child)

            if child:
                v.go[c] = child
            else:
                if v == root:
                    v.go[c] = root
                else:
                    v.go[c] = v.sufflink.go[c]
    return root, nodes



def print_debug_info(all_nodes):
    print()
    for v in all_nodes:
        s = v.sufflink.id if v.sufflink else 0
        d = v.dict_link.id if v.dict_link else 0
        term = f" (шаблоны: {v.pattern_ids})" if v.pattern_ids else ""
        print(f"узел {v.id} ['{v.road_char}']: суффисная ссылка на узел -> {s}, сжатая ссылка на узел -> {d}{term}")
    print()

if __name__ == "__main__":

    text = input().strip()
    n = int(input())

    patterns = []
    for _ in range(n):
        patterns.append(input().strip())

    print(f"текст: {text}")
    print(f"список паттернов: {patterns}\n")

    results = []
    root, nodes = build(patterns)

    print("-"*40)
    print("бор:")
    print_debug_info(nodes)


    print()
    print("-"*40)
    print("ищем шаблоны в тексте")
    v = root
    for i, char in enumerate(text):
        old = v.id
        v = v.go[num(char)]
        print(f"[{i+1}] символ '{char}': узел {old} -> узел {v.id}")

        # по терминальным узлам через сжатые ссылки
        temp = v
        while temp != root:
            if temp.pattern_ids:
                for p_id in temp.pattern_ids:
                    results.append((i - len(patterns[p_id-1]) + 2, p_id))
                    print(f"найдено совпадение шаблона '{patterns[p_id-1]}' (id={p_id}) в позиции {i - len(patterns[p_id-1]) + 2}")
            temp = temp.dict_link

    results.sort()
    for pos, p_id in results:
        print(pos, p_id)
