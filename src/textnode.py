from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        return node.text == self.text and node.url == self.url and node.text_type == self.text_type

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"