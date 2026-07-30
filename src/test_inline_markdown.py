import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another** bolded word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
                TextNode(" bolded word", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with multiple **bolded words** and **another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with multiple ", TextType.TEXT),
                TextNode("bolded words", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD), [])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("A **bold** word", TextType.TEXT),
            TextNode("An **important** word", TextType.TEXT),
        ]
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("An ", TextType.TEXT),
            TextNode("important", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "**", TextType.BOLD),
            expected,
        )

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [node],
        )

    def test_multiple_pairs(self):
        node = TextNode("A **bold** and **strong** sentence", TextType.TEXT)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode(" sentence", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_delimiter_at_beginning(self):
        node = TextNode("`code` afterward", TextType.TEXT)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" afterward", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            expected,
        )

    def test_delimiter_at_end(self):
        node = TextNode("Before _italic_", TextType.TEXT)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            expected,
        )

    def test_no_delimiter(self):
        node = TextNode("Plain text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [node],
        )

    def test_unmatched_delimiter(self):
        node = TextNode("An **unfinished phrase", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_supported_delimiters(self):
        cases = [
            ("**bold**", "**", TextType.BOLD, "bold"),
            ("_italic_", "_", TextType.ITALIC, "italic"),
            ("`code`", "`", TextType.CODE, "code"),
        ]
        for source, delimiter, text_type, content in cases:
            with self.subTest(delimiter=delimiter):
                self.assertEqual(
                    split_nodes_delimiter(
                        [TextNode(source, TextType.TEXT)],
                        delimiter,
                        text_type,
                    ),
                    [TextNode(content, text_type)],
                )

    def test_empty_delimited_content(self):
        node = TextNode("Before **** after", TextType.TEXT)
        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_three_asterisks_treated_as_double_asterisk_delimiter(self):
        node = TextNode("***word***", TextType.TEXT)
        expected = [
            TextNode("*word", TextType.BOLD),
            TextNode("*", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )

    def test_four_asterisks(self):
        node = TextNode("****word****", TextType.TEXT)
        expected = [
            TextNode("word", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            expected,
        )


if __name__ == "__main__":
    unittest.main()        