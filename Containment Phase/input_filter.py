import re
import logging

# Configure logging
logging.basicConfig(filename='input_filter.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to sanitize user inputs
def sanitize_input(user_input):
    try:
        # Remove potentially malicious SQL keywords
        sanitized_input = re.sub(r"(?i)(SELECT|INSERT|DELETE|UPDATE|DROP|UNION|OR 1=1|--|#|;|\*|\")", "", user_input)
        logging.info(f"Sanitized user input: {sanitized_input}")
        return sanitized_input
    except Exception as e:
        logging.error(f"Error occurred while sanitizing input: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Example user input to sanitize
        user_input = "SELECT * FROM users WHERE username='admin' OR 1=1; --"
        sanitized_output = sanitize_input(user_input)
        print(f"Sanitized Output: {sanitized_output}")
    except Exception as e:
        print(f"Error: {str(e)}")
