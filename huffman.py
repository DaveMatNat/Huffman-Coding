import heapq
import sys
from itertools import count

class Node:
    def __init__(self, symbol=None, freq=0, left_child=None, right_child=None):
        self.symbol = symbol
        self.freq = freq
        self.left_child = left_child
        self.right_child = right_child

class MinHeap:
    def __init__(self):
        self.minheap = []
        self._counter = count()

    def push(self, node:Node):
        heapq.heappush(self.minheap,(node.freq, next(self._counter), node))

    def pop(self) -> Node:
        if not self.is_empty():
            popped = heapq.heappop(self.minheap)[2]
            return popped
        else:
            # raise IndexError("Cannot pop from empty heap")
            # Return dummy node
            return Node(None,0)
    
    def peak(self) -> list:
        if not self.minheap.is_empty():
            return self.minheap[0]
        else:
            raise IndexError("Cannot pop from empty heap")

    def is_empty(self):
        return len(self.minheap) == 0
    
    def size(self):
        return len(self.minheap)

class HuffmanCoding:
    def __init__(self, data):
        self.output_length = 1000
        self.original_data = data
        self.frequency = {}
        total = len(data)
        if total:
            bar_width = 30
            for i, sym in enumerate(data, start=1):
                self.frequency[sym] = self.frequency.get(sym, 0) + 1
                if i == total or i % 1000 == 0:
                    filled = int(bar_width * i / total)
                    bar = "#" * filled + "-" * (bar_width - filled)
                    percent = (i / total) * 100
                    sys.stdout.write(f"\rCounting symbols: [{bar}] {percent:6.2f}%")
                    sys.stdout.flush()
            sys.stdout.write("\n")
        self.minheap = MinHeap()
        unique_total = len(self.frequency)
        if unique_total:
            bar_width = 30
            for i, (sym, freq) in enumerate(self.frequency.items(), start=1):
                self.minheap.push(Node(sym, freq))
                if i == unique_total or i % 200 == 0:
                    filled = int(bar_width * i / unique_total)
                    bar = "#" * filled + "-" * (bar_width - filled)
                    percent = (i / unique_total) * 100
                    sys.stdout.write(f"\rBuilding heap:   [{bar}] {percent:6.2f}%")
                    sys.stdout.flush()
            sys.stdout.write("\n")

        self.huffman_tree = self.build_huffman_tree()
        self.encodings = self.generate_encoding()
        self.new_data = self.compress_data()
    
    def build_huffman_tree(self) -> Node:
        total_merges = self.minheap.size() - 1
        merges_done = 0
        bar_width = 30
        while self.minheap.size() > 1:
            first_least_sym = self.minheap.pop()
            second_least_sym = self.minheap.pop()
            new_node = Node("", first_least_sym.freq + second_least_sym.freq, first_least_sym, second_least_sym)
            self.minheap.push(new_node)
            merges_done += 1
            if merges_done == total_merges or merges_done % 200 == 0:
                filled = int(bar_width * merges_done / max(total_merges, 1))
                bar = "#" * filled + "-" * (bar_width - filled)
                percent = (merges_done / max(total_merges, 1)) * 100
                sys.stdout.write(f"\rBuilding tree:  [{bar}] {percent:6.2f}%")
                sys.stdout.flush()
        if total_merges > 0:
            sys.stdout.write("\n")
        return self.minheap.pop()
    
    def compress_data(self) -> str: # requires huffman tree and syms
        new_data = ""
        total = len(self.original_data)
        if total == 0:
            return ""

        bar_width = 30
        for i, sym in enumerate(self.original_data, start=1):
            new_data += self.encodings[sym]
            if i == total or i % 500 == 0:
                filled = int(bar_width * i / total)
                bar = "#" * filled + "-" * (bar_width - filled)
                percent = (i / total) * 100
                sys.stdout.write(f"\rCompressing: [{bar}] {percent:6.2f}%")
                sys.stdout.flush()

        sys.stdout.write("\n")
        return new_data

    def generate_encoding(self) -> dict:
        root = self.huffman_tree
        encodings = dict()

        # Edge case: only one unique symbol
        if root.left_child is None and root.right_child is None:
            encodings[root.symbol] = "0"
            return encodings

        # Traverse Tree in Pre-Order
        def preOrder(node: Node, res=''):
        # Base cases
            # if current Node is None
            if node is None:
                return 
            
            # if current Node is a leaf
            if node.left_child is None and node.right_child is None:
                encodings[node.symbol] = res
                return
            
        # Go left
            preOrder(node.left_child, res + '0')

        # Go right
            preOrder(node.right_child, res + '1')
        
        preOrder(root)
        return encodings
    
    def generate_decode(self) -> str:
        root = self.huffman_tree
        output = ""
        curr_node = root

        # Edge case: only one unique symbol
        if root.left_child is None and root.right_child is None:
            # each bit corresponds to that symbol (with the "0" convention above)
            return root.symbol * len(self.new_data)

        for b in self.new_data:
            if b == '0':
                curr_node = curr_node.left_child
            elif b == '1':
                curr_node = curr_node.right_child
            if not curr_node.left_child and not curr_node.right_child:
                output += curr_node.symbol
                curr_node = root

        return output
    
    def print_symbol_frequency(self, decreasing_order=True) -> None:
        sorted_freq = sorted(huffman_coding.frequency.items(), key=lambda item: item[1], reverse=decreasing_order)
        print(f"Unique Chars: {len(sorted_freq)}\n")
        for sym, freq in sorted_freq:
            if sym != "\n":
                print(f"{freq} : \'{sym}\'")
            else:
                print(f"{freq} : \'newline\'")

    def __str__(self):
        length = self.output_length
        old_bits = len(self.original_data) * 8
        new_bits = len(self.new_data)

        compression_ratio = new_bits / old_bits if old_bits else 0
        space_saving = 1 - compression_ratio
        print(f"Original data: ({old_bits:,} binary digits)\n{self.original_data[:length]}{'...' if len(self.original_data) >= length else ''}\n")
        print("----------------------------------------------")
        print(f"Compressed data: ({new_bits:,} binary digits)\n{self.new_data[:length]}{'...' if len(self.new_data) >= length else ''}\n")
        print("----------------------------------------------")
        print(f"Compressed data decoded:\n{huffman_coding.generate_decode()[:length]}{'...' if len(self.new_data) >= length else ''}\n")
        print("----------------------------------------------")
        print(f"Compression ratio: {compression_ratio:.4f}")
        print(f"Space saved: {space_saving*100:.2f}%")
        return ""
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        file_path = str(path)
    else:
        file_path = 'data.txt'

    data = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        print("File successfully read:\n")
    except FileNotFoundError:
        print(f"Error: The file 'your_file.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    huffman_coding = HuffmanCoding(data)

    print(huffman_coding)

    # huffman_coding.print_symbol_frequency()

    # print(huffman_coding.generate_decode() == huffman_coding.original_data)