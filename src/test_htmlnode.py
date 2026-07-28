import unittest
#from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        tag = "this is a tag"
        tag2 = "this is a tag"      # this should be the same as "tag" for the test_eq to be true
        value = "this is a value"
        children = ["this", "is", "a", "list", "of", "children"]
        props = {
            "this is a key": "this is the value of 'this is a key'",
            "this is 2 key": "this is 2 value",
            "this is 3 key": "this is 3 value",
        }

        node = HTMLNode(tag, value, children, props)
        node2 = HTMLNode(tag2, value, children, props)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("this is a tag", "this is a value")
        node2 = HTMLNode("this is a DIFFERENT tag", "this is a DIFFERENT value")
        self.assertNotEqual(node, node2)


    def test_props_to_html(self):
        tag = "this is a tag"
        value = "this is a value"
        children = ["this", "is", "a", "list", "of", "children"]
        props = {
            "this is a key": "this is the value",
        }

        node = HTMLNode(tag, value, children, props)
        result = node.props_to_html()

        self.assertEqual(result, ' this is a key="this is the value"')

    def test_empty_props_to_html(self):
        tag = "this is a tag"
        value = "this is a value"
        children = ["this", "is", "a", "list", "of", "children"]

        node = HTMLNode(tag, value, children)
        result = node.props_to_html()

        self.assertEqual(result, "")

    def test_empty_dict_props_to_html(self):
        tag = "this is a tag"
        value = "this is a value"
        children = ["this", "is", "a", "list", "of", "children"]
        props = {}

        node = HTMLNode(tag, value, children, props)
        result = node.props_to_html()

        self.assertEqual(result, "")

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_raw_text(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Visit site", {"href": "https://example.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com">Visit site</a>',
        )

    def test_leaf_missing_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
