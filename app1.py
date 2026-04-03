import streamlit as st
import pandas as pd

st.title("My First Streamlit App")

# User input
name = st.text_input("Enter your name:")
st.write(f"Hello, {name}!")

# Display a dataframe
data = pd.DataFrame({
    "Numbers": [1, 2, 3, 4],
    "Squares": [1, 4, 9, 16]
})
st.write(data)