import psycopg2

hostname = 'localhost'
database = 'Mashroom'
username = 'postgres'
pwd = 'root'
port_id = 5432

try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    
    # Create a cursor to execute queries
    cur = conn.cursor()
    
    # Example query
    cur.execute("SELECT version();")
    print(cur.fetchone())
    
    # Close cursor and connection
    cur.close()
    conn.close()
    
except Exception as error:
    print(f"Error: {error}")