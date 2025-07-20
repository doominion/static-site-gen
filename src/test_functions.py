import unittest
from functions import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        nodes = [TextNode("Hello **world**!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "world")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, "!")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        nodes = [TextNode("a**b**c**d**e", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual([n.text for n in result], ["a", "b", "c", "d", "e"])
        self.assertEqual([n.text_type for n in result], [
            TextType.TEXT, TextType.BOLD, TextType.TEXT, TextType.BOLD, TextType.TEXT
        ])

    def test_no_delimiter(self):
        nodes = [TextNode("No delimiter here", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No delimiter here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_non_text_type(self):
        nodes = [TextNode("**bold**", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "**bold**")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_empty_string(self):
        nodes = [TextNode("", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_delimiter_at_edges(self):
        nodes = [TextNode("**edge**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual([n.text for n in result], ["", "edge", ""])
        self.assertEqual([n.text_type for n in result], [
            TextType.TEXT, TextType.BOLD, TextType.TEXT
        ])

    def test_consecutive_delimiters(self):
        nodes = [TextNode("a****b", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertEqual([n.text for n in result], ["a", "", "b"])
        self.assertEqual([n.text_type for n in result], [
            TextType.TEXT, TextType.ITALIC, TextType.TEXT
        ])

    def test_mixed_nodes(self):
        nodes = [
            TextNode("A **B** C", TextType.TEXT),
            TextNode("No split", TextType.TEXT),
            TextNode("**D**", TextType.BOLD)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertEqual([n.text for n in result], ["A ", "B", " C", "No split", "**D**"])
        self.assertEqual([n.text_type for n in result], [
            TextType.TEXT, TextType.ITALIC, TextType.TEXT, TextType.TEXT, TextType.BOLD
        ])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This is a [link](http://example.com)."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "http://example.com")])

    def test_multiple_links(self):
        text = "Links: [Google](https://google.com) and [GitHub](https://github.com)."
        result = extract_markdown_links(text)
        self.assertEqual(result, [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ])

    def text_not_match_images(self):
        text = "This is a ![image](http://example.com). [link](http://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "http://example.com")])

    def test_no_links(self):
        text = "There are no links here."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_link_with_special_characters(self):
        text = "Check [this_link!](https://example.com/path?query=1&other=2)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("this_link!", "https://example.com/path?query=1&other=2")])

    def test_link_with_empty_text(self):
        text = "Empty text []()"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "")])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is a ![image](http://example.com)."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "http://example.com")])

    def test_multiple_images(self):
        text = "images: ![Google](https://google.com) and ![GitHub](https://github.com)."
        result = extract_markdown_images(text)
        self.assertEqual(result, [
            ("Google", "https://google.com"),
            ("GitHub", "https://github.com")
        ])

    def test_no_images(self):
        text = "There are no images here."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_image_with_special_characters(self):
        text = "Check ![this_image!](https://example.com/path?query=1&other=2)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("this_image!", "https://example.com/path?query=1&other=2")])

    def test_image_with_empty_text(self):
        text = "Empty text ![]()"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "")])

class TestSplitNodesImages(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode(
            "Here is an ![img](http://img.com/img.png) in text.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "http://img.com/img.png"),
            TextNode(" in text.", TextType.TEXT),
        ])

    def test_multiple_images(self):
        node = TextNode(
            "A ![one](url1) B ![two](url2) C",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" B ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2"),
            TextNode(" C", TextType.TEXT),
        ])

    def test_image_at_start(self):
        node = TextNode(
            "![start](url) then text",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("start", TextType.IMAGE, "url"),
            TextNode(" then text", TextType.TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode(
            "Text before ![end](url)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "url"),
        ])

    def test_no_images(self):
        node = TextNode(
            "No images here.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_empty_text(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_non_text_type(self):
        node = TextNode(
            "![img](url)",
            TextType.BOLD,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_image_with_empty_alt_and_url(self):
        node = TextNode(
            "Here ![]() is empty.",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(result, [
            TextNode("Here ", TextType.TEXT),
            TextNode(" is empty.", TextType.TEXT),
        ])

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This is a [link](http://example.com).",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.TEXT),
        ])

    def test_multiple_links(self):
        node = TextNode(
            "Links: [Google](https://google.com) and [GitHub](https://github.com).",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Links: ", TextType.TEXT),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("GitHub", TextType.LINK, "https://github.com"),
            TextNode(".", TextType.TEXT),
        ])

    def test_link_at_start(self):
        node = TextNode(
            "[start](url) then text",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("start", TextType.LINK, "url"),
            TextNode(" then text", TextType.TEXT),
        ])

    def test_link_at_end(self):
        node = TextNode(
            "Text before [end](url)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Text before ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url"),
        ])

    def test_no_links(self):
        node = TextNode(
            "No links here.",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_empty_text(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_non_text_type(self):
        node = TextNode(
            "[link](url)",
            TextType.BOLD,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_link_with_empty_text_and_url(self):
        node = TextNode(
            "Here []() is empty.",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Here ", TextType.TEXT),
            TextNode(" is empty.", TextType.TEXT),
        ])

    def test_consecutive_links(self):
        node = TextNode(
            "[a](1)[b](2)[c](3)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("a", TextType.LINK, "1"),
            TextNode("b", TextType.LINK, "2"),
            TextNode("c", TextType.LINK, "3"),
        ])

    def test_mixed_nodes(self):
        nodes = [
            TextNode("A [B](url) C", TextType.TEXT),
            TextNode("No split", TextType.TEXT),
            TextNode("[D](url2)", TextType.LINK, "url2")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("B", TextType.LINK, "url"),
            TextNode(" C", TextType.TEXT),
            TextNode("No split", TextType.TEXT),
            TextNode("[D](url2)", TextType.LINK, "url2"),
        ])

class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "Just plain text."
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Just plain text.", TextType.TEXT)])

    def test_bold_text(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ])

    def test_italic_text(self):
        text = "This is _italic_ text."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ])

    def test_code_text(self):
        text = "Here is `code`."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ])

    def test_bold_and_italic(self):
        text = "Mix **bold** and _italic_ text."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Mix ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ])

    def test_image(self):
        text = "Here is an ![img](url) in text."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here is an ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode(" in text.", TextType.TEXT),
        ])

    def test_link(self):
        text = "A [link](url) here."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" here.", TextType.TEXT),
        ])

    def test_all_features(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://example.com/img.png) and a [link](https://example.com)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ])

    def test_empty_string(self):
        text = ""
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("", TextType.TEXT)])

    def test_consecutive_delimiters(self):
        text = "a****b"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("a", TextType.TEXT),
            TextNode("", TextType.BOLD),
            TextNode("b", TextType.TEXT),
        ])

    def test_image_with_empty_alt_and_url(self):
        text = "Here ![]() is empty."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here ", TextType.TEXT),
            TextNode(" is empty.", TextType.TEXT),
        ])

    def test_link_with_empty_text_and_url(self):
        text = "Here []() is empty."
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("Here ", TextType.TEXT),
            TextNode(" is empty.", TextType.TEXT),
        ])