import streamlit as st
import base64
import time
import google.generativeai as genai
from google.api_core import exceptions

# --- Configuration and Setup ---
st.set_page_config(
    page_title="Adventure Content Planner AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
<style>
.stButton>button {
    background-color: #EF4444;
    color: white;
    font-weight: bold;
    border-radius: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.stButton>button:hover {
    background-color: #DC2626;
    transform: translateY(-1px);
}
.result-section {
    padding: 1rem;
    border-radius: 0.75rem;
    background-color: #F9FAFB;
    margin-bottom: 1rem;
    border: 1px solid #E5E7EB;
}
</style>
""", unsafe_allow_html=True)

# --- 1. Smart Model Selector (Fixes 404 Errors) ---
def get_best_model(api_key):
    """
    Automatically finds the best available model for the user to avoid 404 errors.
    """
    genai.configure(api_key=api_key)
    try:
        # List all models available to this API key that support content generation
        all_models = genai.list_models()
        available_model_names = [
            m.name for m in all_models 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # Priority list: We prefer Flash (fast/cheap), then Pro
        priorities = [
            'gemini-1.5-flash',
            'gemini-1.5-flash-latest',
            'gemini-1.5-flash-001',
            'gemini-1.5-pro',
            'gemini-pro',
            'gemini-1.0-pro'
        ]
        
        # Find the first priority that exists in the available models
        for p in priorities:
            for m in available_model_names:
                if p in m:
                    return m # Return the full model name (e.g., models/gemini-1.5-flash)
        
        # Fallback: If no specific match, just take the first available one
        if available_model_names:
            return available_model_names[0]
            
        return 'gemini-1.5-flash' # Ultimate fallback
        
    except Exception as e:
        # If listing fails, default to a safe bet
        return 'gemini-1.5-flash'

# --- 2. The Real AI Function ---
def generate_content_plan(api_key, activity_summary):
    genai.configure(api_key=api_key)
    
    # Smartly pick the model
    model_name = get_best_model(api_key)
    
    # Instantiate the model
    model = genai.GenerativeModel(model_name)

    system_prompt = """
    You are an expert video content strategist for Instagram Reels and TikTok.
    Your goal: Turn a raw activity description into a viral-worthy content plan.
    
    CRITICAL INSTRUCTION: You MUST format your output in Markdown.
    Include these specific sections:
    1. ### Content Planner Output for: [Summary Title]
    2. #### 💡 Post Ideas (3 distinct concepts)
    3. #### 🎬 Reel Storyline (A table with columns: Stage, Duration, Visual, Audio/Transition)
    4. #### ✍️ Caption Options (3 options: Funny, Inspiring, Short)
    5. #### #️⃣ Hashtags (10 optimized tags)
    """

    full_prompt = f"{system_prompt}\n\nUSER ACTIVITY SUMMARY:\n{activity_summary}"

    try:
        with st.spinner(f"🤖 AI is brainstorming using {model_name}..."):
            response = model.generate_content(full_prompt)
            return response.text
    except Exception as e:
        # Intelligent Error Handling (Rate Limits)
        error_msg = str(e)
        if "429" in error_msg:
            st.warning("🚦 High Traffic (Rate Limit Hit). Retrying automatically in 4 seconds...")
            time.sleep(4)
            try:
                response = model.generate_content(full_prompt)
                return response.text
            except Exception as e2:
                st.error("Still busy! Please wait a minute before trying again.")
                return None
        else:
            st.error(f"API Error: {e}")
            return None

# --- 3. The Mock Function (Fallback) ---
def mock_llm_call(activity_summary):
    time.sleep(2)
    return f"""
### (MOCK MODE) Content Planner for: "{activity_summary}"
*To see real AI results, please enter a Gemini API Key in the sidebar.*

#### 💡 Post Ideas
1. **POV Action:** High energy cuts.
2. **Fail Compilation:** Funny set to upbeat music.
3. **Scenery:** Slow pans of the view.

#### 🎬 Reel Storyline
| Stage | Duration | Visual |
| :--- | :--- | :--- |
| Hook | 1s | The best moment first. |
| Body | 5s | Fast cuts of action. |
| Outro | 2s | High fives. |

#### ✍️ Captions
1. Best day ever! 🏔️
2. Rate this 1-10.
3. Wait for the end...
"""

# --- UI Layout ---

st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Get a free key from aistudio.google.com")

# DEBUG TOOLS (Optional but helpful)
if api_key:
    st.sidebar.divider()
    if st.sidebar.button("🔍 Check Model Access"):
        try:
            genai.configure(api_key=api_key)
            # List models that support generateContent
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.sidebar.success(f"Access Confirmed! Found {len(models)} models.")
            st.sidebar.code("\n".join(models))
        except Exception as e:
            st.sidebar.error(f"Key Error: {e}")

st.title("🏔️ Adventure Content Planner AI")
st.markdown("Instantly generate storyboards, captions, and hashtags.")

# Input Section
with st.container():
    st.header("1. Describe Your Activity")
    activity_summary = st.text_area(
        "What happened?",
        "Skiing day with friends. We found some amazing deep powder, had lunch on the mountain, and I had one hilarious wipeout.",
        height=150
    )
    
    generate_button = st.button("Generate Content Plan", use_container_width=True)

# Logic: Decide which function to call
if generate_button:
    if not activity_summary:
        st.warning("Please write a summary first.")
    else:
        if api_key:
            # REAL AI CALL
            result = generate_content_plan(api_key, activity_summary)
            if result:
                st.session_state['result'] = result
        else:
            # MOCK CALL
            st.warning("Running in Simulation Mode (No API Key detected).")
            st.session_state['result'] = mock_llm_call(activity_summary)

# Display Results
if 'result' in st.session_state:
    st.divider()
    st.header("3. Your Custom Content Plan")
    st.markdown(st.session_state['result'])

    # Download Button
    b64 = base64.b64encode(st.session_state['result'].encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="content_plan.txt" style="text-decoration:none;color:#EF4444;font-weight:bold;">⬇️ Download Plan (.txt)</a>'
    st.markdown(href, unsafe_allow_html=True)