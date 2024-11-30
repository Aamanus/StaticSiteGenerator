import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_initialization(self):
        node = TextNode("Sample text", TextType.BOLD)
        self.assertEqual(node.text, "Sample text")
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_text_retrieval(self):
        node = TextNode("Another sample", TextType.ITALIC)
        self.assertEqual(node.text, "Another sample")

    def test_text_type(self):
        node = TextNode("Sample text", TextType.BOLD)
        self.assertEqual(node.text_type, TextType.BOLD)

    def test_inequality_different_text(self):
        node1 = TextNode("Text A", TextType.BOLD)
        node2 = TextNode("Text B", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_inequality_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_string_representation(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertEqual(str(node), "TextNode('Hello','b','None')")  

    def test_hashing(self):
        node1 = TextNode("Hashable text", TextType.TEXT)
        node2 = TextNode("Hashable text", TextType.TEXT)
        self.assertEqual(hash(node1), hash(node2))

if __name__ == "__main__":
    unittest.main()