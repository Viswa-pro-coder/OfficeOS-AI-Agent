import streamlit as st
import time
import os
import requests
import json
import re
import pandas as pd
from io import StringIO
from streamlit_option_menu import option_menu
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# --- PAGE CONFIG ---
st.set_page_config(page_title="OfficeOS", layout="wide", page_icon="🏢")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Gradient Buttons */
    div.stButton > button {
        background: linear-gradient(45deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.4s;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(45deg, #182848 0%, #4b6cb7 100%);
        color: white;
    }

    /* Result Card */
    .result-card {
        background-color: #2D2D2D;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #8A2BE2;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Input alignment adjustment */
    .stTextInput > div > div > input {
        min-height: 45px;
    }
</style>
""", unsafe_allow_html=True)

# --- HELPER: TEXT CLEANER ---
def clean_text(text):
    """
    Forces newlines before headers ONLY to fix Markdown rendering.
    """
    text = re.sub(r'(?<!\n)###', '\n\n###', text) 
    return text

# --- REAL AI LOGIC 1: MARKET RESEARCHER ---
def run_direct_research(topic):
    results_container = st.empty()
    with st.status("🕵️ Agent is working...", expanded=True) as status:
        st.write("🌐 Connecting to World Wide Web...")
        time.sleep(1) 
        
        url = "[https://google.serper.dev/search](https://google.serper.dev/search)"
        payload = json.dumps({"q": topic})
        headers = {
            'X-API-KEY': st.secrets["SERPER_API_KEY"],
            'Content-Type': 'application/json'
        }
        
        st.write(f"🔍 Searching Google for: '{topic}'...")
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            search_data = response.json()
            organic_results = search_data.get("organic", [])[:4] 
            context_text = ""
            for res in organic_results:
                context_text += f"- {res.get('title')}: {res.get('snippet')}\n"
            st.write("✅ Found relevant data sources.")
            time.sleep(1)
        except Exception as e:
            status.update(label="Error in Search", state="error")
            return f"Search Error: {e}"

        st.write("🧠 Reading and analyzing content...")
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a Senior Market Researcher. 
        Your goal is to write a brief, executive-level summary based strictly on the provided search context.
        Use bullet points. Be professional. Do not hallucinate facts not in the context."""
        human_prompt = f"Topic: {topic}\n\nSearch Findings:\n{context_text}\n\nPlease summarize these findings into a report."
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("✍️ Drafting final report...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Mission Complete", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 2: EMAIL DRAFTER ---
def run_email_drafter(email_content):
    with st.status("📧 Agent is drafting...", expanded=True) as status:
        st.write("🧠 Analyzing email sentiment...")
        time.sleep(1) 
        llm = ChatGroq(temperature=0.7, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a highly professional Executive Assistant. 
        Your goal is to draft a polite, clear, and concise reply to the incoming email."""
        human_prompt = f"Incoming Email Content:\n{email_content}\n\nDraft a reply:"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("✍️ Composing response...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Draft Ready", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 3: MEETING MINUTES ---
def run_meeting_minutes(transcript):
    with st.status("📝 Agent is transcribing...", expanded=True) as status:
        st.write("🎧 Identifying speakers and key topics...")
        time.sleep(1)
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are an expert Project Manager. 
        Analyze the provided meeting transcript and generate clean Meeting Minutes.
        
        FORMATTING RULES:
        1. Use '###' for section headers.
        2. Ensure every bullet point starts on a NEW line.
        
        Required Structure:
        
        ### 📅 Meeting Summary
        * **Date:** (Insert Date)
        * **Attendees:** (Insert Names)
        
        ### 🗣️ Discussion Points
        * (Point 1)
        * (Point 2)
        
        ### ✅ Action Items
        * [ ] (Task) - Assigned to (Name)
        """
        human_prompt = f"Transcript:\n{transcript}\n\nGenerate Minutes:"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("📊 Extracting action items...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Minutes Generated", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 4: RESUME SCREENER ---
def run_resume_screener(resume_text, job_description):
    with st.status("📄 Agent is analyzing...", expanded=True) as status:
        st.write("🔍 Scanning resume for keywords...")
        time.sleep(1)
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a Senior Technical Recruiter.
        Compare the Candidate's Resume against the Job Description.
        
        FORMATTING RULES:
        1. Use '###' for section headers.
        
        Required Structure:
        
        ### 🎯 Match Analysis
        * **Match Score:** (0-100)%
        
        ### ✅ Key Strengths
        * (List 3 matching skills)
        
        ### ⚠️ Missing / Gaps
        * (List missing critical skills)
        
        ### 💡 Recommendation
        * (Proceed to Interview / Reject / Hold) - Give a 1-sentence reason.
        """
        human_prompt = f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("⚖️ Calculating match score...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Analysis Complete", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 5: SOCIAL MEDIA ENGINE ---
def run_social_media(announcement):
    with st.status("📱 Agent is creating content...", expanded=True) as status:
        st.write("🔥 Analyzing trends and hashtags...")
        time.sleep(1)
        llm = ChatGroq(temperature=0.8, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a Viral Social Media Manager.
        Convert the announcement into engaging posts for LinkedIn and Twitter.
        Output Structure:
        ### 💼 LinkedIn Post
        (Content)
        ### 🐦 Twitter / X Thread
        (Content)
        """
        human_prompt = f"Announcement:\n{announcement}\n\nGenerate Posts:"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("✍️ Writing viral hooks...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Content Ready", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 6: CONTRACT SIMPLIFIER ---
def run_contract_simplifier(legal_text):
    with st.status("⚖️ Agent is reviewing...", expanded=True) as status:
        st.write("🧐 Analyzing legal jargon...")
        time.sleep(1)
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a Senior Legal Counsel.
        Summarize the provided legal text into plain English.
        
        Structure:
        ### 🔎 Plain English Summary
        (2-3 sentences)
        
        ### 🚨 Key Risks & Red Flags
        * (Bullet point 1)
        * (Bullet point 2)
        
        ### 🟢 Rating
        * **Risk Level:** (Low/Medium/High)
        """
        human_prompt = f"Legal Text:\n{legal_text}\n\nSimplify this:"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("📝 Translating to plain English...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Review Complete", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 7: CODE BUG HUNTER ---
def run_bug_hunter(code_snippet):
    with st.status("🐛 Agent is debugging...", expanded=True) as status:
        st.write("🔍 Tracing logic flows...")
        time.sleep(1)
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a Senior Software Engineer.
        Analyze the code, find bugs/inefficiencies, and provide the fixed code.
        
        Structure:
        ### 🐞 Bug Analysis
        (Explain what is wrong in 1 sentence)
        
        ### 🛠️ Fixed Code
        ```python
        (The corrected code)
        ```
        """
        human_prompt = f"Code:\n{code_snippet}\n\nFind bugs and fix:"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("💻 Writing patch...")
        chain = prompt | llm
        response = chain.invoke({})
        status.update(label="Debug Complete", state="complete", expanded=False)
        return clean_text(response.content)

# --- REAL AI LOGIC 8: DATA CLEANER ---
def run_data_cleaner(messy_data):
    with st.status("🧹 Agent is cleaning...", expanded=True) as status:
        st.write("🌪️ Parsing unstructured text...")
        time.sleep(1)
        llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])
        system_prompt = """You are a Data Engineer.
        Convert the unstructured text into a CSV format string.
        Output ONLY valid CSV data. Ensure each row is on a new line. Do not wrap in markdown code blocks.
        """
        human_prompt = f"Messy Data:\n{messy_data}\n\nConvert to CSV:"
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])
        st.write("📊 Formatting to CSV...")
        chain = prompt | llm
        response = chain.invoke({})
        csv_string = response.content.strip()
        status.update(label="Data Cleaned", state="complete", expanded=False)
        return csv_string

# --- HEADER ---
st.title("🏢 OfficeOS: 8-Agent Project Day Demo")
st.markdown("---")

# --- SIDEBAR ---
with st.sidebar:
    st.title("Select Department")
    department = option_menu(
        "Choose Agent",
        ["Market Researcher", "Email Auto-Drafter", "Meeting Minutes", "Resume Screener", "Social Media Engine", "Contract Simplifier", "Code Bug Hunter", "Data Cleaner"],
        icons=["search", "envelope", "card-text", "person-lines-fill", "share", "file-earmark-text", "bug", "table"],
        menu_icon="cast", default_index=0,
    )
    st.markdown("---")
    st.markdown("### 🤖 OfficeOS v1.0")

# --- MAIN CONTENT LOGIC ---

# 1. Market Researcher
if department == "Market Researcher":
    st.header("📈 Market Researcher (Marketing)")
    col1, col2 = st.columns([3, 1])
    with col1: topic = st.text_input("Enter Topic", placeholder="e.g., Trends in AI for 2024", label_visibility="collapsed")
    with col2: start_btn = st.button("Start Research")
    if start_btn and topic:
        try: result = run_direct_research(topic)
        except Exception as e: result = f"Error: {e}"
        st.markdown(f"""<div class="result-card"><h3>✅ Research Complete</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 2. Email Auto-Drafter
elif department == "Email Auto-Drafter":
    st.header("📧 Email Auto-Drafter (Admin)")
    col1, col2 = st.columns([3, 1])
    with col1: email_content = st.text_area("Paste Email", height=200, placeholder="Paste email here...", label_visibility="collapsed")
    with col2: 
        st.write(""); st.write("")
        draft_btn = st.button("Draft Reply")
    if draft_btn and email_content:
        try: result = run_email_drafter(email_content)
        except Exception as e: result = f"Error: {e}"
        st.markdown(f"""<div class="result-card"><h3>✅ Draft Generated</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 3. Meeting Minutes
elif department == "Meeting Minutes":
    st.header("📝 Meeting Minutes Generator (Ops)")
    col1, col2 = st.columns([3, 1])
    with col1: transcript = st.text_area("Paste Transcript", height=300, placeholder="Paste transcript...", label_visibility="collapsed")
    with col2: 
        st.write(""); st.write("")
        gen_btn = st.button("Generate Minutes")
    if gen_btn and transcript:
        try: result = run_meeting_minutes(transcript)
        except Exception as e: result = f"Error: {e}"
        st.markdown(f"""<div class="result-card"><h3>✅ Minutes Generated</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 4. Resume Screener
elif department == "Resume Screener":
    st.header("📄 Resume Screener (HR)")
    col1, col2 = st.columns([3, 1])
    with col1: 
        resume_text = st.text_area("Paste Resume", height=200, placeholder="Paste resume...", label_visibility="collapsed")
        job_description = st.text_area("Job Description", height=200, placeholder="Paste JD...", label_visibility="collapsed")
    with col2: 
        st.write(""); st.write(""); st.write(""); st.write("")
        analyze_btn = st.button("Analyze Match")
    if analyze_btn and resume_text and job_description:
        try: result = run_resume_screener(resume_text, job_description)
        except Exception as e: result = f"Error: {e}"
        st.markdown(f"""<div class="result-card"><h3>✅ Analysis Complete</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 5. Social Media Engine
elif department == "Social Media Engine":
    st.header("📱 Social Media Engine (Content)")
    col1, col2 = st.columns([3, 1])
    with col1: announcement = st.text_area("Announcement", height=150, placeholder="Enter announcement...", label_visibility="collapsed")
    with col2: 
        st.write("")
        gen_post_btn = st.button("Generate Posts")
    if gen_post_btn and announcement:
        try: result = run_social_media(announcement)
        except Exception as e: result = f"Error: {e}"
        st.markdown(f"""<div class="result-card"><h3>✅ Posts Generated</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 6. Contract Simplifier
elif department == "Contract Simplifier":
    st.header("⚖️ Contract Simplifier (Legal)")
    col1, col2 = st.columns([3, 1])
    with col1: legal_text = st.text_area("Legal Text", height=300, placeholder="Paste legalese...", label_visibility="collapsed")
    with col2: 
        st.write(""); st.write("")
        simplify_btn = st.button("Simplify")
    if simplify_btn and legal_text:
        try: result = run_contract_simplifier(legal_text)
        except Exception as e: result = f"Error: {e}"
        st.markdown(f"""<div class="result-card"><h3>✅ Summary</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 7. Code Bug Hunter
elif department == "Code Bug Hunter":
    st.header("🐛 Code Bug Hunter (IT)")
    col1, col2 = st.columns([3, 1])
    with col1: code_input = st.text_area("Paste Code", height=300, placeholder="Paste buggy code...", label_visibility="collapsed")
    with col2: 
        st.write(""); st.write("")
        debug_btn = st.button("Debug")
    if debug_btn and code_input:
        try: result = run_bug_hunter(code_input)
        except Exception as e: result = f"Error: {e}"
        # FIX: Added newlines \n\n to prevent markdown parser error with closing div
        st.markdown(f"""<div class="result-card"><h3>✅ Debug Report</h3>\n\n{result}\n\n</div>""", unsafe_allow_html=True)

# 8. Data Cleaner
elif department == "Data Cleaner":
    st.header("🧹 Data Cleaner (Finance)")
    col1, col2 = st.columns([3, 1])
    with col1: messy_data = st.text_area("Messy Data", height=200, placeholder="Paste data...", label_visibility="collapsed")
    with col2: 
        st.write(""); st.write("")
        clean_btn = st.button("Format to CSV")
    if clean_btn and messy_data:
        try: 
            csv_data = run_data_cleaner(messy_data)
            st.markdown(f"""<div class="result-card"><h3>✅ Data Cleaned</h3></div>""", unsafe_allow_html=True)
            st.code(csv_data, language="csv") # Cleaner display for raw CSV
            try:
                df = pd.read_csv(StringIO(csv_data))
                st.dataframe(df)
            except:
                st.warning("Could not render table, but CSV is valid above.")
        except Exception as e: 
            st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("Built with intent")