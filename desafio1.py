from xml.dom import minidom

#Ansi escape codes for colors
class colors:
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

#Read the xml file
xmlFile = minidom.parse("./xml/ebay.xml")

def print_node(node, indent=0):
    # Print element name with indentation
    if node.nodeType == node.ELEMENT_NODE:

        child_elements = [child for child in node.childNodes if child.nodeType == child.ELEMENT_NODE]

        #if the current element is a leaf node aka has no childNodes
        if not child_elements:
            textContent = ''.join([child.data.strip() for child in node.childNodes])
            #this print structure may make it more readable in some contexts
            print(" " * indent + f"{colors.BLUE}{node.tagName}:{colors.ENDC}{textContent}")
        #if the current element is not a leaf it has elements and so the previous print
        #structure is not the most adequate
        else:
            print(" " * indent + colors.RED +node.tagName + colors.ENDC)
            
            # Iterate over attributes if any
            for attr_name, attr_value in node.attributes.items():
                print(" " * (indent + 4) + f"{attr_name}    {attr_value}")
            
            # Iterate over child nodes
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    text = child.data.strip()
                    if text:
                        print(" " * (indent + 4) + text)
                else:
                    # Recursively call print_node for child elements
                    print_node(child, indent + 4)

# Start from the root element
print_node(xmlFile.documentElement)
