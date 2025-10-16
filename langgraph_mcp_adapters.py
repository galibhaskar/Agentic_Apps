import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

"""
MCP_Adapaters in Langchain:
1. Host : application
2. MCP Client : instance/process that communicates with the MCP server
3. MCP Server : remote/local server that serves the MCP client requests.

"""

GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

llm_model1 = ChatGroq(
    model="llama-3.3-70b-versatile",
    # max_tokens=100
)


llm_model2 = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    # max_tokens=100
)

def extractResponse(response):
    print(response["messages"][-1].content)


async def run_agent():
    # defining the clients
    client = MultiServerMCPClient(
        {
            # local MCP server that communciates with remote
            "github": {
               "command": "npx",
               "args": [
                   "-y",
                   "@modelcontextprotocol/server-github"
               ],
               "env": {
                   "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
               },
               "transport": "stdio"
           }
        }
    )

    tools = await client.get_tools()

    agent = create_react_agent(
        model=llm_model2,
        tools=tools
    )

    while True:
        user_input = input("Enter a query:")

        if user_input in ["quit", "exit", "q"]:
            break
        
        query = HumanMessage(user_input)

        # ainvoke: asynchronous invoke
        response = await agent.ainvoke({
            "messages": [query]
        })

        print(extractResponse(response))

if __name__=="__main__":
    asyncio.run(run_agent())