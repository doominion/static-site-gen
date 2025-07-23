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

if __name__ == "__main__":
    unittest.main()
