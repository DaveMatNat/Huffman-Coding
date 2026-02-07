# from collections import defaultdict
import heapq
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
        self.original_data = data
        self.frequency = { sym: data.count(sym) for sym in data }
        self.minheap = MinHeap()
        for sym, freq in self.frequency.items():
            self.minheap.push(Node(sym, freq))

        self.huffman_tree = self.build_huffman_tree()
        self.encodings = self.generate_encoding()
        self.new_data = self.compress_data()
    
    def build_huffman_tree(self) -> Node:
        while self.minheap.size() > 1:
            first_least_sym = self.minheap.pop()
            second_least_sym = self.minheap.pop()
            new_node = Node("", first_least_sym.freq + second_least_sym.freq, first_least_sym, second_least_sym)
            self.minheap.push(new_node)
        return self.minheap.pop()
    
    def compress_data(self) -> str: # requires huffman tree and syms
        new_data = ""

        for sym in self.original_data:
            new_data += self.encodings[sym]
        
        return new_data

    def generate_encoding(self) -> dict:
        # Traverse Tree in Pre-Order
        root = self.huffman_tree
        encodings = dict()
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

        for b in self.new_data:
            if b == '0':
                curr_node = curr_node.left_child
            elif b == '1':
                curr_node = curr_node.right_child
            if not curr_node.left_child and not curr_node.right_child:
                output += curr_node.symbol
                curr_node = root
                
        return output

    def __str__(self):
        old_bits = len(self.original_data) * 8
        new_bits = len(self.new_data)

        compression_ratio = new_bits / old_bits if old_bits else 0
        space_saving = 1 - compression_ratio

        print(f"Old Data: ({old_bits} bits)\n\t{self.original_data}\n")
        print(f"New Data: ({new_bits} bits)\n\t{self.new_data}\n")
        print(f"Compression ratio: {compression_ratio:.4f}")
        print(f"Space saved: {space_saving*100:.2f}%")
        return ""
if __name__ == '__main__':
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

    # for sym, freq in huffman_coding.frequency.items():
    #     print(f"{freq} : {sym}")


    print(huffman_coding.generate_decode())