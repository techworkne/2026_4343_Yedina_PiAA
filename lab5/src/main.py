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
    nodes = []
    root = Vertex(id=0, road_char="root")
    counter = 1

    for idx, p in enumerate(patterns, start=1):
        v = root
        for i in p:
            c = num(i)

            if v.next[c] is None:
                v.next[c] = Vertex(id=counter, road_char=i)
                nodes.append(v.next[c])
                counter += 1

            v = v.next[c]
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


def chain(all, root):
    max_suff = 0
    max_dict = 0

    for v in all:
        # суффиксная цепочка
        curr_suff = 0
        temp = v
        while temp != root:
            curr_suff += 1
            temp = temp.sufflink
        max_suff = max(max_suff, curr_suff)

        # цепочка конечных ссылок
        curr_dict = 0
        temp = v
        while temp != root and temp.dict_link != root:
            curr_dict += 1
            temp = temp.dict_link
        max_dict = max(max_dict, curr_dict)

    return max_suff, max_dict


def print_debug_info(all_nodes):
    print()
    for v in all_nodes:
        s = v.sufflink.id if v.sufflink else 0
        d = v.dict_link.id if v.dict_link else 0
        term = f" (шаблоны: {v.pattern_ids})" if v.pattern_ids else ""
        print(f"узел {v.id} ['{v.road_char}']: суффисная ссылка на узел -> {s}, сжатая ссылка на узел -> {d}{term}")
    print()

if __name__ == "__main__":
    # text = input().strip()
    # n = int(input())

    # patterns = []
    # for _ in range(n):
    #     patterns.append(input().strip())
    text = "NTAG"
    patterns = ["NT", "NG"]


    results = []
    root, nodes = build(patterns)

    print(f"текст: {text}")
    print(f"список паттернов: {patterns}\n")

    print("-"*40)
    print("бор:")
    print_debug_info(nodes)

    max_suff, max_dict = chain(nodes, root)
    print(f"максимальная длина цепочки суффиксных ссылок: {max_suff}")
    print(f"максимальная длина цепочки сжатых ссылок: {max_dict}")

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
