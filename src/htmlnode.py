class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
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
    