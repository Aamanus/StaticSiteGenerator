

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This method should be set by the subclass")
    
    def props_to_html(self):
        if not isinstance(self.props,dict):
            return ""
        
        props_html = ""
        for key, value in self.props.items():
            props_html += f" {key}=\"{value}\""
        return props_html
        
    def __repr__(self):
        return(f"HTMLNode('{self.tag}','{self.value}','{self.children}','{self.props}')")
    
    def __eq__(self, other_node):
        return str(self) == str(other_node)
    
# Subclasses for different types of HTML nodes

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):

        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value==None:
            raise ValueError("Value is required but not set")
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag set")
        output = f"<{self.tag}>"
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("Children must be instances of HTMLNode")
            
            output += child.to_html()
        
        output += f"</{self.tag}>"
        return output
    
            

        