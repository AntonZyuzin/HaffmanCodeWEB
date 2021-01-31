import cgi
import heapq
from collections import Counter
from collections import namedtuple


class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")


class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"


def huffman_encode(s):
    h = []
    for ch, freq in Counter(s).items():
        h.append((freq, len(h), Leaf(ch)))
    heapq.heapify(h)
    count = len(h)
    while len(h) > 1:
        freq1, _count1, left = heapq.heappop(h)
        freq2, _count2, right = heapq.heappop(h)
        heapq.heappush(h, (freq1 + freq2, count, Node(left, right)))
        count += 1
    code = {}
    if h:
        [(_freq, _count, root)] = h
        root.walk(code, "")
    return code


def main(s):
    code = huffman_encode(s)
    encoded = "".join(code[ch] for ch in s)
    result = []
    for ch in sorted(code):
        result.append("{}: {}".format(ch, code[ch]))
    return (encoded, " | ".join(result))


if __name__ == "__main__":
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
            <html>
            <head>
                <title>Кодировка</title>
                <style>
   body {
    background: #000000;
    color: #fff; 
   }
    </style>

            </head>
            <body>""")

    form = cgi.FieldStorage()
    text1 = form.getfirst("TEXT_1", False)

    if text1:
        print("<h1>Результат кодирования</h1>")
        text1, text2 = main(text1)
        print("<p>Закодированная строка | {}</p>".format(text1))
        print("<p>Закодированные символы | {}</p>".format(text2))

    else:
        print("<h1>Данные не заданы!</h1>")

    print("""</body>
            </html>""")
