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

```sh
    git clone https://github.com/yourusername/paper-scout.git
    cd paper-scout
```

### 2. Install Dependencies

```sh
    poetry install
```

### 3. Install Dependencies [MCP Servers]

```sh
    cd .\mcp_servers\pdf_search
    uv install
    cd ..
    cd ..
    cd .\mcp_servers\pdf_summarize
    uv install
```

### 4. Set Up Environment Variables

Create a `.env` file in repo directory and `\mcp_servers\pdf_summarize\`:
```
    MODEL_NAME=YOUR-MODEL-NAME
    OPENROUTER_API_KEY=YOUR-OPENROUTER-API-KEY
```

### 5. Run the CLI

From the repo directory,
```sh
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