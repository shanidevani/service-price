import streamlit as st
import pandas as pd
import numpy as np

# --- Set wide page layout
st.set_page_config(layout="wide")

# --- User Authentication Configuration
# In a real-world app, you would use a proper database or a more secure
# method for user management. This is for demonstration purposes.
users = {
    "ARMMACHAWASASADMIN": "Smart@123456",
    "MATOLASASADMIN": "Smart@123456",
    "MATOLARIOSASADMIN": "Smart@123456",
    "MAPUTOSASADMIN": "Smart@123456",
    "CHOUPALSASADMIN": "Smart@123456",
    "MACHAWASASADMIN": "Smart@123456",
    "ARMBEIRASASADMIN": "Smart@123456",
    "BEIRASASADMIN": "Smart@123456",
    "NAMPULASASADMIN": "Smart@123456",
    "CHEMOIOSASADMIN": "Smart@123456",
}

def login_form():
    """Displays the login form and handles authentication."""
    with st.form("Login Form"):
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username in users and users[username] == password:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.rerun()  # Rerun the app to switch to the main page
            else:
                st.error("Invalid username or password.")

def logout_button():
    """Displays the logout button."""
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        del st.session_state['username']
        st.rerun()

# --- Main Application Logic
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    login_form()
else:
    # --- Data Loading (using st.cache_data for performance)
    @st.cache_data
    def load_data():
        """
        Loads the data from the raw CSV file on GitHub.
        """
        try:
            # Correct raw URL for the GitHub CSV file.
            # The URL was changed from the web page URL to the raw content URL.
            csv_url = "https://raw.githubusercontent.com/shanidevani/service-price/main/final%20service%20data.csv"
            df = pd.read_csv(csv_url)
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}. Please ensure the URL is correct and the CSV is publicly accessible.")
            return pd.DataFrame() # Return empty DataFrame on error

    df = load_data()

    if not df.empty:
        st.title(f"Welcome, {st.session_state['username']}!")
        st.header("Service Part Filter")
        st.write("Use the dropdowns below to filter the data.")

        # --- Filter Dropdowns with cascading logic
        col1, col2, col3, col4 = st.columns(4)
        
        # Step 1: Select Code Description
        with col1:
            code_desc_options = ['All'] + sorted(list(df['code desc.'].unique()))
            selected_code_desc = st.selectbox("Select Code Description", code_desc_options)

        # Create a filtered dataframe based on the first selection
        filtered_df_step1 = df.copy()
        if selected_code_desc != 'All':
            filtered_df_step1 = filtered_df_step1[filtered_df_step1['code desc.'] == selected_code_desc]
        
        # Step 2: Select Service (cascading from Code Description)
        with col2:
            service_options = ['All'] + sorted(list(filtered_df_step1['service'].unique()))
            selected_service = st.selectbox("Select Service", service_options)

        # Create a filtered dataframe based on the second selection
        filtered_df_step2 = filtered_df_step1.copy()
        if selected_service != 'All':
            filtered_df_step2 = filtered_df_step2[filtered_df_step2['service'] == selected_service]
        
        # Step 3: Select Make (cascading from Service)
        with col3:
            make_options = ['All'] + sorted(list(filtered_df_step2['make'].unique()))
            selected_make = st.selectbox("Select Make", make_options)
            
        # Create a filtered dataframe based on the third selection
        filtered_df_step3 = filtered_df_step2.copy()
        if selected_make != 'All':
            filtered_df_step3 = filtered_df_step3[filtered_df_step3['make'] == selected_make]

        # Step 4: Select Model Name (cascading from Make)
        with col4:
            model_name_options = ['All'] + sorted(list(filtered_df_step3['model name'].unique()))
            selected_model_name = st.selectbox("Select Model Name", model_name_options)
        
        # --- Final Filter the DataFrame
        filtered_df = filtered_df_step3.copy()
        if selected_model_name != 'All':
            filtered_df = filtered_df[filtered_df['model name'] == selected_model_name]
        
        # --- Display the results
        st.subheader("Filtered Results")
        
        # Before conversion, fill any NaN values in 'price' with 0
        # Then, convert the 'price' column to an integer to remove decimals
        filtered_df['price'] = filtered_df['price'].fillna(0).round(0).astype(int)

        # Display the required columns
        display_columns = ['part code', 'price', 'duracao', 'year start', 'description']
        st.dataframe(filtered_df[display_columns], use_container_width=True)

        st.markdown("---")
        # --- Logout button at the bottom of the page
        logout_button()
    else:
        st.info("The application could not load the data. Please check the CSV URL.")
