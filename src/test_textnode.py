import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("this is a text node", TextType.ITALIC)
        node2 = TextNode("this is a text node", TextType.ITALIC, "not None")
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("this is a text node", TextType.TEXT)
        node2 = TextNode("this is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_text_to_leaf(self):
        node = TextNode("this is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a text node")

    def test_bold_to_leaf(self):
        node = TextNode("this is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is a text node")

    def test_italic_to_leaf(self):
        node = TextNode("this is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is a text node")

    def test_code_to_leaf(self):
        node = TextNode("this is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "this is a text node")

    def test_link_to_leaf(self):
        node = TextNode("this is a text node", TextType.LINK, "this is a fake link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this is a text node")
        assert html_node.props is not None
        self.assertEqual(html_node.props["href"], "this is a fake link.com")

    def test_image_to_leaf(self):
        node = TextNode("this is a text node", TextType.IMAGE, "this is a fake link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")       # MUST return an empty-string .value
        assert html_node.props is not None
        self.assertEqual(html_node.props["src"], "this is a fake link.com")
        self.assertEqual(html_node.props["alt"], "this is a text node")

    def test_image_to_leaf_missing_url(self):
        node = TextNode("this is a text node", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "invalid or missing URL")

    def test_invalid_type_raises(self):
        node = TextNode("this is a text node", TextType.TEXT)
        node.text_type = "not_a_real_type"  # type: ignore       #this ignores the warning that not_a_real_type is not a real type
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "text_node.text_type is invalid")
if __name__ == "__main__":
    unittest.main()