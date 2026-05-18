import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from pydantic.v1 import BaseModel

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
        "Always use the search tools provided to gather information before answering. "
        "Do not answer from your internal knowledge. Use web_search, arxiv, or wikipedia when relevant."
    )

    agent_executor = create_agent(
        model=llm, 
        tools=tools, 
        system_prompt=system_instructions
    )

    with st.chat_message("assistant"):
        final_answer = ""
        search_results = ""

        try:
            result = agent_executor.invoke({"messages": st.session_state.messages})
            messages_output = None

            if isinstance(result, dict):
                messages_output = result.get("messages") or result.get("output")
            elif hasattr(result, "messages"):
                messages_output = result.messages
            elif isinstance(result, list):
                messages_output = result
            else:
                messages_output = [result]

            if not isinstance(messages_output, list):
                messages_output = [messages_output]

            for item in reversed(messages_output):
                if hasattr(item, "content") and item.content:
                    final_answer = item.content
                    break
                if isinstance(item, dict) and item.get("content"):
                    final_answer = item["content"]
                    break

            if not final_answer and isinstance(result, str):
                final_answer = result
        except Exception as e:
            st.warning(
                "Agent tool execution failed. Falling back to a direct web search and summary."
            )
            st.warning(f"Debug: {str(e)}")
            try:
                search_results = search_tool.run(user_prompt)
                with st.expander("✅ DuckDuckGo search results"):
                    st.write(search_results)

                prompt = (
                    "Use the following search results to answer the user question in a concise final answer. "
                    "Do not invent facts."
                    f"\n\nSearch results:\n{search_results}\n\nQuestion: {user_prompt}"
                )
                summary_msg = llm.invoke([HumanMessage(content=prompt)])
                final_answer = getattr(summary_msg, "content", str(summary_msg))
            except Exception as ex:
                st.error(f"Fallback search failed: {str(ex)}")
                final_answer = ""

        if final_answer:
            st.write(final_answer)
            st.session_state.messages.append(AIMessage(content=final_answer))
        else:
            st.error("No final answer could be extracted from the agent output.")