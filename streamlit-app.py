import streamlit as st
from ollama import Client
import json
client = Client(
  host='https://jz5hf1ica1zdsw-11434.proxy.runpod.net'
)
import random
import json
import time


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_event_query",
            "description": "Run this function when user asks to see some shows or events or something equivalent...",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "User's search query with extracted essential keywords."},
                    "date": {"type": "string", "description": "Preferred date or date range for the event."},
                    "price": {"type": "string", "description": "Preferred price range for the event."},
                    "location": {"type": "string", "description": "City of user."}
                },
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "SeeMoreShows",
            "description": "Triggered when the user wants to see more show options.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_show",
            "description": "Triggered when the user wants to book a show. Remember to understand context correctly.",
            "parameters": {
                "type": "object",
                "required": ["event_id", "event_name"],
                "properties": {
                    "event_id": {"type": "string", "description": "Unique event identifier"},
                    "event_name": {"type": "string", "description": "Name of the event"}
                },
                "additionalProperties": False
            }
        }
    }
]

sp2 = f"""[INST]
You're a chatbot concierge named Mochan-D, introducing yourself as a personal companion for discovering and booking events, shows and live concerts. Emphasize Mochan-D's ability to discover and book tickets and plan surprises for yourself or anyone whose ever is important or special in your life whether it is personal or official. Adapt to the user's persona, and always keep the conversation as human-like.

Your available functions:
- `search_event_query`: Search for events based on keywords, location, and date
- `SeeMoreShows`: Display additional event options when the user wants more choices
- `book_show`: Book tickets for a specific event using event_id and event_name


Example 1 - Initial Inquiry:
User: "Hi there, can you help me find some events?"
Response:
{{
  "content": "Hey! I'm Mochan-D, your personal event companion. What kind of events are you looking for?",
  "function_call": null
}}

Example 2 - Specific Search:
User: "Any comedy shows in Delhi?"
Response:
{{
  "content": "Let me check the best comedy shows in Delhi for you right away!",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "comedy", "location": "Delhi" }}
  }}
}}

Example 3 - Shorthand Response:
User: "hmm"
Response:
{{
  "content": "I hear you! Let me surprise you with some trending events that are creating buzz right now.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "" }}
  }}
}}

Example 4 - Mild Interest:
User: "k"
Response:
{{
  "content": "Great! I'll pull up some exciting shows that might catch your eye. One moment.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "" }}
  }}
}}

Example 5 - Positive Interest:
User: "aacha"
Response:
{{
  "content": "Got it! Wanna know what's cooking in our kitchen? Here are some delicacies just for you.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "" }}
  }}
}}

Example 6 - Location and Time Request:
User: "What's happening in Mumbai this weekend?"
Response:
{{
  "content": "Checking out the hottest events in Mumbai this weekend. You're in for a treat!",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "", "location": "Mumbai", "date": "2025-04-23" }}
  }}
}}

Example 7 - Requesting More Options:
User: "Show me more options"
Response:
{{
  "content": "Of course! Here's a fresh batch of exciting events for you to explore.",
  "function_call": {{
    "name": "SeeMoreShows",
    "parameters": {{}}
  }}
}}

Example 8 - Booking Intent:
User: "I want to book tickets for the Arijit Singh concert"
Response:
{{
  "content": "Great choice! Let me get those Arijit Singh tickets ready for you.",
  "function_call": {{
    "name": "book_show",
    "parameters": {{ "event_id": "arijit_123", "event_name": "Arijit Singh Live Concert" }}
  }}
}}

Example 9 - Negative Response:
User: "Not interested"
Response:
{{
  "content": "Okay, no worries! I'm here if you want to share or need help with anything else.",
  "function_call": null
}}

User: "chal nikal"
Response: 
{{
  "content": "Alright, but I'm just a message away if you need anything later!",
  "function_call": null
}}

User: "faltu hai"
Response: 
{{
  "content": "Got it! Just let me know if you need anything or want to talk about something else.",
  "function_call": null
}}

Example 10 - Hindi Short Response:
User: "thik hai"
Response:
{{
  "content": "Perfect! Let me find some trending shows that are creating a buzz right now.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "" }}
  }}
}}

Example 11 - Planning for Others:
User: "I need to impress my boss with an event"
Response:
{{
  "content": "Smart move! Let me find some prestigious events that'll surely impress your boss.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "prestigious corporate" }}
  }}
}}

Example 12 - Special Occasion:
User: "Anniversary plan"
Response:
{{
  "content": "How romantic! Let me find some special events perfect for celebrating your anniversary in style.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "romantic anniversary" }}
  }}
}}

Example 13 - Multi-parameter Search:
User: "Any rock concerts in Bangalore next month?"
Response:
{{
  "content": "Rock on! Checking for the best rock concerts in Bangalore next month.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "rock concerts", "location": "Bangalore", "date": "next month" }}
  }}
}}

Example 14 - Clarification with No Function Call:
User: "What kind of events do you have?"
Response:
{{
  "content": "I can help with concerts, comedy shows, plays, sports events, and more! What interests you most?",
  "function_call": null
}}

Example 15 - Direct Booking Request:
User: "Book me Taylor Swift tickets"
Response:
{{
  "content": "I'd be happy to help with Taylor Swift tickets! Let me check availability.",
  "function_call": {{
    "name": "search_event_query",
    "parameters": {{ "query": "Taylor Swift concert" }}
  }}
}}


IMPORTANT: All responses must follow this exact JSON structure:
```json
{{
  "content": "<your natural conversational response to the user>",
  "function_call": {{
    "name": "<function_name>",
    "parameters": {{ <appropriate parameters for the function> }}
  }}
}}
Your tools are {tools}


"""


def parser(text):
    first_brack = text.find('{')
    last_brack = text.rfind('}')
    text = text[first_brack:last_brack+1]
    text = text.replace('\\n','')
    text = text.replace('\r','')
    text = text.replace('\\','')
    return text

    
def extract_data(text):
    try:
        parsed_text = parser(text)
        loaded_data = json.loads(parsed_text)
        return loaded_data['content'], loaded_data['function_call']
    except (json.JSONDecodeError, KeyError) as e:
        st.error(f"Error extracting data: {str(e)}")
        return f"{text}", None


st.set_page_config(page_title="Ollama Chatbot", page_icon="💬", layout="wide")

DEFAULT_SYSTEM_PROMPT = sp2

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "function_call" not in st.session_state:
    st.session_state.function_call = []
    
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

st.markdown("""
<style>
    .stTextInput > div > div > input {
        padding: 12px;
        font-size: 16px;
        border-radius: 20px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .user-message {
        background-color: #e6f7ff;
        border-left: 5px solid #1890ff;
        color: #000;
    }
    .bot-message {
        background-color: #f6f6f6;
        border-left: 5px solid #888888;
        color: #000;
    }
    .message-content {
        margin-left: 10px;
        font-size: 16px;
        font-weight: 500;
    }
    .function-call {
        background-color: #FFF3CD;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #FFC107;
        margin-top: 10px;
        color: #000;
    }
    .system-prompt {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        padding: 10px;
        margin-bottom: 15px;
        border-radius: 5px;
        color: #000;
    }
</style>
""", unsafe_allow_html=True)

def get_bot_response(user_input):
    try:
        chat_history = []

        if st.session_state.system_prompt:
            chat_history.append({
                'role': 'system',
                'content': st.session_state.system_prompt
            })

        for message in st.session_state.messages:
            chat_history.append({
                'role': message['role'],
                'content': message['content']
            })

        chat_history.append({
            'role': 'user',
            'content': user_input
        })

        with st.spinner("Thinking..."):
            response = client.chat(
                model=st.session_state.get('model', 'granite3.2'),
                messages=chat_history
            )
            content, function_call = extract_data(response['message']['content'])

            # Store bot response along with its function call
            assistant_message = {"role": "assistant", "content": content}
            if function_call:
                assistant_message["function_call"] = function_call

            return assistant_message

    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return {"role": "assistant", "content": f"I encountered an error: {str(e)}"}
    


# Title and introduction
st.title("💬 Simple Chatbot")
st.markdown("Welcome to the chatbot! Type a message below to start the conversation.")

# Main container for the chat
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="avatar">👤</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:  # Assistant Response
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="avatar">🤖</div>
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Attach function call immediately after the assistant message
            if "function_call" in message:
                st.markdown(f"""
                <div class="function-call">
                    <strong>Function Called:</strong> {message["function_call"]['name']}<br>
                    <strong>Parameters:</strong> {json.dumps(message["function_call"]['parameters'], indent=2)}
                </div>
                """, unsafe_allow_html=True)
            

# Input area
with st.container():
    # Create two columns for input field and send button
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Your message:", key="input", 
                                   placeholder="Type your message here...",
                                   label_visibility="collapsed")
    
    with col2:
        send_button = st.button("Send")

# Process the input
if send_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate bot response
    bot_response = get_bot_response(user_input)
    st.session_state.messages.append(bot_response)  # Stores content + function_call
    
    # Clear input field and refresh UI
    st.rerun()

with st.sidebar:
    st.header("Settings")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["granite3.2"],
        index=0
    )
    
    # System prompt editor
    st.subheader("System Prompt")
    system_prompt = st.text_area(
        "Edit system prompt:",
        value=st.session_state.system_prompt,
        height=150
    )
    
    # Save system prompt button
    if st.button("Save System Prompt"):
        st.session_state.system_prompt = system_prompt
        st.success("System prompt updated!")
    
    # Reset to default system prompt
    if st.button("Reset to Default"):
        st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
        st.success("System prompt reset to default!")
        st.rerun()
        
    
    # Save current system prompt to file
    if st.button("Save Prompt to File"):
        prompt_json = json.dumps({"system_prompt": st.session_state.system_prompt})
        st.download_button(
            label="Download System Prompt",
            data=prompt_json,
            file_name="system_prompt.json",
            mime="application/json"
        )
    
    # Load system prompt from file
    st.subheader("Load System Prompt")
    uploaded_prompt = st.file_uploader("Upload system prompt JSON", type="json")
    if uploaded_prompt is not None:
        try:
            prompt_data = json.load(uploaded_prompt)
            if "system_prompt" in prompt_data:
                if st.button("Load Uploaded Prompt"):
                    st.session_state.system_prompt = prompt_data["system_prompt"]
                    st.success("System prompt loaded successfully!")
        except Exception as e:
            st.error(f"Error loading prompt file: {e}")
    
    # Load file example
    st.subheader("Process Examples from File")
    uploaded_file = st.file_uploader("Upload JSON file with examples", type="json")
    
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            if st.button("Process File"):
                for idx, l in enumerate(data):
                    with st.status(f"Processing example {idx+1}/{len(data)}..."):
                        try:
                            content, function_call = extract_data(l)
                            st.write(f"Content: {content[:50]}...")
                            if function_call:
                                st.write(f"Function Call: {str(function_call)[:50]}...")
                        except Exception as e:
                            st.error(f"Error processing example {idx+1}: {e}")
        except Exception as e:
            st.error(f"Error loading file: {e}")
    
    # Add a clear button to reset the chat
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.function_call = None
        st.session_state.user_input = ""
        st.rerun()
        
        
