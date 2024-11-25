# Time2Crack

**Time2Crack** is a Python-based tool that estimates the time required to brute-force a password based on its character set, length, and hash type. It leverages `hashcat` to perform benchmarks and determine device-specific hash rates.

## Features
- User-friendly interactive prompts to specify:
  - Character set (letters, numbers, special characters, or custom sets)
  - Password length
  - Hash type (e.g., MD5, SHA1, SHA256, NTLM, bcrypt)
- Automatically detects and allows selection of compute devices (CPU/GPU) for benchmarking.
- Calculates and displays:
  - Total possible combinations for a given password configuration.
  - Estimated time to crack the password based on benchmark results.
- Supports both Windows and Linux platforms.

---

## Prerequisites

Before running **Time2Crack**, ensure the following are installed:

### Python
- **Python 3.7 or later**: [Download Python](https://www.python.org/downloads/)

### Hashcat
- Install the latest version of `hashcat`:
  - [Download Hashcat](https://hashcat.net/hashcat/)

### OpenCL
- Ensure OpenCL runtime libraries are installed for your hardware:
  - **NVIDIA GPUs:** Install the [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit).
  - **AMD GPUs:** Install the [AMD Radeon Software](https://www.amd.com/en/support).
  - **CPUs:** Install appropriate OpenCL runtime for your processor.

---

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-repo/Time2Crack.git
   cd Time2Crack
