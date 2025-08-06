# bit_packer.py

def pack_bits(encoded_string: str) -> bytes:
    """
    Packs a string of '0's and '1's into a compact byte representation.

    The first byte of the output is a header that stores the number of padding
    bits added to the end of the bit string to make its length a multiple of 8.
    """
    # Calculate how many bits of padding are needed.
    padding_needed = 8 - (len(encoded_string) % 8)
    if padding_needed == 8:
        padding_needed = 0  # No padding needed if it's already a multiple of 8.

    # Add the padding bits (as '0's) to the end of the string.
    padded_string = encoded_string + '0' * padding_needed

    # The header is a single byte representing the number of padding bits.
    header = bytes([padding_needed])

    # Convert every 8 bits (a string of 8 characters) into an integer, then a byte.
    byte_array = bytearray()
    for i in range(0, len(padded_string), 8):
        byte = int(padded_string[i:i+8], 2)
        byte_array.append(byte)

    # Return the header byte followed by the data bytes.
    return header + bytes(byte_array)

def unpack_bits(packed_data: bytes) -> str:
    """
    Unpacks bytes back into the original string of '0's and '1's.

    It reads the header byte first to know how many padding bits to remove
    from the end of the resulting bit string.
    """
    # The first byte is the header, which tells us the number of padding bits.
    padding_needed = packed_data[0]
    data_bytes = packed_data[1:]

    # Convert each byte back to an 8-bit binary string (e.g., 5 -> "00000101").
    # The 'zfill(8)' is crucial to ensure each byte becomes 8 bits.
    bit_string = ''.join(bin(byte)[2:].zfill(8) for byte in data_bytes)

    # If padding was added, remove it from the end.
    if padding_needed > 0:
        return bit_string[:-padding_needed]
    
    return bit_string