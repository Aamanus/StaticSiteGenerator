import unittest

# Assuming the ParentNode class is defined in a module named htmlnode
from htmlnode import ParentNode, LeafNode  # Adjust the import according to your project structure

class TestParentNode(unittest.TestCase):

    def test_initialization_with_all_params(self):
        # Test the initialization of the ParentNode with all parameters
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "parent"})
        
        self.assertEqual(parent.tag, "div")
        self.assertEqual(parent.children, [child1, child2])
        self.assertEqual(parent.props, {"class": "parent"})

    def test_initialization_with_none_props(self):
        # Test initialization without props, expecting props to be None
        child = LeafNode(tag="h1", value="Header")
        parent = ParentNode(tag="section", children=[child])
        
        self.assertEqual(parent.tag, "section")
        self.assertEqual(parent.children, [child])
        self.assertIsNone(parent.props)  # Expect props to be None

    def test_to_html_with_children(self):
        # Test the to_html method with valid children
        child1 = LeafNode(tag="p", value="First child")
        child2 = LeafNode(tag="p", value="Second child")
        parent = ParentNode(tag="div", children=[child1, child2])
        
        expected_output = '<div><p>First child</p><p>Second child</p></div>'
        self.assertEqual(parent.to_html(), expected_output)

    def test_to_html_with_empty_children(self):
        # Test the to_html method with no children
        parent = ParentNode(tag="ul", children=[])
        
        expected_output = '<ul></ul>'
        self.assertEqual(parent.to_html(), expected_output)

    def test_to_html_with_invalid_child(self):
        # Test the to_html method with an invalid child type
        parent = ParentNode(tag="div", children=["Invalid child"])
        
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "Children must be instances of HTMLNode")

    def test_to_html_with_none_tag(self):
        # Test the to_html method with None as tag
        child = LeafNode(tag="p", value="Content")
        parent = ParentNode(tag=None, children=[child])
        
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "No tag set")

    def test_props_to_html(self):
        # Test the props_to_html method
        child = LeafNode(tag="span", value="Child")
        parent = ParentNode(tag="div", children=[child], props={"id": "parent-div"})
        
        expected_props_html = ' id="parent-div"'
        self.assertEqual(parent.props_to_html(), expected_props_html)

if __name__ == "__main__":
    unittest.main()