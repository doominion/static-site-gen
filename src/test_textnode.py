import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_print(self):
        node = TextNode("node 1", "type_1")
        self.assertEqual("TextNode(node 1, type_1, None)", f"{node}")

    def test_none_url(self):
        node = TextNode("node", "type")
        self.assertEqual(None, node.url)

    def test_same_type(self):
        node = TextNode("node", "type")
        node2 = TextNode("node", "type2")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        node = TextNode("plain text", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "plain text")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_link(self):
        node = TextNode("link text", TextType.LINK, url="https://example.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_node_image(self):
        node = TextNode("alt text", TextType.IMAGE, url="https://img.com/img.png")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://img.com/img.png", "alt": "alt text"})

    def test_text_node_to_html_node_invalid_type(self):
        node = TextNode("unknown", "not_a_type")
        with self.assertRaises(ValueError):
            node.text_node_to_html_node()

if __name__ == "__main__":
    unittest.main()
