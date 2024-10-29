import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='error_message_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to detect repeated SQL error messages
def detect_repeated_errors():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URI)

        # Query to fetch database error logs
        query = """
        SELECT event_time, user_host, argument
        FROM mysql.general_log
        WHERE argument LIKE '%error%'
        """

        # Load data from database
        data = pd.read_sql(query, engine)

        # Identify repeated error messages
        repeated_errors = data['argument'].value_counts().reset_index()
        repeated_errors.columns = ['error_message', 'count']
        repeated_errors = repeated_errors[repeated_errors['count'] > 1]

        if not repeated_errors.empty:
            logging.warning("Repeated SQL error messages detected:")
            for _, row in repeated_errors.iterrows():
                logging.warning(f"Error Message: {row['error_message']}, Count: {row['count']}")
                print(f"Repeated error detected: Error Message: {row['error_message']}, Count: {row['count']}")
    except Exception as e:
        logging.error(f"Error occurred while detecting repeated SQL error messages: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    detect_repeated_errors()
