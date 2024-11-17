import pandas as pd
from lxml import etree

xml_base_dir = "./xml/"

def validate(xmlTree):
    xmlschema = etree.XMLSchema(etree.parse("xml/output.xsd"))
    return xmlschema.validate(xmlTree)

def csv_to_xml(filepath):
    root = etree.Element("root")

    df = pd.read_csv(filepath, sep=',')
    for _, row in df.iterrows():
        item = etree.SubElement(root, "item")

        for col in df.columns:
            col_element = etree.SubElement(item, col.replace(' ', "_"))
            col_element.text = str(row[col])

    tree = etree.ElementTree(root)

    if validate(tree) == True:
        print(f"Base xml is valid")
        with open("./xml/output.xml", "wb") as xmlFile:
            tree.write(xmlFile)
    else:
        print(f"Base xml is invalid")

def xml_xpath_query(filepath, query, filename):
    tree = etree.parse(filepath)

    products = tree.xpath(query)

    subxml_root = etree.Element("filtered_catalog")

    for product in products:
        subxml_root.append(product)
    
    subxml_str = etree.tostring(subxml_root, pretty_print=True)

    if validate(tree) == True:
        print(f"{filename} is valid")
        with open(xml_base_dir + filename, "wb") as f:
            f.write(etree.tostring(subxml_root, pretty_print=True))
    else:
        print(f"{filename} is invalid")
        print(f"{filename} is valid")

#Convert csv to xml
csv_to_xml("csv/car.csv")

#Split into individual sellers and dealerships
xml_xpath_query("xml/output.xml","//item[seller_type='Individual']", "individual.xml" )
xml_xpath_query("xml/output.xml","//item[seller_type='Dealer']", "dealership.xml" )

#Split by fuel types
xml_xpath_query("xml/output.xml","//item[fuel='Diesel']", "diesel.xml" )
xml_xpath_query("xml/output.xml","//item[fuel='Petrol']", "petrol.xml" )
xml_xpath_query("xml/output.xml","//item[fuel='Electric']", "electric.xml" )

#Split by transmition type
xml_xpath_query("xml/output.xml","//item[transmission='Manual']", "manual_transmission.xml" )
xml_xpath_query("xml/output.xml","//item[transmission='Automatic']", "automatic_transmission.xml" )

#Split by owner ammount
xml_xpath_query("xml/output.xml","//item[owner='First Owner']", "first_owner.xml" )
xml_xpath_query("xml/output.xml","//item[owner='Second Owner']", "second_owner.xml" )
xml_xpath_query("xml/output.xml","//item[owner='Third Owner']", "third_owner.xml" )
xml_xpath_query("xml/output.xml","//item[owner='Fourth & Above Owner']", "fourth_owner_&_above.xml" )
