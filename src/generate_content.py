from markdown_blocks import markdown_to_html_node
from pathlib import Path

import os



def generate_page(from_path: str, template_path: str, dest_path: str | Path, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path} template")

    with open(from_path) as f:
        md_content = f.read()
    with open(template_path) as g:
        template = g.read()
    md_node = markdown_to_html_node(md_content)
    html_content = md_node.to_html()
    title = extract_title(md_content)

    template = template.replace('{{ Title }}', title) # type: ignore
    template = template.replace('{{ Content }}', html_content)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest = os.path.dirname(dest_path)
    if dest:
        os.makedirs(dest, exist_ok=True)
    with open(dest_path, "w") as h:
        h.write(template)


def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            return title
    if len(title) == 0:
        raise Exception("No title found")

def generate_pages_recursive(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    for entry in os.listdir(from_path):
        input_path = os.path.join(from_path, entry)
        output_path = os.path.join(dest_path, entry)
        if os.path.isdir(input_path):
            generate_pages_recursive(input_path, template_path, output_path, basepath)
        if os.path.isfile(input_path):
            output_html = output_path.replace('.md', '.html')
            generate_page(input_path, template_path, output_html, basepath)

    
