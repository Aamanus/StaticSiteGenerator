import unittest

# Assuming the HTMLNode class is defined in a module named htmlnode
from htmlnode import HTMLNode  # Adjust the import according to your project structure

class TestHTMLNode(unittest.TestCase):

    def test_initialization_with_all_params(self):
        # Test the initialization of the HTMLNode with all parameters
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting"})

    def test_initialization_with_none_props(self):
        # Test initialization without props, expecting props to be None
        node = HTMLNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph.")
        self.assertIsNone(node.props)  # Expect props to be None

    def test_initialization_with_none_value(self):
        # Test initialization with None as value
        node = HTMLNode(tag="h1", value=None, props={"class": "header"})
        self.assertEqual(node.tag, "h1")
        self.assertIsNone(node.value)  # Expect value to be None
        self.assertEqual(node.props, {"class": "header"})

    def test_equality_same_node(self):
        # Test that two identical nodes are considered equal
        node1 = HTMLNode(tag="span", value="Text", props={"style": "color:red;"})
        node2 = HTMLNode(tag="span", value="Text", props={"style": "color:red;"})
        self.assertEqual(node1, node2)

    def test_inequality_different_tag(self):
        # Test that nodes with different tags are not equal
        node1 = HTMLNode(tag="div", value="Content")
        node2 = HTMLNode(tag="span", value="Content")
        self.assertNotEqual(node1, node2)

    def test_inequality_different_value(self):
        # Test that nodes with different values are not equal
        node1 = HTMLNode(tag="div", value="Content A")
        node2 = HTMLNode(tag="div", value="Content B")
        self.assertNotEqual(node1, node2)

    def test_inequality_different_props(self):
        # Test that nodes with different properties are not equal
        node1 = HTMLNode(tag="div", value="Content", props={"class": "my-class"})
        node2 = HTMLNode(tag="div", value="Content", props={"class": "other-class"})
        self.assertNotEqual(node1, node2)

    def test_string_representation(self):
        # Test the string representation of the node
        node = HTMLNode(tag="a", value="Click here", props={"href": "http://example.com"})
        expected_output = "HTMLNode('a','Click here','None','{'href': 'http://example.com'}')"
        self.assertEqual(str(node), expected_output)

    def test_props_to_html(self):
        # Test the props_to_html method
        node = HTMLNode(tag="input", value=None, props={"type": "text", "placeholder": "Enter text"})
        expected_props_html = ' type="text" placeholder="Enter text"'
        self.assertEqual(node.props_to_html(), expected_props_html)

if __name__ == "__main__":
    unittest.main()