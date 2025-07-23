import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_no_tag_raises(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node]).to_html()

    def test_to_html_with_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "one")
        child2 = LeafNode("b", "two")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), "<div><span>one</span><b>two</b></div>")

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        # props order may vary, so check both possibilities
        html = parent.to_html()
        self.assertTrue(
            html == '<div class="container" id="main"><span>child</span></div>'
            or html == '<div id="main" class="container"><span>child</span></div>'
        )

    def test_to_html_nested_with_props(self):
        grandchild = LeafNode("i", "deep")
        child = ParentNode("span", [grandchild], props={"style": "color:red"})
        parent = ParentNode("div", [child], props={"class": "top"})
        html = parent.to_html()
        self.assertIn('<div', html)
        self.assertIn('class="top"', html)
        self.assertIn('<span style="color:red">', html)
        self.assertIn('<i>deep</i>', html)
        self.assertTrue(html.startswith('<div'))
        self.assertTrue(html.endswith('</div>'))

    def test_to_html_with_non_leaf_child(self):
        child = ParentNode("ul", [
            LeafNode("li", "item1"),
            LeafNode("li", "item2")
        ])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            "<div><ul><li>item1</li><li>item2</li></ul></div>"
        )

if __name__ == "__main__":
    unittest.main()
   