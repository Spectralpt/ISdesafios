import pandas as pd
import xml.etree.ElementTree as ET

df = pd.read_csv('./csv/winequality-red.csv', sep=';')

root = ET.Element("root")

for _, row in df.iterrows():
    item = ET.SubElement(root, "item")

    for col in df.columns:
        col_element = ET.SubElement(item, col.replace(' ', "_"))
        col_element.text = str(row[col])

tree = ET.ElementTree(root)
with open("./xml/output.xml", "wb") as xmlFile:
    tree.write(xmlFile)
