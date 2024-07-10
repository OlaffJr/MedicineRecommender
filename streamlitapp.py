import streamlit as st
import requests

# Backend URL
backend_url = 'http://localhost:5000/medicines'

st.title("Medicine Finder")

# Input for disease name
disease_name = st.text_input("Enter the disease name:")

if st.button("Search"):
    if disease_name:
        # Fetch medicines for the given disease
        response = requests.get(f"{backend_url}/{disease_name}")
        if response.status_code == 200:
            medicines = response.json()
            if medicines:
                for medicine in medicines:
                    st.subheader(medicine['medicine_name'])
                    st.write(f"Price: {medicine.get('price', 'N/A')}")
                    st.write(f"Disease Name: {medicine.get('disease_name', 'N/A')}")

                    st.write("Description:")
                    st.write(medicine.get('description', 'Description not available'))

                    st.write("Directions for Use:")
                    st.write(medicine.get('directions', 'Directions not available'))

                    st.write("Side Effects:")
                    st.write(medicine.get('side_effects', 'Side effects not available'))
            else:
                st.write("No medicines found for the given disease.")
        else:
            st.write("Error fetching data from the backend.")
    else:
        st.write("Please enter a disease name to search.")

# Run the Streamlit app using the command:
# streamlit run streamlit_app.py
