from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient, load_mcp_prompt
from models.gemini_chat_model import GeminiChatModel,Chat
from langgraph.prebuilt import create_react_agent
from prompts.prompt import general_prompt
mcp_client = MultiServerMCPClient({
        "search": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http"
        },
        "database":{
            "url": "http://127.0.0.1:8001/mcp",
            "transport":"streamable_http"
        },
        "scripts":{
            "url":"http://127.0.0.1:8002/mcp",
            "transport":"streamable_http"
        }
    })


async def gemini(messages: GeminiChatModel):
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    tools = await mcp_client.get_tools()
   
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=general_prompt()
    )

    response = await agent.ainvoke(messages.model_dump())
    last_content = response['messages'][-1].content

    # Ensure it's always a string
    if isinstance(last_content, list):
        last_content = "\n".join(str(c) for c in last_content)
    else:
        last_content = str(last_content)

    messages.messages.append(Chat(role="ai", content=last_content))
    return messages

