# **LangChain SQL Chatbot: Query Databases with AI**  

🚀 **Interact with SQL databases using natural language!** This open-source Streamlit app leverages **LangChain** and **Groq Llama3** to enable conversational querying of SQLite, PostgreSQL, and MySQL databases.  

---

## **Features**
✅ Chat with your database using AI  
✅ Supports **SQLite, PostgreSQL, and MySQL**  
✅ Uses **LangChain SQL Agent** for intelligent query generation  
✅ Secure **API Key input for Groq Llama3 model**  
✅ Optimized for **performance with caching**  

---

## **Installation**
### **1. Clone the Repository**
```sh
git clone https://github.com/ravirch/Query-Databases-with-AI.git
cd langchain-sql-chatbot
```

### **2. Create a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Run the Streamlit App**
```sh
streamlit run app.py
```

---

## **Configuration**
### **Database Connection**  
1. **SQLite**: Uses `student.db` by default.  
2. **PostgreSQL**: Enter host, user, password, and database name in the sidebar.  
3. **MySQL**: Similar setup to PostgreSQL.  

### **API Key**  
You need a **Groq API Key** to use the **Llama3 model**. Enter it in the sidebar.

---

## **Usage**
1. **Select a database** from the sidebar.  
2. **Provide credentials** (if using PostgreSQL/MySQL).  
3. **Enter your query** in plain English (e.g., *"Show top 10 students from student.db"*).  
4. The chatbot **generates and executes** the SQL query.  
5. **View responses** instantly in the chat interface.  

---

## **Tech Stack**
- **Streamlit** → UI & Chatbot Interface  
- **LangChain** → SQL Agent for Query Processing  
- **Groq Llama3** → AI-Powered Query Understanding  
- **SQLAlchemy** → Database Connection  
- **SQLite, PostgreSQL, MySQL** → Supported Databases  

---

## **Contributing**
🎯 **Want to improve this project?**  

1. **Fork this repository**  
2. **Create a new branch**  
3. **Make your changes**  
4. **Submit a pull request**  

All contributions are welcome!  

---

## **License**
🚨 **No license yet!** This project is open-source but doesn't have a license. Feel free to use and modify it, but it's recommended to add a license if needed.  

---

### **⭐ Star this Repo if You Like It!**
🔗 **GitHub Repo:** _[https://github.com/ravirch/Query-Databases-with-AI](https://github.com/ravirch/Query-Databases-with-AI)_  
💬 **Questions?** Open an issue or reach out!  

---
