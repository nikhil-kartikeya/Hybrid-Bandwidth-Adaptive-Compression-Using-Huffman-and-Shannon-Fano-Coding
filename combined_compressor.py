import numpy as np
from rle import rle_encode, rle_decode
from huffman import huffman_encode, huffman_decode

def flatten_rle_pairs(rle_pairs):
    """Convert RLE pairs into a flat list: [val1, count1, val2, count2, ...]"""
    flat = []
    for val, count in rle_pairs:
        flat.append(val)
        flat.append(count)
    return flat

def unflatten_rle_pairs(flat_list):
    """Convert flat list back to RLE format"""
    return [(flat_list[i], flat_list[i+1]) for i in range(0, len(flat_list), 2)]

def compress_combined(image_array):
    flat_data = image_array.flatten()

    # Step 1: RLE
    rle_pairs = rle_encode(flat_data)

    # Step 2: Flatten RLE for Huffman
    rle_flat = flatten_rle_pairs(rle_pairs)

    # Step 3: Huffman encode flattened RLE
    huffman_encoded, huffman_codes, huffman_tree = huffman_encode(rle_flat)

    return huffman_encoded, huffman_tree, image_array.shape

def decompress_combined(encoded_data, huffman_tree, original_shape):
    # Step 1: Huffman decode
    decoded_flat = huffman_decode(encoded_data, huffman_tree)

    # Step 2: Reconstruct RLE pairs
    rle_pairs = unflatten_rle_pairs(decoded_flat)

    # Step 3: Apply RLE decode
    decompressed_flat = rle_decode(rle_pairs)

    # Step 4: Reshape
    decompressed_image = np.array(decompressed_flat[:np.prod(original_shape)], dtype=np.uint8).reshape(original_shape)
    return decompressed_image
