# MongoDB_MCP Backend

## Agent Capabilities (Kowalski - Research and Information Assistant)

This backend integrates with an AI Agent named Kowalski, a highly capable **Research and Information Assistant**. Kowalski's primary goal is to investigate user queries using reasoning, available tools, and Python scripting. It always returns **self-contained, consistent HTML responses** adhering to a specific dark card theme and styling rules.

### Kowalski's Tools:

*   `get_links`, `search`, `get_page_content`: For web research and information gathering.
*   `get_weather`: For fetching weather information.
*   `get_databases`, `get_collections`, `get_fields_for_collection`: For database schema introspection.
*   `add_record`, `update_record`, `read_records`: For performing CRUD operations on database records.
*   `list_scripts`, `write_script`, `read_script`, `run_script`: For managing and executing custom Python scripts in a workspace.

### Kowalski's General Workflow:

1.  **Understand the question thoroughly**: Determine if the query is factual, analytical, data-driven, or research-based, and identify the expected output format (HTML, table, card, chart, etc.).
2.  **Determine the appropriate tool(s) to use**:
    *   **Quick facts / definitions** → use `search`.
    *   **Reference lists / multiple sources** → use `get_links` first, then `get_page_content`.
    *   **In-depth research / summaries** → use `get_links`, then `get_page_content`, then summarize.
    *   **Weather queries** → use `get_weather`.
    *   **Database tasks** → validate schema using `get_databases`, `get_collections`, `get_fields_for_collection`, then `read_records`, `add_record`, or `update_record`.
3.  **If analysis or processing is required beyond existing tools**: Write and run a custom Python script in the workspace for tasks like data aggregation, computations, text parsing, or web scraping.
4.  **Web scraping / research workflow**: Identify target URLs, retrieve content, parse and extract structured information, using scripts if necessary. Always respect `robots.txt`.
5.  **Cross-check multiple sources** whenever possible.
6.  **Summarize findings clearly and concisely**: Format output in the standardized HTML theme using tables, cards, and icons.
7.  **Fallback to scripting if no suitable tool exists**: Automatically write and run a Python script, returning processed results in theme-consistent HTML.

---

This project provides a backend API built with FastAPI, utilizing MongoDB for data storage and integrating with the Model Context Protocol (MCP) for advanced functionalities. It includes user authentication (registration, login, logout) and a chat endpoint powered by a Gemini model with tool-use capabilities.

## Features

*   **FastAPI Backend:** A robust and high-performance API framework.
*   **MongoDB Integration:** Asynchronous database operations using `motor` for user and session management.
*   **User Authentication:** Secure user registration, login, and logout with password hashing (bcrypt).
*   **Session Management:** Basic session handling for authenticated users.
*   **Gemini Chat Integration:** A `/chat` endpoint that leverages Google's Gemini model for conversational AI, enhanced with MCP tools.
*   **Model Context Protocol (MCP):** Integration with external MCP servers for functionalities like search, database interactions, and script execution.
*   **CORS Enabled:** Configured for cross-origin resource sharing.
*   **Structured Logging:** Using `loguru` for improved logging.
*   **Environment Variable Configuration:** Database connection URL configurable via `.env` file.

## Project Structure

```
.
├── .env                      # Environment variables (e.g., MONGO_URL)
├── api.py                    # Main FastAPI application, API endpoints
├── client.py                 # (Presumed) Client-side interaction script
├── requirements.txt          # Python dependencies
├── start_server.bat          # Windows batch script to start the server
├── test.ipynb                # Jupyter notebook for testing
├── db/                       # Database related modules
│   ├── __init__.py
│   ├── crud.py               # CRUD operations for users and sessions
│   └── database.py           # MongoDB connection and utility functions
├── models/                   # Pydantic models for data validation
│   ├── api_models.py         # API request/response schemas, UserSchema
│   └── gemini_chat_model.py  # Models for Gemini chat interactions
├── prompts/                  # Prompt definitions for AI models
│   └── prompt.py             # General prompt for the Gemini agent
├── servers/                  # MCP server definitions and related files
│   ├── dockerfile
│   ├── mongoose_database_server.py
│   ├── script_server.py
│   ├── search_server.py
│   ├── web_data.json
│   └── workspace/            # Scripts for the script_server
│       └── ... (various utility scripts)
└── utils/                    # Utility functions
    ├── __init__.py
    ├── gemini_call.py        # Logic for calling Gemini API with MCP tools
    └── pass_hasher.py        # Password hashing utilities
```

## Setup and Installation

### Prerequisites

*   Python 3.8+
*   MongoDB instance (local or remote)

### 1. Clone the repository

```bash
git clone <repository_url>
cd MongoDB_MCP
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your MongoDB connection string:

```
MONGO_URL="mongodb://localhost:27017/"
# Add any other necessary environment variables here
```

### 5. Start MongoDB

Ensure your MongoDB instance is running. If you're running it locally, you can usually start it via your system's service manager or by running `mongod` in your terminal.

### 6. Start the FastAPI Server

```bash
python api.py
```

The API will be accessible at `http://localhost:8080`.

### 7. (Optional) Start MCP Servers

This project integrates with MCP servers. You might need to start these separately if they are not already running. The `utils/gemini_call.py` file indicates the following MCP servers are expected:

*   `search`: `http://127.0.0.1:8000/mcp`
*   `database`: `http://127.0.0.1:8001/mcp`
*   `scripts`: `http://127.0.0.1:8002/mcp`

Refer to the documentation for these specific MCP servers for instructions on how to run them.

## API Endpoints

### User Authentication

*   **`POST /register`**
    *   Registers a new user.
    *   Request Body: `UserSchema` (username, password)
    *   Response: `ResponseSchema` (status, content)
*   **`POST /login`**
    *   Logs in an existing user and creates a session.
    *   Request Body: `UserSchema` (username, password)
    *   Response: `ResponseSchema` (status, content including user data and `session_id`)
*   **`POST /logout`**
    *   Logs out a user.
    *   Headers: `Authorization: <session_id>`
    *   Response: `ResponseSchema` (status, content)

### Chat

*   **`POST /chat`**
    *   Interacts with the Gemini AI model.
    *   Request Body: `GeminiChatModel` (list of `Chat` messages)
    *   Response: `GeminiChatModel` with the AI's response appended.

## Improvements Implemented

*   **Enhanced Error Handling:** More specific error handling for user registration and login, returning `ResponseSchema` with descriptive messages.
*   **Improved Logging:** Added `loguru` statements for successful and failed user registrations and logins, providing better visibility into application flow.
*   **Database Interaction Refinements:** Corrected a typo in `db/crud.py`'s `login` method (`if not user:` changed to `if not user_instance:`).
*   **Centralized Configuration:** `MONGO_URL` in `db/database.py` is now loaded from the `.env` file, improving deployment flexibility.

## Future Enhancements (Not Implemented in this iteration)

*   **Robust Session Management:** Decoupling session storage (e.g., using Redis), specific session logout, and implementing a FastAPI dependency for session validation on protected routes.
*   **Comprehensive Input Validation:** More detailed validation for user inputs beyond basic Pydantic models.
*   **Rate Limiting:** To prevent abuse of API endpoints.
*   **Containerization:** Dockerize the application for easier deployment.
*   **Automated Testing:** Implement unit and integration tests.
