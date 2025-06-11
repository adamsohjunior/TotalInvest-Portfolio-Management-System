import pyodbc

server = 'localhost,1433'  # Change to your server's address
database = 'sc2207'  # Your database name
username = 'sa'
password = '84taNDcq@dLYwyd'  # Replace with your actual password

# Set up the connection string
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect to SQL Server
conn = pyodbc.connect(conn_str)
conn.autocommit = True

cursor = conn.cursor()