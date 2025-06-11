import os
from cursor import cursor, conn

OUTPUT_FILE = "seed.sql"

def dump_table(table_name, file):    
    """Dump table data as INSERT statements."""
    cursor.execute(f"SELECT * FROM [{table_name}]")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    
    if not rows:
        return

    with open(file, "a", encoding="utf-8") as f:
        f.write(f"-- Dumping data for table [{table_name}]\n")
        for row in rows:
            values = ", ".join(
                f"'{str(value).replace("'", "''")}'" if value is not None else "NULL"
                for value in row
            )
            sql = f"INSERT INTO [{table_name}] ({', '.join(columns)}) VALUES ({values});\n"
            f.write(sql)
        f.write("\n")

def dump_database():
    """Dump the entire database into an SQL file."""
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    for table in ["Asset", "Stock", "Bond", "Fund", "AssetPrice", 
                  "Investor", "Financial_Goal", "Portfolio", 
                  "Investor_Record", "Asset_Allocation", 
                  "Invested_Value", "Unrealised_Gain_Loss", 
                  "PTransaction", "Owned_Assets", "Bought_Asset_From"]:
        dump_table(table, OUTPUT_FILE)

    print(f"Database dumped to {OUTPUT_FILE}")

if __name__ == "__main__":
    dump_database()