# SortDemo

SortDemo is a graphical visualization tool for sorting algorithms, built with Python, GTK 4, and Libadwaita. It is designed to help understand how different sorting algorithms work by visualizing their operations in real-time.

## Features

- **Visual Sorting**: Watch sorting algorithms process data step-by-step.
- **Multiple Algorithms**: Includes Bubble Sort, Insertion Sort, Quick Sort, and Merge Sort.
- **Interactive Controls**:
  - Start, Pause, and Reset sorting.
  - Adjust sorting speed dynamically.
  - Change the dataset size (from 10 to 1000 elements).
- **Modern UI**: Built with Libadwaita for a native GNOME look and feel.

## Prerequisites

- **Python**: 3.13 or later
- **GTK 4** and **Libadwaita**
- **uv** (Recommended for dependency management)

### System Dependencies

You need to install system-level development headers for PyGObject to build.

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install -y \
    build-essential \
    pkg-config \
    python3-dev \
    libgirepository-2.0-dev \
    libcairo2-dev \
    libgtk-4-dev \
    libadwaita-1-dev
```
*(Note: On older Ubuntu versions, use `libgirepository1.0-dev` instead of `libgirepository-2.0-dev`)*

**Fedora:**
```bash
sudo dnf install -y \
    python3-devel \
    gobject-introspection-devel \
    cairo-gobject-devel \
    gtk4-devel \
    libadwaita-devel \
    gcc
```

## Installation & Running

This project uses `uv` for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/sortdemo.git
    cd sortdemo
    ```

2.  **Sync dependencies:**
    ```bash
    uv sync
    ```

3.  **Run the application:**
    ```bash
    uv run sortdemo
    ```

## Usage

1.  Select a sorting algorithm from the dropdown menu in the header.
2.  Use the **Size** slider to set the number of elements.
3.  Click **Start** to begin the visualization.
4.  Use the **Speed** slider to adjust the animation speed in real-time.
5.  Click **Pause** to stop temporarily, or **Reset** to generate a new random dataset.

## Implemented Algorithms

- **Bubble Sort**: A simple comparison-based algorithm.
- **Insertion Sort**: Builds the final sorted array one item at a time.
- **Quick Sort**: A divide-and-conquer algorithm (visualized recursively).
- **Merge Sort**: Another efficient divide-and-conquer algorithm.

## Project Structure

```
sortdemo/
├── src/
│   └── sortdemo/
│       ├── main.py       # Entry point
│       ├── window.py     # Main window and UI logic
│       ├── canvas.py     # Drawing area (Gtk.DrawingArea)
│       └── algorithms/   # Sorting algorithm implementations
├── pyproject.toml        # Project metadata and dependencies
└── README.md
```

## License

This project is open source.
