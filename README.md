# paper-scout 📰

Scout scientific papers from just a simple prompt!

---

## 🚀 Features

- **Natural Language Search:**  
  Search arXiv for scientific papers using plain English prompts.

- **PDF Summarization:**  
  Summarize any scientific paper PDF with a single command.

- **LLM-Powered Tool Routing:**  
  Uses OpenRouter and OpenAI-compatible LLMs to intelligently route your queries to the right tool.

- **Streaming CLI Output:**  
  See results streamed live in your terminal.

- **Modular MCP Tooling:**  
  Easily extend or add new tools using the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/specification).

---

## 🛠️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/paper-scout.git
cd paper-scout
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Install MCP Server Dependencies

#### Linux/macOS:
```bash
# Install pdf_search server dependencies
(cd mcp_servers/pdf_search && uv install)

# Install pdf_summarize server dependencies  
(cd mcp_servers/pdf_summarize && uv install)
```

#### Windows (PowerShell):
```powershell
# Install pdf_search server dependencies
Push-Location mcp_servers\pdf_search; uv install; Pop-Location

# Install pdf_summarize server dependencies
Push-Location mcp_servers\pdf_summarize; uv install; Pop-Location
```

#### Windows (Command Prompt):
```cmd
# Install pdf_search server dependencies
cd mcp_servers\pdf_search && uv install && cd ..\..

# Install pdf_summarize server dependencies
cd mcp_servers\pdf_summarize && uv install && cd ..\..
```

### 4. Set Up Environment Variables

Create `.env` files in the following locations:
- Root directory: `paper-scout/.env`
- PDF summarize server: `paper-scout/mcp_servers/pdf_summarize/.env`

Add the following variables to both files:
```env
MODEL_NAME=YOUR-MODEL-NAME
OPENROUTER_API_KEY=YOUR-OPENROUTER-API-KEY
```

### 5. Run the CLI

From the repository root directory:
```bash
python main.py
```

### 6. Ask away!

---

## 🧩 Project Structure

```
paper-scout/
│
├── agent_host/         # Agent logic and MCP client
├── llm/                # LLM client (OpenRouter/OpenAI)
├── mcp_servers/        # MCP tool servers (pdf_search, pdf_summarize)
├── setup/              # Logging, config, and CLI streaming
├── main.py             # CLI entrypoint
└── .env
```

---

## Author ✍

Made with ♥ by [Abhay Shukla](https://github.com/into-the-night)

---

## License 📜
This project is open-source and available under the [MIT License](LICENSE.md).

---