import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time

st.markdown("""
<style>
.big-font {
    font-size: 30px !important;
    color: #1f77b4;
}
.custom-btn {
    background-color: #1f77b4;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 5px;
}
.custom-btn:hover {
    background-color: #0f4c81;
}
.stButton>button {
    background-color: #1f77b4;
    color: white;
}
.stButton>button:hover {
    background-color: #0f4c81;
}
.stExpander>div {
    border: 1px solid #1f77b4;
    border-radius: 5px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_name = "gpt2-medium"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

pipe = load_model()

st.title("AI-Powered Event Organizer")
st.markdown('<p class="big-font">Organize Your Event with Ease!</p>', unsafe_allow_html=True)

st.subheader("Enter event details:")

event_type = st.selectbox(
    "Select event type:",
    ["Wedding", "Conference", "Birthday Party", "Dance", "Other"]
)

with st.expander("Event Details"):
    if event_type == "Wedding":
        guests = st.slider("How many guests?", 50, 1000, 300)
        theme = st.selectbox("Select theme:", ["Pakistani", "Modern", "Classic", "Vintage"])
        budget = st.number_input("Enter your budget (USD):", min_value=1000, value=60000)

    elif event_type == "Conference":
        attendees = st.slider("Number of attendees?", 10, 500, 100)
        industry = st.selectbox("Select industry type:", ["Tech", "Finance", "Healthcare", "Education"])
        budget = st.number_input("Enter your budget (USD):", min_value=1000, value=20000)

    elif event_type == "Birthday Party":
        age_group = st.selectbox("Select age group:", ["Kids", "Teens", "Adults"])
        guests = st.slider("How many guests?", 10, 100, 50)
        budget = st.number_input("Enter your budget (USD):", min_value=100, value=1000)

    elif event_type == "Dance":
        theme = st.text_input("Enter the theme of the dance:")
        guests = st.slider("How many guests?", 50, 500, 150)
        budget = st.number_input("Enter your budget (USD):", min_value=1000, value=5000)

    else:
        custom_event = st.text_input("Describe your event:")
        budget = st.number_input("Enter your budget (USD):", min_value=500, value=1000)

if st.button("Get AI Suggestions", key="suggestions", help="Get suggestions from AI", use_container_width=True):
    user_input = (
        f"Organizing a {event_type} with a budget of ${budget}. "
        "Provide a comprehensive plan including suggestions for venues, themes, vendors, "
        "and any other useful advice. Consider these specifics: "
    )

    if event_type == "Wedding":
        user_input += f"Wedding theme: {theme}, Number of guests: {guests}."
    elif event_type == "Conference":
        user_input += f"Industry type: {industry}, Number of attendees: {attendees}."
    elif event_type == "Birthday Party":
        user_input += f"Age group: {age_group}, Number of guests: {guests}."
    elif event_type == "Dance":
        user_input += f"Dance theme: {theme}, Number of guests: {guests}."
    else:
        user_input += f"Event description: {custom_event}."

    user_input += " Provide a detailed response with actionable insights and recommendations. "
    user_input += "Include advice on how to manage the event, potential challenges, and tips for a successful outcome."

    start_time = time.time()
    response = pipe(user_input, max_length=800, num_return_sequences=1)
    ai_response = response[0]["generated_text"]
    st.write(f"Time taken for response: {time.time() - start_time:.2f} seconds")

    def format_response(text):
        lines = text.split('\n')
        formatted_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(formatted_lines)

    formatted_response = format_response(ai_response)
    st.subheader("AI Response")
    st.write(formatted_response)

if st.button("Other useful advice"):
    st.write("Remember to book the venue early and ensure catering is within budget!")
