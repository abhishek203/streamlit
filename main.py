import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets['openai_key'])
assistant_id = 'asst_i6lQ9jKozoyclqCCa6V8jxZB'


def run_assistant(thread):
    
      run = client.beta.threads.runs.create_and_poll(
      thread_id=thread.id,
      assistant_id=assistant_id    )
      if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
          thread_id=thread.id
        )
        return messages
      else:
        return run.status

def generate_response(query):
    thread = client.beta.threads.create()
    thread_id = thread.id
    message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=query,
        )
    
    # Run the assistant and get the new message
    new_message = run_assistant(thread)

    return new_message
def display_messages_nicely(data):
    for message in data:
        # Accessing the content list
        for content_block in message.content:
            # Checking if the content block is of type 'text'
            if content_block.type == 'text':
                # Printing the 'value' of the text content block
                return (content_block.text.value)

# Assuming 'data' is your list of Message objects

def main():
    st.title('GPT for oscilloscope code')

    # Creating an input field for the user
    user_input = st.text_input('Enter your prompt:', '')

    # Button to process the data
    if st.button('Process'):
        # Use the imported function
        result = generate_response(user_input)
        res = display_messages_nicely(result)
        # Display the result
        st.write('Processed Data:', res)

def test():
     generate_response('give python code to extract channel 1 data for 10 sec')

main()