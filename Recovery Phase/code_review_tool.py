import re
import logging
import os

# Configure logging
logging.basicConfig(filename='code_review_tool.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Directory containing code files to review
CODE_DIRECTORY = "./application_code"

# Function to perform code review for SQL vulnerabilities
def review_code_for_sql_vulnerabilities(directory):
    try:
        # Patterns indicating potential SQL vulnerabilities
        sql_patterns = [
            r"(?i)(SELECT .* FROM .* WHERE .* OR 1=1)",
            r"(?i)(DROP TABLE)",
            r"(?i)(INSERT INTO)",
            r"(?i)(UNION SELECT)",
            r"(?i)(DELETE FROM)",
            r"(?i)(UPDATE .* SET .* WHERE)"
        ]

        # Iterate over files in the code directory
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") or file.endswith(".sql"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        for pattern in sql_patterns:
                            if re.search(pattern, content):
                                logging.warning(f"Potential SQL vulnerability found in {file_path} with pattern: {pattern}")
                                print(f"Potential SQL vulnerability found in {file_path} with pattern: {pattern}")
    except Exception as e:
        logging.error(f"Error occurred during code review: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        review_code_for_sql_vulnerabilities(CODE_DIRECTORY)
    except Exception as e:
        print(f"Error: {str(e)}")
