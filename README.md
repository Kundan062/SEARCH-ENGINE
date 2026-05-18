# 🔍 Transparent Search Agent

A transparent AI search agent built with Streamlit that shows every step of the research process in real-time. Watch the agent intelligently select and use multiple tools—DuckDuckGo, Wikipedia, ArXiv—to gather information. See live tool calls, queries, and results. Built with LangChain, LangGraph, and Groq LLM.

## ✨ Features

- **🔍 Multi-Source Search**: Integrates DuckDuckGo, Wikipedia, and ArXiv for comprehensive research
- **🤖 AI-Powered Agent**: Uses LangChain + LangGraph with Groq LLM for intelligent tool selection
- **👁️ Full Transparency**: Displays every tool call, query, and result in real-time
- **💬 Conversational Interface**: Chat-based UI with message history using Streamlit
- **🛠️ ReAct Pattern**: Implements reasoning and acting for reliable information gathering
- **🔒 API Key Protection**: Secure API key input through Streamlit sidebar

## 🛠️ Tech Stack

- **Streamlit** - Interactive web UI framework
- **LangChain** - LLM framework for tool integration
- **LangGraph** - Agentic workflow orchestration
- **Groq API** - Fast LLM inference
- **DuckDuckGo API** - Web search
- **Wikipedia API** - Wikipedia searches
- **ArXiv API** - Academic paper queries

## 📋 Prerequisites

- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com))

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Searchengine
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install streamlit langchain-groq langchain-community langgraph
```

Or if requirements.txt is available:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Usage

1. **Enter Your Groq API Key**: Paste your API key in the sidebar
2. **Type Your Query**: Ask any research question in the chat input
   - Example: "Search Wikipedia for Quantum Computing"
   - Example: "Find recent papers on machine learning from ArXiv"
3. **Watch the Agent Work**: 
   - See which tools are being called
   - View the queries being sent
   - Read the raw results in expandable sections
4. **Get Your Answer**: The agent compiles the information into a final response

## 🔄 How It Works

1. **User Input** → Sends message to the AI agent
2. **Tool Selection** → Agent decides which tool(s) to use
3. **Execution** → Runs the selected tools with appropriate queries
4. **Transparency** → Shows each step in the UI
5. **Compilation** → Agent synthesizes results into final answer

## 🎯 Example Queries

- "Search for information about quantum entanglement"
- "Find the latest papers on deep learning from ArXiv"
- "What is the capital of France and who is the current president?"
- "Search Wikipedia for machine learning"
- "Find recent news about AI safety"

## ⚙️ Configuration

### API Settings
- **Model**: `openai/gpt-oss-120b` (via Groq)
- **Temperature**: 0 (deterministic responses)
- **Streaming**: Disabled for better tool call tracking

### Tool Settings
- **ArXiv**: Top 1 result, max 1000 characters
- **Wikipedia**: Top 1 result, max 1000 characters
- **DuckDuckGo**: Web search with default parameters

Modify `app.py` to adjust these settings.

## 📁 Project Structure

```
Searchengine/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .git/              # Git repository
```

## 🐛 Troubleshooting

### "Invalid API Key" Error
- Ensure your Groq API key is valid
- Get a free key at https://console.groq.com

### Tool Not Responding
- Check your internet connection
- Verify API rate limits haven't been exceeded
- Try a simpler query

### Streamlit Connection Error
- Ensure port 8501 is not in use
- Try: `streamlit run app.py --server.port 8502`

## 📝 Notes

- The agent is instructed to **always use tools** and not rely on internal knowledge
- Tool results are shown in expandable sections to keep the UI clean
- Conversation history is maintained within the session

## 🔗 Related Links

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://docs.langchain.com/)
- [Groq API Docs](https://console.groq.com/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of AI/ML project exploration.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Last Updated**: May 2026
