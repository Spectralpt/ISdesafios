import pandas as pd
from lxml import etree
import os

# Define XML directory
xml_base_dir = "./xml/"

# Function to validate XML against a schema
def validate(xmlTree):
    try:
        xmlschema = etree.XMLSchema(etree.parse("xml/output.xsd"))
        return xmlschema.validate(xmlTree)
    except (etree.XMLSyntaxError, etree.DocumentInvalid) as e:
        print(f"Schema validation error: {e}")
        return False

# Function to convert CSV to XML
def csv_to_xml(filepath):
    root = etree.Element("root")
    try:
        df = pd.read_csv(filepath, sep=',')
    except FileNotFoundError:
        print(f"CSV file not found at {filepath}.")
        return
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV: {e}")
        return

    for _, row in df.iterrows():
        item = etree.SubElement(root, "item")
        for col in df.columns:
            col_element = etree.SubElement(item, col.replace(' ', "_"))
            col_element.text = str(row[col])

    tree = etree.ElementTree(root)

    # Validate the generated XML
    if validate(tree):
        print(f"Base XML is valid")
        with open(os.path.join(xml_base_dir, "car.xml"), "wb") as xmlFile:
            tree.write(xmlFile, pretty_print=True)
    else:
        print(f"Base XML is invalid")

# Function to query and generate sub-XMLs
def xml_xpath_query(filepath, query, filename):
    try:
        tree = etree.parse(filepath)
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return

    try:
        products = tree.xpath(query)
    except etree.XPathEvalError as e:
        print(f"Error in XPath query: {e}")
        return

    subxml_root = etree.Element("filtered_catalog")

    for product in products:
        subxml_root.append(product)
    
    subxml_str = etree.tostring(subxml_root, pretty_print=True)

    if validate(tree):
        print(f"{filename} is valid")
        with open(xml_base_dir + filename, "wb") as f:
            f.write(etree.tostring(subxml_root, pretty_print=True))
    else:
        print(f"{filename} is invalid")

# Function to display search menu
def display_menu():
    print("Select an option to search in the XML files:")
    print("1. Search by seller type")
    print("2. Search by fuel type")
    print("3. Search by transmission type")
    print("4. Search by owner amount")
    print("5. Search by year")
    print("6. Validate all XMLs")
    print("7. Search by XPath")
    print("9. Exit")
    return input("Enter your choice: ")

# Function to search XML using XPath
def search_xml(file, xpath_query):
    try:
        tree = etree.parse(file)
        return tree.xpath(xpath_query)
    except FileNotFoundError:
        print(f"File {file} not found.")
        return []
    except etree.XPathEvalError as e:
        print(f"Error in XPath query: {e}")
        return []
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return []

# Function to format and display search results
def format_results(results):
    if not results:
        print("No results found.")
        return
    for result in results:
        print("Item:")
        for element in result:
            print(f"{element.tag}: {element.text}")
        print("++++++++++++++++++++++++++++++++++++")

# Clear screen for better user experience
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main function for user interaction
def main():
    clear_screen()
    while True:
        choice = display_menu()
        if choice == '1':
            try:
                clear_screen()
                seller_type = input("Enter seller type (Individual/Dealer): ").capitalize()
                file = f"xml/{'individual' if seller_type == 'Individual' else 'dealership'}.xml"
                results = search_xml(file, f"//item[seller_type='{seller_type}']")
                format_results(results)
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '2':
            try:
                clear_screen()
                fuel_type = input("Enter fuel type (Diesel/Petrol/Electric): ").capitalize()
                file = f"xml/{fuel_type.lower()}.xml"
                results = search_xml(file, f"//item[fuel='{fuel_type}']")
                format_results(results)
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '3':
            try:
                clear_screen()
                transmission_type = input("Enter transmission type (Manual/Automatic): ").capitalize()
                file = f"xml/{'manual_transmission' if transmission_type == 'Manual' else 'automatic_transmission'}.xml"
                results = search_xml(file, f"//item[transmission='{transmission_type}']")
                format_results(results)
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '4':
            try:
                clear_screen()
                owner_amount = input("Enter owner amount (First Owner/Second Owner/Third Owner/Fourth Owner & Above): ")
                owner_amount = owner_amount.lower().replace(' ', '_')
                file = f"xml/{owner_amount}.xml"
                results = search_xml(file, f"//item[owner='{owner_amount.replace('_', ' ').title()}']")
                format_results(results)
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '5':
            try:
                clear_screen()
                year = input("Enter year: ")
                file = "xml/car.xml"
                results = search_xml(file, f"//item[year='{year}']")
                format_results(results)
                xml_xpath_query("xml/car.xml", f"//item[year='{year}']", f"year_{year}.xml")
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '6':
            try:
                clear_screen()
                for file in os.listdir(xml_base_dir):
                    if file.endswith(".xml"):
                        if validate(etree.parse(xml_base_dir + file)):
                            print(f"{file} is valid")
                        else:
                            print(f"{file} is invalid")
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '7':
            try:
                clear_screen()
                print("Available categories: ")
                for element in etree.parse("xml/car.xml").getroot()[0]:
                    print(element.tag)
                xpath = input("Enter XPath query (e.g., //item[transmission='Automatic']): ")
                results = search_xml(f"xml/car.xml", xpath)
                format_results(results)
                input("Press Enter to continue...")
                clear_screen()
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")
                clear_screen()
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")
            clear_screen()

# CSV to XML Conversion
csv_to_xml("csv/car.csv")

# Generate sub-XML files
xml_xpath_query("xml/car.xml", "//item[seller_type='Individual']", "individual.xml")
xml_xpath_query("xml/car.xml", "//item[seller_type='Dealer']", "dealership.xml")
xml_xpath_query("xml/car.xml", "//item[fuel='Diesel']", "diesel.xml")
xml_xpath_query("xml/car.xml", "//item[fuel='Petrol']", "petrol.xml")
xml_xpath_query("xml/car.xml", "//item[fuel='Electric']", "electric.xml")
xml_xpath_query("xml/car.xml", "//item[transmission='Manual']", "manual_transmission.xml")
xml_xpath_query("xml/car.xml", "//item[transmission='Automatic']", "automatic_transmission.xml")
xml_xpath_query("xml/car.xml", "//item[owner='First Owner']", "first_owner.xml")
xml_xpath_query("xml/car.xml", "//item[owner='Second Owner']", "second_owner.xml")
xml_xpath_query("xml/car.xml", "//item[owner='Third Owner']", "third_owner.xml")
xml_xpath_query("xml/car.xml", "//item[owner='Fourth & Above Owner']", "fourth_&_above_owner.xml")

# Start the main menu loop
if __name__ == "__main__":
    main()

