import asyncio
import shutil

from html2image import Html2Image
from markdown import markdown
from pyppeteer import launch


async def get_content_height(page, html_content, width, font_size, line_height):
    custom_css = f"""
    <style>
        body {{
            width: {width}px;
            font-size: {font_size}px;
            line-height: {line_height};
            font-family: 'Noto Sans', sans-serif;
            padding: 20px;
            margin:0
        }}
    </style>
    """
    content = f"<!DOCTYPE html><html><head>{custom_css}</head><body>{html_content}</body></html>"
    await page.setContent(content)
    height = await page.evaluate('document.body.scrollHeight')
    return height


async def paginate_markdown(browser, markdown_text, width, height, font_size, line_height):
    html_content = markdown(markdown_text)
    page = await browser.newPage()
    await page.setViewport({"width": width, "height": height})

    elements = html_content.split('\n')
    chunks = []
    current_chunk = ""
    current_height = 0
    list_prefix = ""

    for element in elements:
        # 保留列表项的序号和前缀
        if element.strip().startswith('<li>') and list_prefix:
            element = list_prefix + element
        elif element.strip().startswith('<li>') and not list_prefix:
            list_prefix = element[:element.find('<li>')]

        temp_chunk = current_chunk + element + '\n'
        temp_height = await get_content_height(page, temp_chunk, width, font_size, line_height)

        if temp_height <= height:
            current_chunk = temp_chunk
            current_height = temp_height
        else:
            chunks.append(current_chunk)
            current_chunk = element + '\n'
            current_height = await get_content_height(page, current_chunk, width, font_size, line_height)

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def create_image(html_content, output_file_path, width=800, height=1000, font_size=16, line_height=1.5):
    custom_css = f"""
    <style>
        body {{
            width: {width}px;
            height: {height}px;
            font-size: {font_size}px;
            line-height: {line_height};
            font-family: 'Noto Sans', sans-serif;
            padding: 20px;
            background-color: white;
            margin: 20px;
            box-sizing: border-box; /* 确保右边界不出页面 */
            overflow-wrap: break-word; /* 在单词内断行 */
            white-space: normal; /* 确保文本在容器内断行 */
        }}
    </style>
    """
    html = f"<!DOCTYPE html><html><head>{custom_css}</head><body>{html_content}</body></html>"

    hti = Html2Image()

    print("当前目录", os.getcwd())
    hti.screenshot(html_str=html, save_as=output_file_path, size=(width, height))


async def create_images_from_markdown(markdown_text, output_folder, output_prefix, width=800, height=1000, font_size=16,
                                      line_height=1.5):
    browser = await launch(headless=True, args=["--no-sandbox"])
    chunks = await paginate_markdown(browser, markdown_text, width, height, font_size, line_height)

    original_cwd = os.getcwd()
    try:
        for i, chunk in enumerate(chunks):
            print(chunk)
            output_file_path = f"{i + 1}.png"
            if output_prefix != "":
                output_file_path = f"{output_prefix}_{i + 1}.png"
            create_image(chunk, output_file_path, width, height, font_size, line_height)
            if output_folder != "":
                # move到该文件夹
                final_path = os.path.join(output_folder, output_file_path)
                shutil.move(output_file_path, final_path)
                pass
            print(f"Image {i + 1} generated and saved to {output_file_path} successfully!")
    finally:
        os.chdir(original_cwd)

    await browser.close()


def read_markdown_file(file_path):
    """Reads a markdown file and returns its content as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return str(e)


import os
import glob


def delete_output_png_files(folder_path, pattern):
    """Deletes all files in the specified folder that match 'output_*.png'."""
    try:
        # 使用glob模块获取所有符合条件的文件路径列表
        file_pattern = os.path.join(folder_path, pattern)
        files_to_delete = glob.glob(file_pattern)

        # 遍历文件列表并删除每一个文件
        for file_path in files_to_delete:
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        if not files_to_delete:
            print("No matching files found.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    file_path = "markdown.md"
    markdown_text = read_markdown_file(file_path)
    output_folder = "output"
    output_prefix = ""
    width = 1080  # Adjust width as needed
    height = 1350  # Adjust height as needed
    font_size = 30  # Adjust font size as needed
    line_height = 2

    delete_output_png_files(folder_path=output_folder, pattern='*.png')
    asyncio.run(
        create_images_from_markdown(markdown_text, output_folder, output_prefix, width, height, font_size, line_height))
