import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_to_html_with_tag_and_props(self):
        node = LeafNode("a", "Click here", {"href": "https://example.com", "target": "_blank"})
        html = node.to_html()
        assert html == '<a href="https://example.com" target="_blank">Click here</a>'

    def test_leafnode_to_html_with_tag_no_props(self):
        node = LeafNode("p", "Hello, world!")
        html = node.to_html()
        assert html == "<p>Hello, world!</p>"

    def test_leafnode_to_html_without_tag(self):
        node = LeafNode(None, "Just text")
        html = node.to_html()
        assert html == "Just text"

    def test_leafnode_to_html_raises_when_value_none(self):
        node = LeafNode("span", None)
        try:
            node.to_html()
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == "LeafNode must have a value"

if __name__ == "__main__":
    unittest.main()