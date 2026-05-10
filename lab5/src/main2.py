class Vertex:
    def __init__(self, alpha=5):
        self.next = [None] * alpha  # список переходов в боре
        self.go = [None] * alpha  # список переходов в автомате
        self.sufflink = None
        self.dict_link = None
        self.parts = []


def num(c):
    return "ACGTN".index(c)


def parser(p, joker):
    start = -1
    cur_sub = ""
    parts = []
    for i, char in enumerate(p):
        if char != joker:
            if start == -1:
                start = i
            cur_sub += char
        else:
            if cur_sub:
                parts.append((start, cur_sub))
                cur_sub = ""
                start = -1
    if cur_sub:
        parts.append((start, cur_sub))
    return parts


def build(parts):
    root = Vertex()

    for offset, sub in parts:
        v = root
        for char in sub:
            c = num(char)
            if v.next[c] is None:
                v.next[c] = Vertex()
            v = v.next[c]

        v.parts.append((offset, sub))

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
                if child.sufflink.parts:
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
    return root


text = input().strip()
p = input().strip()
joker = input().strip()

parts = parser(p, joker)

root = build(parts)
counts = [0] * (len(text)+1)


v = root
for i, char in enumerate(text):
    char_idx = num(char)
    if char_idx == -1:
        v = root
        continue

    v = v.go[num(char)]

    temp = v
    while temp != root:
        for offset in temp.parts:
            start_pos = i - len(offset[1]) + 1 - offset[0]
            if start_pos >= 0 and start_pos <= len(text) - len(p):
                counts[start_pos] += 1
        temp = temp.dict_link


num_parts = len(parts)
for i in range(len(text)):
    if counts[i] == num_parts:
        print(i + 1)
