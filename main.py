# main.py
import os
import numpy as np
import matplotlib.pyplot as plt
import io
import time
from PIL import Image
from utils import load_image_grayscale, save_image_grayscale
from combined_compressor import compress_combined, decompress_combined
from file_io import save_compressed_file, load_compressed_file

def process_image(image_path, show_plots=True):
    """
    Processes a single image: compresses, decompresses, verifies, profiles performance,
    and returns a dictionary of statistics.
    """
    print(f"\n📂 Processing: {os.path.basename(image_path)}")
    img_array = load_image_grayscale(image_path)
    flat_data = img_array.flatten()
    original_size_bytes = flat_data.nbytes

    # --- 1. OUR RLE+HUFFMAN COMPRESSION & TIMING ---
    print("⏱️  Profiling RLE+Huffman Compression...")
    start_time = time.perf_counter()
    encoded_data, tree, shape = compress_combined(img_array)
    end_time = time.perf_counter()
    rlehuff_compress_time_ms = (end_time - start_time) * 1000

    # Save to custom file to get final size
    os.makedirs("compressed_output", exist_ok=True)
    compressed_path = f"compressed_output/{os.path.basename(image_path)}.rlehuff"
    save_compressed_file(compressed_path, encoded_data, tree, shape)
    compressed_size_bytes = os.path.getsize(compressed_path)

    # --- 2. OUR RLE+HUFFMAN DECOMPRESSION & TIMING ---
    print("⏱️  Profiling RLE+Huffman Decompression...")
    start_time = time.perf_counter()
    loaded_encoded, loaded_tree, loaded_shape = load_compressed_file(compressed_path)
    decompressed = decompress_combined(loaded_encoded, loaded_tree, loaded_shape)
    end_time = time.perf_counter()
    rlehuff_decompress_time_ms = (end_time - start_time) * 1000
    
    # --- 3. STANDARD FORMATS COMPRESSION & TIMING ---
    # PNG (Lossless)
    print("⏱️  Profiling PNG Compression...")
    png_buffer = io.BytesIO()
    start_time = time.perf_counter()
    save_image_grayscale(img_array, png_buffer, format='PNG')
    end_time = time.perf_counter()
    png_compress_time_ms = (end_time - start_time) * 1000
    png_size_bytes = png_buffer.tell()

    # JPEG (Lossy)
    print("⏱️  Profiling JPEG Compression...")
    jpeg_buffer = io.BytesIO()
    start_time = time.perf_counter()
    save_image_grayscale(img_array, jpeg_buffer, format='JPEG')
    end_time = time.perf_counter()
    jpeg_compress_time_ms = (end_time - start_time) * 1000
    jpeg_size_bytes = jpeg_buffer.tell()

    # --- 4. STANDARD FORMATS DECOMPRESSION & TIMING ---
    print("⏱️  Profiling PNG Decompression...")
    png_buffer.seek(0) # Rewind buffer to the beginning
    start_time = time.perf_counter()
    _ = Image.open(png_buffer) # The actual decompression happens here
    end_time = time.perf_counter()
    png_decompress_time_ms = (end_time - start_time) * 1000

    # --- VERIFICATION & SAVING THE RECONSTRUCTED IMAGE ---
    total_diff = np.sum(np.abs(img_array.astype(np.int16) - decompressed.astype(np.int16)))
    print("\n--- Verification ---")
    print(f"✅ Lossless Verification Passed: {total_diff == 0}")

    # This block ensures the final, viewable image is saved.
    os.makedirs("reconstructed", exist_ok=True)
    reconstructed_path = f"reconstructed/hybrid_{os.path.basename(image_path)}"
    save_image_grayscale(decompressed, reconstructed_path)
    print(f"🖼️  Reconstructed image saved to: {reconstructed_path}")

    # --- ANALYSIS & STATS ---
    original_kb = original_size_bytes / 1024
    compressed_kb = compressed_size_bytes / 1024
    png_kb = png_size_bytes / 1024
    jpeg_kb = jpeg_size_bytes / 1024
    ratio = original_kb / compressed_kb if compressed_kb > 0 else 0

    print("\n--- Size Statistics ---")
    print(f"📏 Original size:       {original_kb:.2f} KB")
    print(f"📉 Our RLE+Huffman:     {compressed_kb:.2f} KB (Ratio: {ratio:.2f}:1)")
    print(f"🔹 Standard PNG:        {png_kb:.2f} KB")
    print(f"🔸 Standard JPEG (Lossy): {jpeg_kb:.2f} KB")

    print("\n--- Performance Statistics (ms) ---")
    print(f"{'Format':<18} | {'Compress Time':>15} | {'Decompress Time':>15}")
    print("-" * 54)
    print(f"{'Our RLE+Huffman':<18} | {rlehuff_compress_time_ms:15.2f} | {rlehuff_decompress_time_ms:15.2f}")
    print(f"{'Standard PNG':<18} | {png_compress_time_ms:15.2f} | {png_decompress_time_ms:15.2f}")
    print(f"{'Standard JPEG':<18} | {jpeg_compress_time_ms:15.2f} | {'N/A (different lib)':>15}")

    stats = {
        'filename': os.path.basename(image_path),
        'original_kb': original_kb,
        'compressed_kb': compressed_kb,
        'ratio': ratio,
        'compress_time': rlehuff_compress_time_ms,
        'decompress_time': rlehuff_decompress_time_ms,
    }

    if show_plots:
        # Plot 1: Size Comparison
        plt.figure(figsize=(10, 6))
        labels = ["Original", "Our RLE+Huffman", "Standard PNG", "JPEG (Lossy)"]
        sizes = [original_kb, compressed_kb, png_kb, jpeg_kb]
        colors = ["#3498db", "#f39c12", "#2ecc71", "#e74c3c"]
        bars = plt.bar(labels, sizes, color=colors)
        plt.ylabel("Size (KB)")
        plt.title(f"Size Comparison: {os.path.basename(image_path)}")
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f}', va='bottom', ha='center')
        plt.tight_layout()
        plt.show()

        # Plot 2: Performance Comparison
        plt.figure(figsize=(12, 6))
        
        # Subplot for Compression Speed
        plt.subplot(1, 2, 1)
        perf_labels = ['Our RLE+Huffman', 'Standard PNG', 'JPEG (Lossy)']
        compress_times = [rlehuff_compress_time_ms, png_compress_time_ms, jpeg_compress_time_ms]
        plt.bar(perf_labels, compress_times, color=['#f39c12', '#2ecc71', '#e74c3c'])
        plt.ylabel("Time (milliseconds)")
        plt.title("Compression Speed")
        plt.xticks(rotation=15, ha="right")

        # Subplot for Decompression Speed
        plt.subplot(1, 2, 2)
        decompress_labels = ['Our RLE+Huffman', 'Standard PNG']
        decompress_times = [rlehuff_decompress_time_ms, png_decompress_time_ms]
        plt.bar(decompress_labels, decompress_times, color=['#f39c12', '#2ecc71'])
        plt.ylabel("Time (milliseconds)")
        plt.title("Decompression Speed")
        plt.xticks(rotation=15, ha="right")

        plt.suptitle(f"Performance Comparison: {os.path.basename(image_path)}")
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

    return stats

def main():
    image_dir = "images"
    os.makedirs(image_dir, exist_ok=True)
    imgs = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not imgs:
        print("❌ No images found in 'images/' folder. Please add some to test.")
        return

    while True:
        print("\n--- Image Compression Menu ---")
        for i, f in enumerate(imgs, 1):
            print(f"{i}. {f}")
        print("-" * 20)
        print(f"A. Process ALL images (Batch Mode)")
        print("Q. Quit")

        choice = input("Enter your choice: ").strip().lower()

        if choice == 'q':
            break
        elif choice == 'a':
            # Batch mode
            all_stats = []
            for img_file in imgs:
                img_path = os.path.join(image_dir, img_file)
                stats = process_image(img_path, show_plots=False)
                all_stats.append(stats)
            
            # Print summary table
            print("\n--- Batch Processing Summary ---")
            print(f"{'Filename':<25} | {'Size Ratio':>10} | {'Comp Time (ms)':>16} | {'Decomp Time (ms)':>17}")
            print("-" * 80)
            for s in all_stats:
                ratio_str = f"{s['ratio']:.2f}:1"
                print(f"{s['filename']:<25} | {ratio_str:>10} | {s['compress_time']:>16.2f} | {s['decompress_time']:>17.2f}")
            print("-" * 80)

        else:
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(imgs):
                    selected_path = os.path.join(image_dir, imgs[choice_idx])
                    process_image(selected_path, show_plots=True)
                else:
                    print("❌ Invalid number.")
            except ValueError:
                print("❌ Invalid choice. Please enter a number, 'A', or 'Q'.")

if __name__ == "__main__":
    main()

