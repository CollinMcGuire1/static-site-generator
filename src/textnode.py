from enum import Enum
from htmlnode import LeafNode, ParentNode, HTMLNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
    
        self.text = text
        self.text_type  = text_type
        self.url = url
    def __eq__(self, other):
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)
    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        html_node = LeafNode(None, f"{text_node.text}")
        return html_node
    elif text_node.text_type == TextType.BOLD:
        html_node = LeafNode("b", f"{text_node.text}")
        return html_node
    elif text_node.text_type == TextType.ITALIC:
        html_node = LeafNode("i", f"{text_node.text}")
        return html_node
    elif text_node.text_type == TextType.CODE:
        html_node = LeafNode("code", f"{text_node.text}")
        return html_node
    elif text_node.text_type == TextType.LINK:
        html_node = LeafNode("a", f"{text_node.text}", {"href": text_node.url})
        return html_node
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("invalid or missing URL")
        html_node = LeafNode("img", "", {"alt": text_node.text, "src": text_node.url})
        return html_node
    else:
        raise ValueError("text_node.text_type is invalid")
    