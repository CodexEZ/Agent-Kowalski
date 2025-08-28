from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google AI API key: ")

#for servers
            # "search":{
            #     "command":"python",
            #     "args" : ["http://127.0.0.1:8000/mcp"],
            #     "transport":"streamable_http"
            # }
async def main():
    client = MultiServerMCPClient({
            "search":{
               
                "url" : "http://127.0.0.1:8000/mcp",
                "transport":"streamable_http"
            }
    })

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    tools = await client.get_tools()
    agent = create_react_agent(
        model=model,
        tools=tools
    )

    weather_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"who is pablo escobar, check latest data from web"}]}
    )
    print(weather_response['messages'][-1].content)


asyncio.run(main())
