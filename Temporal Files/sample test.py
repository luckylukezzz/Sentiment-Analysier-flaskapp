import re
import ast
import json


def extract_alphanumeric_with_hyphens(data):
    # To store results for each item
    results = []

    # Use regex to capture alphanumeric words or phrases that may contain spaces and hyphens
    pattern = r'[\w.-]+(?:\s+[\w.-]+)*'

    # Iterate over each item in the data list
    for item in data:
        text = item[1]

        if text is None:
            results.append((item[0], []))
        else:
            # Find all matching patterns
            matches = re.findall(pattern, text)

            # Clean up the results by stripping extra spaces
            cleaned_matches = [match.strip() for match in matches if match.strip()]

            # Append the item ID and the cleaned matches to results
            results.append((item[0], cleaned_matches))

    aspects_only = [aspects for _, aspects in results if aspects]

    return flatten_nested_list(aspects_only)

def flatten_nested_list(nested_list):

  flattened_list = []
  for item in nested_list:
    if isinstance(item, list):
      flattened_list.extend(flatten_nested_list(item))
    else:
      flattened_list.append(item)
  return flattened_list

# Example usage
data = [('B004YRBM1Q',
         '[\'[\\\'[\\\\\\\'["[\\\\\\\\\\\\\\\'[]\\\\\\\\\\\\\\\']"]\\\\\\\']\\\']\', \'iOS 7.2\', \'Flip Phone\', \'Android 8.1\']'),
        ('B00NPY1G56', None), ('B07759SBP7',
                               '[\' \\\' \\\\\\\'[\\\\\\\\\\\\\\\' \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\' "[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'[]\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'\\\\\\\\\\\\\\\'\\\\\\\']\\\']\', \' \\\' \\\\\\\' \\\\\\\\\\\\\\\' " \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'T-Mobile\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\']"\\\\\\\\\\\\\\\'\\\\\\\'\\\'\', \' \\\' \\\\\\\' \\\\\\\\\\\\\\\' \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\' " \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'Screen Delay\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'\\\\\\\\\\\\\\\'\\\\\\\'\\\'\', \'[\\\' \\\\\\\' \\\\\\\\\\\\\\\' \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'[" \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'iPhone\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\']\\\\\\\\\\\\\\\'\\\\\\\'\\\'\', \' \\\'[\\\\\\\' \\\\\\\\\\\\\\\'[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\' " \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'Call Mute\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\']"\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\'\\\\\\\\\\\\\\\']\\\\\\\'\\\'\']'),
        ('B078P38R8L', "['[]']")]

extracted_data = extract_alphanumeric_with_hyphens(data)
print(extracted_data)
# negative_aspects = [sublist for sublist in extracted_data if sublist]
# print(negative_aspects)

