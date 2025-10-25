# import psycopg2
# import pandas as pd
# from config import DB_CONFIG

# def get_db_connection():
#     """Create and return database connection"""
#     try:
#         conn = psycopg2.connect(
#             host=DB_CONFIG['localhost'],
#             database=DB_CONFIG['Mashroom'],
#             user=DB_CONFIG['postgres'],
#             password=DB_CONFIG['root'],
#             port=DB_CONFIG['5432']
#         )
#         return conn
#     except psycopg2.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None

# def fetch_all_data(table_name):
#     """Fetch all data from a table"""
#     conn = get_db_connection()
#     if conn:
#         try:
#             df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
#             return df
#         except Exception as e:
#             print(f"Error fetching data: {e}")
#             return None
#         finally:
#             conn.close()
#     return None

# def fetch_custom_query(query):
#     """Execute custom SQL query"""
#     conn = get_db_connection()
#     if conn:
#         try:
#             df = pd.read_sql_query(query, conn)
#             return df
#         except Exception as e:
#             print(f"Error executing query: {e}")
#             return None
#         finally:
#             conn.close()
#     return None


import psycopg2
import pandas as pd
from typing import Optional

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'Mashroom',
    'user': 'postgres',
    'password': 'root',
    'port': 5432
}

def get_connection():
    """
    Establishes and returns a database connection.
    
    Returns:
        connection object or None if connection fails
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None

def fetch_all_data(table_name: str) -> Optional[pd.DataFrame]:
    """
    Fetches all data from the specified table and returns as a pandas DataFrame.
    
    Args:
        table_name: Name of the table to fetch data from
        
    Returns:
        pandas DataFrame with all data or None if fetch fails
    """
    conn = None
    cur = None
    
    try:
        # Establish connection
        conn = get_connection()
        if conn is None:
            return None
        
        # Create cursor
        cur = conn.cursor()
        
        # Execute query
        query = f"SELECT * FROM {table_name}"
        cur.execute(query)
        
        # Fetch all rows
        rows = cur.fetchall()
        
        # Get column names
        column_names = [desc[0] for desc in cur.description]
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=column_names)
        
        print(f"Successfully fetched {len(df)} rows from '{table_name}' table")
        return df
        
    except Exception as error:
        print(f"Error fetching data from {table_name}: {error}")
        return None
        
    finally:
        # Close cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

def fetch_filtered_data(table_name: str, condition: str) -> Optional[pd.DataFrame]:
    """
    Fetches filtered data from the specified table based on a WHERE condition.
    
    Args:
        table_name: Name of the table to fetch data from
        condition: SQL WHERE clause condition (without 'WHERE' keyword)
        
    Returns:
        pandas DataFrame with filtered data or None if fetch fails
        
    Example:
        fetch_filtered_data('details', "status = TRUE AND type = 1")
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        if conn is None:
            return None
        
        cur = conn.cursor()
        
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        cur.execute(query)
        
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=column_names)
        
        print(f"Successfully fetched {len(df)} rows from '{table_name}' with condition: {condition}")
        return df
        
    except Exception as error:
        print(f"Error fetching filtered data: {error}")
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def fetch_by_date_range(table_name: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    Fetches data from the table within a specific date range.
    
    Args:
        table_name: Name of the table to fetch data from
        start_date: Start date in 'YYYY-MM-DD' format
        end_date: End date in 'YYYY-MM-DD' format
        
    Returns:
        pandas DataFrame with filtered data or None if fetch fails
    """
    condition = f"date >= '{start_date}' AND date <= '{end_date}'"
    return fetch_filtered_data(table_name, condition)

def test_connection():
    """
    Tests the database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    conn = get_connection()
    if conn:
        print("Database connection successful!")
        conn.close()
        return True
    else:
        print("Database connection failed!")
        return False


# Example usage and testing
if __name__ == "__main__":
    # Test connection
    test_connection()
    
    # Fetch all data from details table
    print("\n--- Fetching all data ---")
    df = fetch_all_data('details')
    
    if df is not None:
        print("\nData preview:")
        print(df.head())
        print(f"\nData types:\n{df.dtypes}")
        print(f"\nData shape: {df.shape}")
    
    # Example: Fetch only active records
    print("\n--- Fetching filtered data (status = TRUE) ---")
    active_data = fetch_filtered_data('details', "status = TRUE")
    if active_data is not None:
        print(active_data)
    
    # Example: Fetch by date range
    print("\n--- Fetching by date range ---")
    date_filtered = fetch_by_date_range('details', '2025-10-01', '2025-10-31')
    if date_filtered is not None:
        print(date_filtered)