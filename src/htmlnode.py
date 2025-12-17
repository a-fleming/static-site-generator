class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        if tag is not None:
            if type(tag) is not str:
                raise TypeError("tag must be a string if provided")
        if value is not None:
            if type(value) is not str:
                raise TypeError("value must be a string if provided")
        if children is not None:
            if type(children) is not list:
                raise TypeError("children must be a list if provided")
        if props is not None:
            if type(props) is not dict:
                raise TypeError("props must be a dictionary if provided")
            
        self.tag = tag
        self.value = value
        self.children = children # if children is not None else []
        self.props = props # if props is not None else {}
    
    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_as_list = [f'{prop}="{val}"' for prop, val in self.props.items()]
        return f' {" ".join(props_as_list)}'

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
        if value is None:
            raise ValueError("LeafNode requires a value")
    
    def to_html(self) -> str:
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        return f'<{self.tag}{props_html}>{self.value}</{self.tag}>'