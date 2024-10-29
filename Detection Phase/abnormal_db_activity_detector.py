import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='abnormal_db_activity_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to detect abnormal database activities
def detect_abnormal_activity():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URI)

        # Query to fetch database activity logs
        query = """
        SELECT event_time, user_host, command_type, argument
        FROM mysql.general_log
        WHERE command_type IN ('Query', 'Execute')
        """

        # Load data from database
        data = pd.read_sql(query, engine)

        # Identify abnormal activities (e.g., high frequency of DELETE, UPDATE operations)
        suspicious_commands = data[data['command_type'].isin(['DELETE', 'UPDATE'])]
        if not suspicious_commands.empty:
            logging.warning("Abnormal database activities detected:")
            for _, row in suspicious_commands.iterrows():
                logging.warning(f"Time: {row['event_time']}, User: {row['user_host']}, Command: {row['command_type']}")
                print(f"Abnormal activity detected: Time: {row['event_time']}, User: {row['user_host']}, Command: {row['command_type']}")
    except Exception as e:
        logging.error(f"Error occurred while detecting abnormal database activities: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    detect_abnormal_activity()
