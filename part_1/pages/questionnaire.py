import streamlit as st

st.title("Question Answer Model Using GPT-3.5 Turbo")

# Create a dropdown box with a list of options
selected_option1 = st.selectbox("Select an option:", ["Option 1", "Option 2", "Option 3"], key = "selected_option1")


# Display the selected option
st.write("Selected Form:", selected_option1)

st.button("Transcribe Text")


selected_option2 = st.selectbox("Select a default question:", ["Option 1", "Option 2", "Option 3"], key = "selected_option2")
st.write("Selected question", selected_option2)



