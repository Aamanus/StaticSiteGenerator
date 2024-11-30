import unittest

# Assuming the LeafNode class is defined in a module named htmlnode
from htmlnode import LeafNode  # Adjust the import according to your project structure

class TestLeafNode(unittest.TestCase):

    def test_initialization_with_all_params(self):
        # Test the initialization of the LeafNode with all parameters
        node = LeafNode(tag="p", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting"})

    def test_initialization_with_none_props(self):
        # Test initialization without props, expecting props to be None
        node = LeafNode(tag="h1", value="This is a header.")
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.value, "This is a header.")
        self.assertIsNone(node.props)  # Expect props to be None

    def test_to_html_with_value(self):
        # Test the to_html method with a valid value
        node = LeafNode(tag="span", value="Text content", props={"style": "color:red;"})
        expected_output = '<span style="color:red;">Text content</span>'
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_with_none_value(self):
        # Test the to_html method with None as value
        node = LeafNode(tag="div", value=None, props={"class": "container"})
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Value is required but not set")

    def test_to_html_with_none_tag(self):
        # Test the to_html method with None as tag
        node = LeafNode(tag=None, value="Just text", props={"class": "text-only"})
        expected_output = 'Just text'  # No tag should return just the value
        self.assertEqual(node.to_html(), expected_output)

    def test_props_to_html(self):
        # Test the props_to_html method
        node = LeafNode(tag="input", value=None, props={"type": "text", "placeholder": "Enter text"})
        expected_props_html = ' type="text" placeholder="Enter text"'
        self.assertEqual(node.props_to_html(), expected_props_html)

if __name__ == "__main__":
    unittest.main()