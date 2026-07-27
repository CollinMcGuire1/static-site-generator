from textnode import TextNode, TextType

def main():
    new_node = TextNode("dummy text", TextType.BOLD, "dumb URL")
    print(new_node)
main()