import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
import psycopg2
import mysql.connector
from langchain_groq import ChatGroq
import urllib.parse

# Streamlit Page Setup
st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

# Define constants for database types
LOCALDB = "USE_LOCALDB"
POSTGRES = "USE_POSTGRES"
MYSQL = "USE_MYSQL"

# Sidebar - Choose database
radio_opt = ["Use SQLite3 Database - Student.db", "Connect to PostgreSQL Database", "Connect to MySQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB you want to chat with", options=radio_opt)

# Initialize Database Variables
db_uri = None
pg_host, pg_user, pg_password, pg_db = None, None, None, None
mysql_host, mysql_user, mysql_password, mysql_db = None, None, None, None

if selected_opt == radio_opt[0]:  # SQLite
    db_uri = LOCALDB
elif selected_opt == radio_opt[1]:  # PostgreSQL
    db_uri = POSTGRES
    pg_host = st.sidebar.text_input("PostgreSQL Host", value="127.0.0.1").strip()
    pg_user = st.sidebar.text_input("PostgreSQL User", value="postgres").strip()
    pg_password = st.sidebar.text_input("PostgreSQL Password", type="password")
    pg_db = st.sidebar.text_input("PostgreSQL Database Name").strip()
elif selected_opt == radio_opt[2]:  # MySQL
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host").strip()
    mysql_user = st.sidebar.text_input("MySQL User").strip()
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database").strip()

api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not db_uri:
    st.info("Please enter the database information and URI.")

if not api_key:
    st.info("Please add the Groq API key.")

# LLM Model
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# Function to configure database connection
@st.cache_resource(ttl="2h")
def configure_db(db_uri, pg_host=None, pg_user=None, pg_password=None, pg_db=None, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    """Returns a SQLDatabase instance based on the selected configuration."""

    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))

    elif db_uri == POSTGRES:
        if not (pg_host and pg_user and pg_password and pg_db):
            st.error("❌ Please provide all PostgreSQL connection details.")
            st.stop()

        try:
            # ✅ URL Encode the password to handle special characters
            encoded_password = urllib.parse.quote(pg_password)

            # ✅ Corrected Connection String
            db_url = f"postgresql+psycopg2://{pg_user}:{encoded_password}@{pg_host}/{pg_db}"

            print(f"Connecting to PostgreSQL: {db_url}")  # Debugging Output
            engine = create_engine(db_url)
            return SQLDatabase(engine)

        except Exception as e:
            st.error(f"❌ PostgreSQL connection failed: {e}")
            st.stop()

    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("❌ Please provide all MySQL connection details.")
            st.stop()

        try:
            db_url = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
            print(f"Connecting to MySQL: {db_url}")  # Debugging Output
            engine = create_engine(db_url)
            return SQLDatabase(engine)
        except Exception as e:
            st.error(f"❌ MySQL connection failed: {e}")
            st.stop()

# Initialize database connection
if db_uri == LOCALDB:
    db = configure_db(db_uri)
elif db_uri == POSTGRES:
    db = configure_db(db_uri, pg_host, pg_user, pg_password, pg_db)
elif db_uri == MYSQL:
    db = configure_db(db_uri, mysql_host=mysql_host, mysql_user=mysql_user, mysql_password=mysql_password, mysql_db=mysql_db)

# Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create SQL Agent
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Message history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User query input
user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks=[streamlit_callback])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
