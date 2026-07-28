

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag                  # "string HTML tag name; i.e. 'p', 'a', 'h1', etc."
        self.value = value              # "string value of the HTML tag, like text inside of a paragraph"
        self.children = children        # "LIST of HTMLNode children objects"
        self.props = props              # "DICTIONARY of attributes of HTML tag, ex link (<a> tag) might have {'href'': 'https://www.google.com'}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or not self.props:
            return ""

        string = ""
        for key in self.props:
            value = self.props[key]
            string += f' {key}="{value}"'
        return string

    def __repr__(self):
        tag = "Tag:"
        value = "Value:"
        children = "Children:"
        props = "Props:"
        return f"{tag:<12}{self.tag}\n{value:<12}{self.value}\n{children:<12}{self.children}\n{props:<12}{self.props}"

    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super(LeafNode, self,).__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError        # all nodes MUST have a value
        if self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        tag = "Tag:"
        value = "Value:"
        props = "Props:"
        return f"{tag:<12}{self.tag}\n{value:<12}{self.value}\n{props:<12}{self.props}"