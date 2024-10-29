import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='log_investigator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to investigate logs for injected queries
def investigate_logs():
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

        # Patterns indicating potential SQL injection
        injected_patterns = [
            "OR 1=1",
            "UNION SELECT",
            "DROP TABLE",
            "INSERT INTO",
            "xp_cmdshell",
            "admin' --",
            "' OR '1'='1"
        ]

        # Identify injected queries
        injected_queries = data[data['argument'].str.contains('|'.join(injected_patterns), case=False, na=False)]

        if not injected_queries.empty:
            logging.warning("Injected SQL queries detected:")
            for _, row in injected_queries.iterrows():
                logging.warning(f"Time: {row['event_time']}, User: {row['user_host']}, Query: {row['argument']}")
                print(f"Injected query detected: Time: {row['event_time']}, User: {row['user_host']}, Query: {row['argument']}")
    except Exception as e:
        logging.error(f"Error occurred while investigating logs for injected queries: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    investigate_logs()
