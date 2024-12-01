from enum import Enum

class TextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    UNDERLINE = "u"
    STRIKETHROUGH = "s"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"



class TextNode():
    def __init__(self,TEXT, TEXT_TYPE, URL=None):
        if not isinstance(TEXT_TYPE, TextType):
            raise ValueError(f"{TEXT_TYPE} is not a valid TextType")
        
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, other_node):
        return self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url
    
    def __repr__(self):
        return(f"TextNode('{self.text}','{self.text_type.value}','{self.url}')")
    
    def __hash__(self):
        return hash((self.text, self.text_type, self.url))

    def __len__(self):
        return len(self.text)
    
    @staticmethod
    def is_valid_text_type(text_type):
        return isinstance(text_type, TextType)
    
    @staticmethod
    def get_markdown_for_text_type(text_type) -> str:
        match text_type:
            case TextType.BOLD:
                return "**"
            case TextType.ITALIC:
                return "*"
            case TextType.UNDERLINE:
                return "__"
            case TextType.STRIKETHROUGH:
                return "~~"
            case TextType.CODE:
                return "`"
            case TextType.LINK:
                return "["
            case TextType.IMAGE:
                return "!"
            