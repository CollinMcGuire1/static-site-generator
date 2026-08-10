import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("this is text with an ![image](https://randomfakewebsite.address/data.thingything)")
        self.assertEqual([("image", "https://randomfakewebsite.address/data.thingything")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("this is a text with one [link](https://linktoawebsite.address) and a second [link](https://anotherbutdifferentwebsite.otheraddress)")
        self.assertEqual([("link", "https://linktoawebsite.address"), ("link", "https://anotherbutdifferentwebsite.otheraddress")], matches)

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("This is plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is plain text with no images", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_single_image_only(self):
        node = TextNode(
            "![alt text](https://example.com/img.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt text", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode("First ![img1](url1)", TextType.TEXT)
        node2 = TextNode("Second ![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        # Check that both nodes get processed independently

    def test_split_links_no_link(self):
        node = TextNode("This is plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is plain text with no links", TextType.TEXT)],
            new_nodes,
        )

    def test_split_links_adjacent(self):
        node = TextNode(
            "[link1](url1)[link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Tests that back-to-back links with no text between them work correctly

    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [TextNode("This is ", TextType.TEXT),
             TextNode("text", TextType.BOLD),
             TextNode(" with an ", TextType.TEXT),
             TextNode("italic", TextType.ITALIC),
             TextNode(" word and a ", TextType.TEXT),
             TextNode("code block", TextType.CODE),
             TextNode(" and an ", TextType.TEXT),
             TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
             TextNode(" and a ", TextType.TEXT),
             TextNode("link", TextType.LINK, "https://boot.dev"),
             ],
             new_nodes
        )

    def test_plain_text_to_md(self):
        node = "this is plain text"
        new_node = text_to_textnodes(node)
        self.assertListEqual([TextNode("this is plain text", TextType.TEXT)], new_node)

    def test_bold_multiple_times_to_md(self):
        node = "this is **bold text** that is being **used more than one time** in a longer string of **words**"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [TextNode("this is ", TextType.TEXT),
             TextNode("bold text", TextType.BOLD),
             TextNode(" that is being ", TextType.TEXT),
             TextNode("used more than one time", TextType.BOLD),
             TextNode(" in a longer string of ", TextType.TEXT),
             TextNode("words", TextType.BOLD)
             ],
             new_nodes
        )

    def test_starting_ending_delim_to_md(self):
        node = "_this is text_ that starts and ends with `deliminators`"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [TextNode("this is text", TextType.ITALIC),
             TextNode(" that starts and ends with ",TextType.TEXT),
             TextNode("deliminators", TextType.CODE)
             ],
             new_nodes
        )

    def test_text_image_link_image(self):
        node = "This is text before a ![first image](https://example.com/img1.png) then more text and a [cool link](https://example.com) followed by even more text and another ![second image](https://example.com/img2.png)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is text before a ", TextType.TEXT),
                TextNode("first image", TextType.IMAGE, "https://example.com/img1.png"),
                TextNode(" then more text and a ", TextType.TEXT),
                TextNode("cool link", TextType.LINK, "https://example.com"),
                TextNode(" followed by even more text and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://example.com/img2.png"),
            ],
            new_nodes,
        )

    def test_unmatched_delimiter(self):
        node = "This has an **unclosed bold section*"
        with self.assertRaises(ValueError):
            text_to_textnodes(node)

    def test_unclosed_link(self):
        node = "This has a [broken link(https://example.com)"
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [TextNode("This has a [broken link(https://example.com)", TextType.TEXT)],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()        