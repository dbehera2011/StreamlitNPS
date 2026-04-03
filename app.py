import streamlit as st

st.title("Hello Streamlit!")
st.write("This is my first app 🎉")

number = st.slider("Pick a number", 0, 100)
st.write("You selected:", number)