import re
import os

def main():
    # Path to the regex file
    regex_file_path = '/root/regexes.txt'
    # Directory to be searched
    search_directory = '/root/project-folder'

    # Read regex patterns and names from the file
    with open(regex_file_path, 'r') as regex_file:
        regex_patterns = []
        for line in regex_file.readlines():
            match = re.search(r'^\s*([^:]+):\s*["\'](.*)["\']', line)
            if match:
                regex_name = match.group(1).strip()
                regex_pattern = match.group(2)
                regex_patterns.append((regex_name, regex_pattern))

    # Iterate over each regex pattern
    for regex_name, regex_pattern in regex_patterns:
        # Compile the regex pattern
        regex = re.compile(regex_pattern)

        # Iterate over all files recursively in the search directory
        for root, _, files in os.walk(search_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                # Read the file content in binary mode
                with open(file_path, 'rb') as search_file:
                    try:
                        # Decode the binary data using utf-8 encoding
                        file_contents = search_file.read().decode('utf-8')
                    except UnicodeDecodeError:
                        # If decoding using utf-8 fails, try decoding using latin-1 encoding
                        file_contents = search_file.read().decode('latin-1')

                # Search for matches in the file
                matches = regex.findall(file_contents)

                # Print the matches
                if matches:
                    print(f"{regex_name} = {matches[0]}  ---> found in {file_path}.")

if __name__ == "__main__":
    main()
