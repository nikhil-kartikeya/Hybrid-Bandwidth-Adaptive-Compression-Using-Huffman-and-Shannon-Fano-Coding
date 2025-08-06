# huffman.py
from collections import Counter
import heapq

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        # The symbol (e.g., a pixel value)
        self.symbol = symbol
        # The frequency of the symbol
        self.freq = freq
        # Left child node
        self.left = left
        # Right child node
        self.right = right

    # This makes the nodes comparable for the priority queue (heap)
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    """Builds a Huffman tree from the input data."""
    # Count frequency of each symbol in the data
    frequency = Counter(data)
    # Create a leaf node for each symbol and add it to a priority queue
    heap = [Node(freq, sym) for sym, freq in frequency.items()]
    heapq.heapify(heap)

    # Merge nodes until only one root node remains
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        # Create a new internal node with combined frequency
        merged = Node(left.freq + right.freq, None, left, right)
        heapq.heappush(heap, merged)

    # The remaining node is the root of the tree
    return heap[0]

def _generate_codes_recursive(node, current_code, codes):
    """A helper function to recursively generate codes from the tree."""
    if node is None:
        return
    # If it's a leaf node, we have found a code for a symbol
    if node.symbol is not None:
        codes[node.symbol] = current_code
        return

    # Traverse left (append '0') and right (append '1')
    _generate_codes_recursive(node.left, current_code + "0", codes)
    _generate_codes_recursive(node.right, current_code + "1", codes)

def build_codes(root_node):
    """Builds a codebook (dict) from a Huffman tree."""
    codes = {}
    _generate_codes_recursive(root_node, "", codes)
    return codes

def huffman_encode(data):
    """Encodes data using the Huffman algorithm."""
    if not data:
        return "", {}, None
    root = build_huffman_tree(data)
    codes = build_codes(root)
    encoded_data = ''.join(codes[symbol] for symbol in data)
    return encoded_data, codes, root

def huffman_decode(encoded_data, root):
    """Decodes Huffman-encoded data using the tree."""
    decoded = []
    # If the tree is empty or just a leaf, handle edge cases
    if root is None:
        return []
    if root.left is None and root.right is None:
        # This handles data with only one unique symbol
        return [root.symbol] * len(encoded_data)
        
    node = root
    for bit in encoded_data:
        # Move down the tree based on the bit
        node = node.left if bit == '0' else node.right

        # If we reach a leaf node, we have found a symbol
        if node.symbol is not None:
            decoded.append(node.symbol)
            node = root # Reset to the root for the next symbol
    return decoded

# --- NEW FUNCTIONS ADDED FOR FILE I/O ---

def serialize_tree(node):
    """
    Recursively serialize a Huffman tree to a tuple structure for saving.
    ('L', symbol) for a leaf node.
    ('I', left_subtree, right_subtree) for an internal node.
    """
    if node.symbol is not None:
        return ('L', node.symbol)
    else:
        # Recursively serialize the left and right children
        left_serialized = serialize_tree(node.left)
        right_serialized = serialize_tree(node.right)
        return ('I', left_serialized, right_serialized)

def deserialize_tree(data: tuple):
    """
    Recursively deserialize a tuple structure back into a Huffman tree.
    """
    node_type = data[0]
    if node_type == 'L':
        # It's a leaf node. Freq is not needed for decoding, so 0 is a placeholder.
        return Node(0, data[1])
    elif node_type == 'I':
        # It's an internal node. Recursively deserialize its children.
        left = deserialize_tree(data[1])
        right = deserialize_tree(data[2])
        return Node(0, None, left, right)