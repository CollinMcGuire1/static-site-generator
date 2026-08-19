from markdown_blocks import markdown_to_html_node


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

    replaced_title = template.replace('{{ Title }}', title) # type: ignore
    replaced_html_content = replaced_title.replace('{{ Content }}', html_content)

    dest = os.path.dirname(dest_path)
    if dest:
        os.makedirs(dest, exist_ok=True)
    with open(dest_path, "w") as h:
        h.write(replaced_html_content)


def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            return title
    if len(title) == 0:
        raise Exception("No title found")

def dir_walk(from_path, template_path, dest_path):
    for entry in os.listdir(from_path):
        input_path = os.path.join(from_path, entry)
        output_path = os.path.join(dest_path, entry)
        if os.path.isdir(input_path):
            dir_walk(input_path, template_path, output_path)
        if os.path.isfile(input_path):
            output_html = output_path.replace('.md', '.html')
            generate_page(input_path, template_path, output_html)

    
