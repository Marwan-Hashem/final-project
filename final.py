import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Database Connection
def connect_to_db():
    return sqlite3.connect('ecsel_database.db')

# Query to extract countries
def get_countries(conn):
    query = "SELECT DISTINCT Acronym, Country FROM Countries ORDER BY Country"
    return pd.read_sql(query, conn)

# Query to get participants data
def get_participants_data(conn, country_acronym):
    query = f"""
    SELECT p.shortName, p.name, p.activityType, p.organizationURL, SUM(p.ecContribution) AS TotalECContribution
    FROM Participants p
    WHERE p.country = '{country_acronym}'
    GROUP BY p.shortName, p.name, p.activityType, p.organizationURL
    ORDER BY SUM(p.ecContribution) DESC
    """
    return pd.read_sql(query, conn)

# Query to get project coordinators data
def get_coordinators_data(conn, country_acronym):
    query = f"""
    SELECT p.shortName, p.name, p.activityType, p.projectAcronym
    FROM Participants p
    WHERE p.role = 'coordinator' AND p.country = '{country_acronym}'
    ORDER BY p.shortName ASC
    """
    return pd.read_sql(query, conn)

# Query for graph data
def get_graph_data(conn, country_acronym):
    query = f"""
    SELECT pr.year, p.activityType, SUM(p.ecContribution) AS TotalECContribution
    FROM Participants p
    JOIN Proposal pr ON p.projectID = pr.projectID
    WHERE p.country = '{country_acronym}'
    GROUP BY pr.year, p.activityType
    ORDER BY pr.year
    """
    return pd.read_sql(query, conn)

# Streamlit UI
def main():
    conn = connect_to_db()
    
    st.title('Ecsel Project Data Explorer')
    
    countries_df = get_countries(conn)
    country_list = countries_df['Country'].tolist()
    
    selected_country = st.selectbox("Select a Country:", country_list)
    
    if selected_country:
        country_acronym = countries_df[countries_df['Country'] == selected_country]['Acronym'].values[0]
        
        participants_data = get_participants_data(conn, country_acronym)
        coordinators_data = get_coordinators_data(conn, country_acronym)
        graph_data = get_graph_data(conn, country_acronym)
        
        st.subheader("Participants Data")
        st.write(participants_data)
        
        st.subheader("Project Coordinators Data")
        st.write(coordinators_data)

        # Plotting the graph
        if not graph_data.empty:
            fig = px.bar(graph_data, x='year', y='TotalECContribution', color='activityType',
                         title=f'Received Grants by Activity Type in {selected_country}')
            st.plotly_chart(fig, use_container_width=True)
        
        # CSV Download
        st.download_button("Download Participants Data", participants_data.to_csv(), file_name=f"{selected_country}_participants.csv")
        st.download_button("Download Coordinators Data", coordinators_data.to_csv(), file_name=f"{selected_country}_coordinators.csv")

if __name__ == "__main__":
    main()
