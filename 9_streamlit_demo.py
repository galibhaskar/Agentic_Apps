import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

st.title("Chatbot App")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "chat-thread-1"

if "checkpointer" not in st.session_state:
    st.session_state.checkpointer = MemorySaver()

if "agent" not in st.session_state:
    llm_model = ChatGroq(
        model="llama-3.3-70b-versatile",
        max_tokens=50,
        temperature=0,
    )
    st.session_state.agent = create_react_agent(
        model=llm_model,
        tools=[],
        checkpointer=st.session_state.checkpointer,
        prompt="You are a helpful assistant."
    )

agent = st.session_state.agent

def display_chat_history():
    for role, message in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(message)

async def stream_graph_updates(user_input: str) -> str:
    assistant_response = ""
    
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            chat_config = {
                "configurable": 
                    {"thread_id": st.session_state.thread_id}
                }

            events = agent.stream(
                {"messages": [HumanMessage(user_input)]}, 
                config=chat_config)

            for event in events:
                for value in event.values():
                    content = value["messages"][-1].content

                    assistant_response += content
                        
                    message_placeholder.markdown(assistant_response)

        st.session_state.messages.append(("assistant", assistant_response or "_(no output)_"))
    
    except Exception as ex:
        st.error(f"Exception: {ex}")
    
    finally:
        return "done"

async def run_agent():
    print(st.session_state)

    display_chat_history()

    prompt = st.chat_input("How can I help you today?")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append(("user", prompt))

        await stream_graph_updates(prompt)

asyncio.run(run_agent())
