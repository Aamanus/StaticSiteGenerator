from typing import List
import re
from textnode import *
from htmlnode import *
import os
import shutil

def text_to_textnodes(text):
    out_nodes=[TextNode(text,TextType.TEXT)]
    out_nodes = split_nodes_delimiter(out_nodes, TextNode.get_markdown_for_text_type(TextType.CODE),TextType.CODE)
    out_nodes = split_nodes_delimiter(out_nodes, TextNode.get_markdown_for_text_type(TextType.BOLD),TextType.BOLD)
    out_nodes = split_nodes_delimiter(out_nodes, TextNode.get_markdown_for_text_type(TextType.ITALIC),TextType.ITALIC)
    
    out_nodes = split_nodes_image(out_nodes)
    out_nodes = split_nodes_link(out_nodes)

    return out_nodes

def markdown_to_blocks(text):
    if len(text) == 0:
        raise ValueError("Text cannot be blank.")
    
    output = []

    tmp_split = text.split("\n\n")
    for block in tmp_split:
        if len(block) == 0:
            continue
        output.append(block)

    return output


def text_node_to_html_node(text_node: TextNode):
    # Create a new HTML node
    return LeafNode(text_node.text_type, text_node.text, text_node.url)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
                



def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


            
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph


def copy_directory(src, dst):
    """
    Recursively copies all files and folders from the source directory to the destination directory
    after deleting all existing files and folders in the destination directory.

    :param src: Source directory path
    :param dst: Destination directory path
    """
    # Check if the source directory exists
    if not os.path.exists(src):
        print(f"Source directory '{src}' does not exist.")
        return

    # Remove the destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)  # Remove the entire directory tree

    # Create the destination directory
    os.makedirs(dst)

    # Iterate over the items in the source directory
    for item in os.listdir(src):
        # Create full path to the item
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        # If the item is a directory, recursively copy it
        if os.path.isdir(s):
            copy_directory(s, d)
        else:
            # If the item is a file, copy it
            shutil.copy2(s, d)  # Use copy2 to preserve metadata

# Example usage
# copy_directory('path/to/source', 'path/to/destination')

def extract_title(markdown):
    if len(markdown) == 0:
        raise Exception("Markdown is empty!")
    
    lines = markdown.split('\n')
    title = ''
    for line in lines:
        if line.startswith('#'):
            title = line.replace("#","")
            title = title.strip()
            return title
    raise Exception("No title was found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path)
    template_file = open(template_path)
    markdown = markdown_file.read()
    template = template_file.read()
    markdown_file.close()
    template_file.close()
    title = extract_title(markdown)
    
    html = markdown_to_html_node(markdown)
    html_string = html.to_html()
    print(title)
    page = template.replace('{{ title }}', title).replace('{{ content }}', html_string)
    with open(dest_path, 'w') as f:
        f.write(page)
        print(f"Page generated successfully!")
        f.close()
    
    return True




def markdown_to_html_node(markdown):
    # Step 1: Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Step 2: Create a parent HTMLNode (a div)
    parent_node = HTMLNode("div", "", [])  # Assuming HTMLNode takes tag, text, and children

    # Step 3: Loop over each block
    for block in blocks:
        # Step 4: Determine the type of block
        block_type = block_to_block_type(block)
        
        # Step 5: Create a new HTMLNode based on the block type
        if block_type == block_type_paragraph:
            block_node = HTMLNode("p", "", text_to_children(block))
        elif block_type == block_type_heading:
            level = block.count('#')  # Count the number of '#' to determine heading level
            block_node = HTMLNode(f"h{level}", "", text_to_children(block))
        elif block_type == block_type_code:
            block_node = HTMLNode("pre", "", text_to_children(block))
        elif block_type == block_type_quote:
            block_node = HTMLNode("blockquote", "", text_to_children(block))
        elif block_type == block_type_olist:
            block_node = HTMLNode("ol", "", text_to_children(block))
        elif block_type == block_type_ulist:
            block_node = HTMLNode("ul", "", text_to_children(block))
        else:
            # Default to paragraph if block type is not recognized
            block_node = HTMLNode("p", "", text_to_children(block))

        # Step 6: Append the block node to the parent node
        parent_node.children.append(block_node)

    # Step 7: Return the parent HTMLNode
    return parent_node

def text_to_children(text):
    # This function should convert the text into a list of HTMLNode objects
    # For example, it could use the text_to_textnodes function to create TextNodes
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]