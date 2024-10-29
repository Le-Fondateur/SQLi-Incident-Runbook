import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='query_pattern_analyzer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to analyze query access patterns
def analyze_query_patterns():
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

        # Analyze user access patterns for anomalies
        query_counts = data.groupby(['user_host']).size().reset_index(name='query_count')
        avg_queries = query_counts['query_count'].mean()
        threshold = avg_queries * 2  # Example threshold for anomaly detection

        # Identify users with abnormal query counts
        anomalous_users = query_counts[query_counts['query_count'] > threshold]

        if not anomalous_users.empty:
            logging.warning("Anomalous query patterns detected:")
            for _, row in anomalous_users.iterrows():
                logging.warning(f"User: {row['user_host']}, Query Count: {row['query_count']}")
                print(f"Anomalous query pattern detected: User: {row['user_host']}, Query Count: {row['query_count']}")
    except Exception as e:
        logging.error(f"Error occurred while analyzing query patterns: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    analyze_query_patterns()
