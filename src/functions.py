
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    from textnode import TextNode, TextType
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
    import re
    img_regex = r'!\[(.*?)\]\((.*?)\)'
    matches = re.findall(img_regex, text)
    result = []
    for alt_text, url in matches:
        result.append((alt_text, url))
    return result

def extract_markdown_links(text):
    import re
    link_regex = r'(?<!!)\[(.*?)\]\((.*?)\)'
    matches = re.findall(link_regex, text)
    result = []
    for link_text, url in matches:
        result.append((link_text, url))
    return result

def split_nodes_image(old_nodes):
    from textnode import TextNode, TextType
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
    from textnode import TextNode, TextType
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

def text_to_textnodes(text):
    from textnode import TextNode, TextType
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE)]
    for delimiter, type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes