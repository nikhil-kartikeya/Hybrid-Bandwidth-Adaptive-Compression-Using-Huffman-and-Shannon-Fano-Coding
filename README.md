# Hybrid-Bandwidth-Adaptive-Compression-Using-Huffman-and-Shannon-Fano-Coding
A hybrid compression pipeline combines bandwidth estimation (IBW, SEF), adaptive quantization, and entropy coding (Huffman and Shannon–Fano) to efficiently compress signals. It ensures maximum data reduction while maintaining signal fidelity, supporting scalable and low-power transmission for healthcare and IoT applications.

Project Overview

This project implements a hybrid compression pipeline that leverages bandwidth estimation techniques (Instantaneous Bandwidth - IBW, Spectral Edge Frequency - SEF), adaptive quantization, and entropy coding (Huffman and Shannon–Fano) to efficiently compress biomedical signals. The goal is to maximize compression ratio while preserving critical signal fidelity, making it suitable for scalable healthcare and IoT applications.
Features

    Bandwidth estimation via spectrogram and Welch's methods

    Adaptive quantization guided by bandwidth metrics

    Lossless compression using Huffman and Shannon–Fano algorithms

    Performance metrics including Compression Ratio (CR) and Percentage Root Mean Square Difference (PRD)

    Visualization of bandwidth analysis and signal quality

    Modular, extensible Python codebase for easy adaptation

Folder Structure

text
/ ── README.md
   ── data/              # Sample input signals (e.g., ECG .wav files)
   ── src/               # Source code files (bandwidth estimation, quantization, compression)
   ── plots/             # Generated plots and visualization outputs
   ── results/           # Compression and analysis results (tables, metrics)
   ── requirements.txt   # Python dependencies

Getting Started
Prerequisites

    Python 3.7 or higher

    Recommended: virtual environment to isolate dependencies

Installation

    Clone the repository:

bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

Create and activate a virtual environment (optional but recommended):

bash
python -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate

Install dependencies:

    bash
    pip install -r requirements.txt

Usage

    Prepare your signal data: Place your input .wav or compatible signal files in the data/ directory.

    Run bandwidth estimation:

bash
python src/bandwidth_estimation.py --input data/sample.wav

Apply adaptive quantization (optional):

bash
python src/quantization.py --input data/sample.wav --bandwidth_metrics results/ibw_sef.json

Compress using Huffman or Shannon–Fano:

    Huffman:

bash
python src/huffman_compression.py --input data/sample_quantized.wav

Shannon–Fano:

    bash
    python src/shannon_fano_compression.py --input data/sample_quantized.wav

Decompress and analyze:

bash
python src/decompression_analysis.py --compressed results/sample_compressed.bin

Visualize results (plots, waveforms, compression metrics):

    bash
    python src/plot_results.py --results_dir results/

Metrics & Validation

    Compression Ratio (CR): Ratio of original to compressed data size.

    Percentage Root Mean Square Difference (PRD): Quantifies signal distortion after compression/decompression.

    Bandwidth metrics (IBW, SEF) guide quantizer settings to optimize compression.
