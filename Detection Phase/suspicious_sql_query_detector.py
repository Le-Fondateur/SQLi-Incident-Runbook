import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='suspicious_sql_query_detector.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to detect suspicious SQL queries
def detect_suspicious_queries():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URI)

        # Query to fetch database activity logs
        query = """
        SELECT event_time, user_host, argument
        FROM mysql.general_log
        WHERE command_type = 'Query'
        """

        # Load data from database
        data = pd.read_sql(query, engine)

        # Patterns indicating possible SQL injection
        suspicious_patterns = [
            "OR 1=1",
            "UNION SELECT",
            "--",
            "/*",
            "DROP TABLE",
            "INSERT INTO",
            "xp_cmdshell"
        ]

        # Identify suspicious SQL queries
        suspicious_queries = data[data['argument'].str.contains('|'.join(suspicious_patterns), case=False, na=False)]

        if not suspicious_queries.empty:
            logging.warning("Suspicious SQL queries detected:")
            for _, row in suspicious_queries.iterrows():
                logging.warning(f"Time: {row['event_time']}, User: {row['user_host']}, Query: {row['argument']}")
                print(f"Suspicious query detected: Time: {row['event_time']}, User: {row['user_host']}, Query: {row['argument']}")
    except Exception as e:
        logging.error(f"Error occurred while detecting suspicious SQL queries: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    detect_suspicious_queries()
