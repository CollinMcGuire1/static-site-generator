import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """

This is a paragraph.

This is another paragraph.


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another paragraph.",
            ],
        )

    def test_markdown_to_blocks_excessive_whitespace(self):
        md = """
This is block 1.

   

This is block 2.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is block 1.",
                "This is block 2.",
            ],
        )

    def test_markdown_to_blocks_strip(self):
        md = """
  # Heading with leading spaces  

   Paragraph with extra surrounding space.   
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with leading spaces",
                "Paragraph with extra surrounding space.",
            ],
        )

    def test_markdown_to_blocks_multiple_types(self):
        md = """
# Title

> This is a quote block.

- Item 1
- Item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Title",
                "> This is a quote block.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

""" TO ADD, PER CONV IN CH4:L3:

Since your two provided tests (test_paragraphs and test_codeblock) now pass, you've covered the basics, but the lesson tips hint at several other block types you should verify: headings, quotes, ordered lists, and unordered lists. It's worth writing a test for each block type your block_to_block_type function recognizes, since your dispatcher had a blind spot before — better to make sure the others are wired up correctly too.

Here are some tests worth adding:

    Headings — verify a block like "# Heading" produces <h1>Heading</h1>, and test a couple different levels (e.g. ##, ###) to make sure the numbering translates correctly to h2, h3, etc.
    Unordered lists — verify a block like:

    - item one
    - item two

produces <ul><li>item one</li><li>item two</li></ul>.
Ordered lists — verify a block like:

1. first
2. second

produces <ol><li>first</li><li>second</li></ol>.
Quotes — verify a block like:

> quoted text
> more quoted text

produces <blockquote>quoted text more quoted text</blockquote>.
Mixed document — a full markdown document combining a heading, a paragraph, a list, and a code block all together, to make sure markdown_to_html_node correctly assembles them all as siblings inside the outer <div>.
Inline markdown inside blocks — test a heading or list item that contains bold/italic/code/links, to confirm text_to_children is properly parsing inline syntax within those block types (not just paragraphs).
"""

if __name__ == "__main__":
    unittest.main()
