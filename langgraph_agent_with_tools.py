from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessageChunk
from langchain.tools import tool
import os

load_dotenv()

# ================== tools ==================
@tool
def addFile(path:str, filename:str) -> str:
    """Create a new file in the given path"""

    filepath = path + "/" + filename

    if not os.path.exists(filepath):
        with open(filepath, 'w') as fp:
            fp.write("New file")
        
        print(f"File: {filename} is created")
 
    else:
        print(f"File already exists")

@tool
def addFolder(path:str, dirname:str) -> str:
    """Create a new directory in the given path"""

    dirpath = path + "/" + dirname
    
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        
        print(f"Directory with {dirname} is created")
    
    else:
        print(f"Directory already exists")

# ================== Message History ==================

user_conversation_history = [
    SystemMessageChunk("You are a helpful assistant")
]

# ================== Agent: LLM + Tools ==================

model = ChatGroq(model='llama-3.3-70b-versatile', max_tokens=100)

agent = create_react_agent(
        model,
        tools=[addFile, addFolder], 
        prompt=None)

# ================== Helper Functions ==================

def displayConversation(conversation):
    for message in conversation:
        if isinstance(message, AIMessage):
            print("\n\nAssistant:")
        elif isinstance(message, SystemMessageChunk):
            print("\n\nSystem:")
        else:
            print("\n\nUser:")
        
        print(message.content)

# ================== User Interface ==================

while True:
    user_input = input("Enter the query:").lower()

    if user_input in ["quit", "q", "exit"]:
        print("Good bye")

        break

    user_conversation_history.append(HumanMessage(user_input))

    response = agent.invoke(
        {"messages": user_conversation_history}
    )

    user_conversation_history.append(response["messages"][-1])

    displayConversation(user_conversation_history)
