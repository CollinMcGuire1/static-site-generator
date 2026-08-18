from markdown_blocks import markdown_to_html_node
from extract_markdown_title import extract_title

import os



def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} template")

    with open(from_path) as f:
        md_content = f.read()
    with open(template_path) as g:
        template = g.read()
    md_node = markdown_to_html_node(md_content)
    html_content = md_node.to_html()
    title = extract_title(md_content)

    replaced_title = template.replace('{{ Title }}', title)
    replaced_html_content = replaced_title.replace('{{ Content }}', html_content)

    dest = os.path.dirname(dest_path)
    if dest:
        os.makedirs(dest, exist_ok=True)
    with open(dest_path, "w") as h:
        h.write(replaced_html_content)