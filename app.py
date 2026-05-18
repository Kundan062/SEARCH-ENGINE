import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent

# --- 1. Tool Setup ---
arxiv_tool = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=1000))
wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000))
search_tool = DuckDuckGoSearchRun(name="web_search")

tools = [search_tool, arxiv_tool, wiki_tool]

# --- 2. Streamlit UI ---
st.set_page_config(page_title="2026 Transparent Search", page_icon="🔍")
st.title("🔍 Transparent Search Agent")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if not api_key:
    st.info("Please enter your Groq API key to start.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        AIMessage(content="I will now show you exactly which tools I'm using. Ask away!")
    ]

for msg in st.session_state.messages:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    st.chat_message(role).write(msg.content)

# --- 3. Agent Implementation ---
if user_prompt := st.chat_input(placeholder="Search Wikipedia for Quantum Computing"):
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    st.chat_message("user").write(user_prompt)

    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name="openai/gpt-oss-120b", 
        streaming=False,
        temperature=0
    )

    # Force the agent to actually use the tools instead of its internal memory
    system_instructions = (
        "You are a helpful research assistant. "
        "ALWAYS use the search tools provided to gather information before answering. "
        "Do not answer from your internal knowledge. Use web_search, arxiv, or wikipedia."
    )

    agent_executor = create_react_agent(
        model=llm, 
        tools=tools, 
        prompt=system_instructions
    )

    with st.chat_message("assistant"):
        final_answer = ""
        
        try:
            # THE FIX: We use .stream() to catch the graph's events one by one
            # and manually render them to Streamlit.
            for step in agent_executor.stream({"messages": st.session_state.messages}, stream_mode="updates"):
                
                # 1. Catch what the Agent is deciding to do
                if "agent" in step:
                    msg = step["agent"]["messages"][-1]
                    
                    # If it decides to call a tool, show it in a blue info box!
                    if msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            st.info(f"🛠️ **Calling Tool:** `{tool_call['name']}` | **Query:** `{tool_call['args']}`")
                    
                    # If it has the final text response, save it to output
                    if msg.content:
                        final_answer = msg.content
                
                # 2. Catch the data the Tool brings back
                elif "tools" in step:
                    msg = step["tools"]["messages"][-1]
                    
                    # Create a dropdown expander so you can click to see the raw search results
                    with st.expander(f"✅ Result from `{msg.name}`"):
                        st.write(msg.content)
            
            # Print the final compiled answer to the screen
            if final_answer:
                st.write(final_answer)
                st.session_state.messages.append(AIMessage(content=final_answer))
            
        except Exception as e:
            st.error(f"Error: {str(e)}")