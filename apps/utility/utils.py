from datetime import datetime
import re
# common functions used by various apps
def convert_date(date_str):
    if date_str is None:
        return None
        # Define input and output formats
    input_formats = ["%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S.%f%z"]
    output_format = "%d %b %Y"
    # If the input is already a datetime object, use it directly
    if isinstance(date_str, datetime):
        parsed_date = date_str
    else:
        # Try parsing the input date using each format
        for format_str in input_formats:
            try:
                parsed_date = datetime.strptime(date_str, format_str)
                # If parsing is successful, break out of the loop
                break
            except ValueError:
                pass
        else:
            # If none of the formats work, raise an error
            raise ValueError("Invalid date format")

    # Format the date in the desired output format
    formatted_date = parsed_date.strftime(output_format)

    return formatted_date


# Function to extract product and capability
def get_productCapability(json_data):
    #json_data = json.loads(json_data)
    capability = None
    product_version = None
    product_name = None
    frequency = None

    for content_item in json_data.get("content", []):
        if content_item.get("type") == "paragraph":
            
            text_items = [item.get("text", "") for item in content_item.get("content", [])]
            for i in range(len(text_items)):
                line = text_items[i].strip()

                if line.lower().startswith("primary industry:"):
                    capability = line.split(":")[1].strip()

                if line.lower().startswith("product:"):
                    product_line = line.split(":")[1].strip()
                    if i + 1 < len(text_items) and not text_items[i + 1].strip().lower().startswith("current software version:"):
                        product_parts = product_line.split()
                        #product_name = product_line if not any(part.replace('.', '', 1).isdigit() for part in product_parts) else " ".join(product_parts[:-1])
                        product_name = product_line
                        product_version = next((part for part in product_parts if part.replace('.', '', 1).isdigit()), "NA")
                    else:
                        product_name = product_line
                        product_version = "NA"

                if line.lower().startswith("frequency:"):
                    frequency = line.split(":")[1].strip()
    
    return capability, product_name, product_version, frequency    
# function to get subtasks list
def extract_subtasks_data(subtasks):
    # Check if "subtasks" is not empty
    if subtasks:
        # Extracting key and summary of subtasks
        subtasks_data = []
        for subtask in subtasks:
            subtask_data = {
                "key": subtask.get("key", ""),
                "summary": subtask.get("fields", {}).get("summary", "")
            }
            subtasks_data.append(subtask_data)
        return subtasks_data
    else:
        return []


# Function to find the menu id and partner from activity short menu
""" def find_menuid_in_string(match_str,menuList):
    if match_str:
        matching_values = [menu_item for menu_item in menuList if menu_item in match_str]
        longest_matching_value = ''
        p_is_after_match = ''
        longest_matching_value = max(matching_values, key=len, default=None)

        if longest_matching_value is not None:
            index_of_match = match_str.find(longest_matching_value)
            p_is_after_match = (
                                    index_of_match + len(longest_matching_value) < len(match_str)) and (
                                    match_str[index_of_match + len(longest_matching_value)] == 'P')
            return longest_matching_value, p_is_after_match
        return None, False
    else:
        return None, False """
# getting menu card and partner by given string
def find_menuid_in_string(match_str,menuList):
    if match_str:
        match_str = match_str.strip()  # Trim leading and trailing whitespace
        tokens = re.findall(r'(?:QSM|SAA|EMA|TAA)\d+', match_str)  # Extract tokens starting with series prefixes followed by digits
        for token in tokens:
            if token in menuList:
                index_of_match = match_str.find(token)
                if index_of_match != -1:  # Check if token is found in match_str
                    is_p_after_match = (index_of_match + len(token) < len(match_str)) and (match_str[index_of_match + len(token)] == 'P')
                    return token, is_p_after_match
    return None, False
