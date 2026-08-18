


# need to write tests for extract_title()
def extract_title(markdown):
    lines = markdown.split("\n")
    title = ""

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            return title
    if len(title) == 0:
        raise Exception("No title found")
    
