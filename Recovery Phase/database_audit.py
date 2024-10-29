import pandas as pd
import logging
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(filename='database_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'

# Function to audit the database and restore integrity
def audit_database():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URI)

        # Example query to identify suspicious changes in the database
        audit_query = """
        SELECT table_name, operation, timestamp, user_host
        FROM mysql.audit_log
        WHERE operation IN ('DELETE', 'UPDATE', 'DROP')
        """

        # Load data from database
        audit_data = pd.read_sql(audit_query, engine)

        # Log suspicious activities
        if not audit_data.empty:
            logging.warning("Suspicious database operations detected:")
            for _, row in audit_data.iterrows():
                logging.warning(f"Table: {row['table_name']}, Operation: {row['operation']}, Time: {row['timestamp']}, User: {row['user_host']}")
                print(f"Suspicious operation detected: Table: {row['table_name']}, Operation: {row['operation']}, Time: {row['timestamp']}, User: {row['user_host']}")
        else:
            logging.info("No suspicious database operations detected.")
            print("No suspicious database operations detected.")
    except Exception as e:
        logging.error(f"Error occurred during database audit: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    audit_database()
    