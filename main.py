import streamlit as st
import pandas as pd
import io

# --- Login System Configuration ---
# You can add up to 10 user logins here
LOGIN_CREDENTIALS = {
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

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Data Filter App")

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Data Loading (Cached) ---
@st.cache_data
def load_data():
    """
    Loads data from the specified GitHub CSV URL.
    This function is cached to prevent re-downloading on every rerun.
    """
    try:
        # Replaced the URL with the correct raw GitHub URL
        url = "https://raw.githubusercontent.com/shanidevani/service-price/755bea969d9894fda6e06481c039e2496ff94c0d/service%20data.csv"
        # Added on_bad_lines='skip' to handle malformed rows
        df = pd.read_csv(url, on_bad_lines='skip')
        # Rename columns to match the request
        df.columns = ['CODE', 'CODE DESC.', 'Serviço', 'GRUP', 'SHORT', 'QS COD', 'PART CODE', 'PRICE', 'DURACAO', 'Descrição']
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}. Please check the CSV URL and its formatting.")
        return None

# --- Main Application Logic ---
def show_login_page():
    """
    Displays the login form.
    """
    st.title("Login to Access the Data")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
    if submit_button:
        if username in LOGIN_CREDENTIALS and LOGIN_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def show_main_app():
    """
    Displays the main application with filters and data table.
    """
    st.title("Mechanic Data Viewer")
    
    df = load_data()
    if df is None:
        return # Stop execution if data loading failed

    # Create two columns for the filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Get unique values for the "CODE DESC." dropdown
        code_desc_options = df['CODE DESC.'].unique().tolist()
        selected_code_desc = st.selectbox(
            "Filter by Car Type",
            ["All"] + code_desc_options
        )
    
    with col2:
        # Get unique values for the "Serviço" dropdown
        servico_options = df['Serviço'].unique().tolist()
        selected_servico = st.selectbox(
            "Filter by Service",
            ["All"] + servico_options
        )

    # Filter the DataFrame based on selections
    filtered_df = df.copy()
    if selected_code_desc != "All":
        filtered_df = filtered_df[filtered_df['CODE DESC.'] == selected_code_desc]
    
    if selected_servico != "All":
        filtered_df = filtered_df[filtered_df['Serviço'] == selected_servico]
    
    # Select and display the required columns
    display_df = filtered_df[['PART CODE', 'PRICE', 'DURACAO']]
    st.dataframe(display_df, use_container_width=True)
    
    # --- Logout button at the bottom ---
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- Run the appropriate page based on login status ---
if st.session_state.logged_in:
    show_main_app()
else:
    show_login_page()

