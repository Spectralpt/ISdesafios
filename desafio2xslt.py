from lxml import etree

xml_tree = etree.parse("./xml/output.xml")

diesel_xslt_tree = etree.parse("diesel.xslt")
diesel_transform = etree.XSLT(diesel_xslt_tree)
diesel_result_tree = diesel_transform(xml_tree)

with open("test.xml", "wb") as f:
    f.write(etree.tostring(diesel_result_tree, pretty_print=True))
