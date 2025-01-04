# Inertia Analysis Binding Python

This project provides Python bindings for a C library that calculates moments of inertia for polygons. The bindings are provided using both `ctypes` and `cffi`.

## Project Structure

- `native/`: Contains the C library source files (`library.c` and `library.h`).
- `inertia-analysis-binding-python/`: Contains the Python scripts for testing the bindings (`ctypes_test.py` and `cffi_test.py`).
- `.github/workflows/`: Contains the GitHub Actions workflow for building and testing the project.
- `tasks.py`: Contains `invoke` tasks for building and testing the project.

## Prerequisites

- Python 3.8 or higher
- GCC (for compiling the C library)
- `invoke` (for task management)
- `cffi` (for CFFI bindings)

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/inertia-analysis-binding-python.git
    cd inertia-analysis-binding-python
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required Python packages:

    ```sh
    pip install --upgrade pip
    pip install invoke cffi
    ```

## Building the C Library

You can build the C library using `invoke`:

### ctypes

```sh
invoke build-library
python ctypes_test.py
```

### cffi

```sh
invoke build-cffi
python cffi_test.py
```

