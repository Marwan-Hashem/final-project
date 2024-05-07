import sqlite3
import pandas as pd

def read_excel_to_df(filepath):
    """Reads an Excel file into a DataFrame."""
    return pd.read_excel(filepath)

def create_database(db_name):
    """Creates and connects to an SQLite database."""
    conn = sqlite3.connect(db_name)
    return conn

def insert_data(conn, df, table_name):
    """Inserts DataFrame data into the specified SQLite table."""
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def main():
    # Define paths to Excel files
    proposal_file = 'projects.xlsx'
    participants_file = 'participants.xlsx'
    countries_file = 'countries.xlsx'

    # Read Excel files into DataFrames
    df_proposal = read_excel_to_df(proposal_file)
    df_participants = read_excel_to_df(participants_file)
    df_countries = read_excel_to_df(countries_file)
    
    # Create or connect to the SQLite database
    conn = create_database('ecsel_database.db')

    # Insert data into the database (this will also create tables if they don't exist)
    insert_data(conn, df_proposal, 'Proposal')
    insert_data(conn, df_participants, 'Participants')
    insert_data(conn, df_countries, 'Countries')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()