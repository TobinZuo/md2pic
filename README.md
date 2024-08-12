# Markdown to Image

This is a Python script that converts markdown text into images. The script is capable of automatically adjusting the image size, paginating the content, and allowing customization for line height, margins, and more.

## Features

- Converts markdown text to images
- Automatically adjusts image size
- Supports pagination
- Customizable line height
- Customizable margins

## Installation

1. Clone the repository:

```bash
git clone git@github.com:TobinZuo/md2pic.git
cd md2pic
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To use the script, simply run main.py file. You can modify parameters in main.py:

```python
if __name__ == "__main__":
    file_path = "markdown.md"
    markdown_text = read_markdown_file(file_path)
    output_folder = "output"
    output_prefix = ""
    width = 1080  # Adjust width as needed
    height = 1350  # Adjust height as needed
    font_size = 30  # Adjust font size as needed
    line_height = 2
```

## Customization

The script allows for several customizations to tailor the output to your needs:

- **Line Height**: Adjust the line height to control the space between lines of text.
- **Margins**: Set the margin size to control the whitespace around the text.
- **Page Width**: Set the width of the page/image.

For more advanced usage, you can modify the script parameters or extend functionality by diving into the codebase.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
