import pandas as pd
import xml.etree.ElementTree as ET
from lxml import etree

xml_base_dir = "./xml/"

def csv_to_xml(filepath):
    root = ET.Element("root")

    df = pd.read_csv(filepath, sep=',')
    for _, row in df.iterrows():
        item = ET.SubElement(root, "item")

        for col in df.columns:
            col_element = ET.SubElement(item, col.replace(' ', "_"))
            col_element.text = str(row[col])

    tree = ET.ElementTree(root)

    with open("./xml/output.xml", "wb") as xmlFile:
        tree.write(xmlFile)

def xml_xpath_query(filepath, query, filename):
    tree = etree.parse(filepath)

    products = tree.xpath(query)

    subxml_root = etree.Element("filtered_catalog")

    for product in products:
        subxml_root.append(product)
    
    subxml_str = etree.tostring(subxml_root, pretty_print=True)
    print(subxml_str)

    with open(xml_base_dir + filename, "wb") as f:
        f.write(etree.tostring(subxml_root, pretty_print=True))

#Split into individual sellers and dealerships
xml_xpath_query("xml/output.xml","//item[seller_type='Individual']", "individual.xml" )
xml_xpath_query("xml/output.xml","//item[seller_type='Dealer']", "dealership.xml" )

#Split by fuel types
xml_xpath_query("xml/output.xml","//item[fuel='Diesel']", "diesel.xml" )
xml_xpath_query("xml/output.xml","//item[fuel='Petrol']", "petrol.xml" )
xml_xpath_query("xml/output.xml","//item[fuel='Electric']", "electric.xml" )

#Split by transmition type
xml_xpath_query("xml/output.xml","//item[transmition='Manual']", "manual_transmition.xml" )
xml_xpath_query("xml/output.xml","//item[transmition='Automatic']", "automatic_transmition.xml" )

#Split by owner ammount
xml_xpath_query("xml/output.xml","//item[owner='First Owner']", "first_owner.xml" )
xml_xpath_query("xml/output.xml","//item[owner='Second Owner']", "second_owner.xml" )
xml_xpath_query("xml/output.xml","//item[owner='Third Owner']", "third_owner.xml" )
xml_xpath_query("xml/output.xml","//item[owner='Fourth Owner & Above Owner']", "fourth_owner_&_above.xml" )

