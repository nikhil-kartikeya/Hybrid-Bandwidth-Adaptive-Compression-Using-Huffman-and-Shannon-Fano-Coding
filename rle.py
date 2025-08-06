# rle.py

def rle_encode(data):
    if len(data) == 0:
        return []

    encoded = []
    prev = data[0]
    count = 1

    for i in range(1, len(data)):
        if data[i] == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev = data[i]
            count = 1

    encoded.append((prev, count))
    return encoded

def rle_decode(data):
    decoded = []
    for value, count in data:
        decoded.extend([value] * count)
    return decoded
