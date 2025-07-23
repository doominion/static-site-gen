from blocktype import BlockType
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT and delimiter in node.text:
            parts = node.text.split(delimiter)

            for idx in range(len(parts)):
                new_node_type = node.text_type
                
                if idx % 2 != 0:
                    new_node_type = text_type

                new_node = TextNode(parts[idx], new_node_type)                
                node_list.append(new_node)
        else:
            node_list.append(node)

    return node_list

def extract_markdown_images(text):
    img_regex = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(img_regex, text)
    result = []
    for alt_text, url in matches:
        result.append((alt_text, url))
    return result

def extract_markdown_links(text):
    link_regex = r'(?<!!)\[(.*?)\]\((.*?)\)'
    matches = re.findall(link_regex, text)
    result = []
    for link_text, url in matches:
        result.append((link_text, url))
    return result

def split_nodes_image(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            node_list.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        remaining_text = node.text

        if images:
            for text, url in images:
                parts = remaining_text.split(f'![{text}]({url})', 1)
                if parts[0] != "":
                    node_list.append(TextNode(parts[0], TextType.TEXT))
                remaining_text = parts[1]
                if text == "":
                    continue
                node_list.append(TextNode(text, TextType.IMAGE, url))
            if remaining_text != "":
                node_list.append(TextNode(remaining_text, TextType.TEXT))
        else:
            node_list.append(node)
    return node_list
            
def split_nodes_link(old_nodes):
    node_list = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            node_list.append(node)
            continue

        links = extract_markdown_links(node.text)
        remaining_text = node.text

        if links:
            for text, url in links:
                parts = remaining_text.split(f'[{text}]({url})', 1)
                if parts[0] != "":
                    node_list.append(TextNode(parts[0], TextType.TEXT))
                remaining_text = parts[1]
                if text == "":
                    continue
                node_list.append(TextNode(text, TextType.LINK, url))
            if remaining_text:
                node_list.append(TextNode(remaining_text, TextType.TEXT))
        else:
            node_list.append(node)
    return node_list

def text_node_to_html_node(self):
    if self.text_type == TextType.TEXT:
        return LeafNode(None, self.text)
    elif self.text_type == TextType.BOLD:
        return LeafNode("b", self.text)
    elif self.text_type == TextType.ITALIC:
        return LeafNode("i", self.text)
    elif self.text_type == TextType.CODE:
        return LeafNode("code", self.text)
    elif self.text_type == TextType.LINK:
        return LeafNode("a", self.text, props={"href": self.url})
    elif self.text_type == TextType.IMAGE:
        return LeafNode("img", '', props={"src": self.url, "alt": self.text})
    else:
        raise ValueError(f"Unknown text type: {self.text_type}")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]
    for delimiter, type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    parts = markdown.split("\n\n")
    blocks = []
    for part in parts:
        block = part.strip()
        if(block == ""):
            continue
        blocks.append(block)

    return blocks

def block_to_block_type(block):
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("## "):
        return BlockType.HEADING
    elif block.startswith("### "):
        return BlockType.HEADING
    elif block.startswith("#### "):
        return BlockType.HEADING
    elif block.startswith("##### "):
        return BlockType.HEADING
    elif block.startswith("###### "):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"\d+\.\s", block[:10]):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return orderedlist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unorderedlist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block.strip("```")
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def orderedlist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def unorderedlist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    
    raise Exception("No title found in markdown")
