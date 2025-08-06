# individual_compressors.py

from rle import rle_encode
from huffman import huffman_encode
from combined_compressor import flatten_rle_pairs
import numpy as np

def get_rle_only_size(image_array: np.ndarray) -> int:
    """
    Calculates an estimated bit size after applying only RLE.

    The size is an estimation because we assume each number (both pixel value
    and run count) in the RLE output takes 16 bits (2 bytes) to store.
    """
    flat_data = image_array.flatten()
    rle_pairs = rle_encode(flat_data)
    rle_flat = flatten_rle_pairs(rle_pairs)
    
    # Estimate size: assume each number in the flattened list takes 16 bits.
    return len(rle_flat) * 16

def get_huffman_only_size(image_array: np.ndarray) -> int:
    """
    Calculates the exact bit size after applying only Huffman encoding
    to the raw pixel data.
    """
    flat_data = list(image_array.flatten())
    encoded_data, _, _ = huffman_encode(flat_data)
    
    # The length of the encoded bit string is the size in bits.
    return len(encoded_data)