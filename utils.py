# utils.py
from PIL import Image
import numpy as np

def load_image_grayscale(path):
    """
    Loads an image from the specified path and converts it to grayscale.
    
    Args:
        path (str): The file path to the image.
        
    Returns:
        np.ndarray: A NumPy array representing the grayscale image.
    """
    img = Image.open(path).convert("L")
    return np.array(img)

def save_image_grayscale(data, path, format=None):
    """
    Saves a NumPy array as a grayscale image to the specified path.
    
    Args:
        data (np.ndarray): The NumPy array containing the image data.
        path (str or file-like object): The destination file path or buffer.
        format (str, optional): The image format to use (e.g., 'PNG'). 
                                This is essential for saving to in-memory 
                                buffers. Defaults to None, which lets PIL
                                infer from the filename.
    """
    # Ensure the data is in the correct type for image saving
    img = Image.fromarray(data.astype(np.uint8))
    
    # The 'format' argument allows saving to a buffer without a filename extension
    img.save(path, format=format)