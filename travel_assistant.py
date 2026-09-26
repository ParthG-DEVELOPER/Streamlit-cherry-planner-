import streamlit as st
import time
from google import genai
from dotenv import load_dotenv
from rich.console import Console
load_dotenv()
console = Console()


client = genai.Client()
st.set_page_config(
    page_title=" Travel Assistant",
    page_icon="🍒", # Optional: accepts emojis, shortcodes, or paths to local images
    layout="wide"    # Optional: "centered" or "wide"
)
st.markdown(
    """
    <style>
    /* Set a deep luxury cherry / burgundy radiant background with vignette */
    .stApp {
        background: radial-gradient(circle at 50% 15%, #6e1428 0%, #380a13 50%, #1a0307 100%);
        color: #FFFFFF;
        overflow-x: hidden;
    }
    
    /* Creative Background Animation Layers */
    .immersive-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    /* Ambient glowing background light orbs */
    .glow-orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
        opacity: 0.35;
        animation: orbPulse 10s ease-in-out infinite alternate;
    }
    .orb-1 { width: 350px; height: 350px; background: #ff4b6e; top: -100px; left: -100px; }
    .orb-2 { width: 450px; height: 450px; background: #9c1432; bottom: -150px; right: -100px; animation-delay: 5s; }

    @keyframes orbPulse {
        0% { transform: scale(1); opacity: 0.25; }
        100% { transform: scale(1.2); opacity: 0.45; }
    }

    /* Floating Cherry & Sparkle Elements */
    .cherry-particle {
        position: absolute;
        display: block;
        width: 40px;
        height: 40px;
        background: rgba(255, 75, 110, 0.08);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 182, 193, 0.2);
        border-radius: 50%;
        bottom: -150px;
        animation: floatUp 18s linear infinite;
        text-align: center;
        line-height: 40px;
        box-shadow: 0 0 20px rgba(255, 75, 110, 0.15);
    }

    /* Randomizing particle pathways and timings */
    .cherry-particle:nth-child(1) { left: 5%; width: 50px; height: 50px; line-height: 50px; animation-duration: 15s; animation-delay: 0s; }
    .cherry-particle:nth-child(2) { left: 18%; width: 30px; height: 30px; line-height: 30px; animation-duration: 22s; animation-delay: 2s; }
    .cherry-particle:nth-child(3) { left: 32%; width: 60px; height: 60px; line-height: 60px; animation-duration: 19s; animation-delay: 4s; }
    .cherry-particle:nth-child(4) { left: 50%; width: 35px; height: 35px; line-height: 35px; animation-duration: 25s; animation-delay: 1s; }
    .cherry-particle:nth-child(5) { left: 68%; width: 45px; height: 45px; line-height: 45px; animation-duration: 17s; animation-delay: 3s; }
    .cherry-particle:nth-child(6) { left: 82%; width: 55px; height: 55px; line-height: 55px; animation-duration: 21s; animation-delay: 5s; }
    .cherry-particle:nth-child(7) { left: 93%; width: 35px; height: 35px; line-height: 35px; animation-duration: 24s; animation-delay: 2s; }

    @keyframes floatUp {
        0% { transform: translateY(0) rotate(0deg) scale(0.8); opacity: 0.8; }
        50% { opacity: 0.4; transform: translateY(-600px) rotate(360deg) scale(1.15); }
        100% { transform: translateY(-1200px) rotate(720deg) scale(0.8); opacity: 0; }
    }

    /* Keyframes for Floating Hover Effects */
    @keyframes headerFloat {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    @keyframes buttonFloat {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }

    /* Ensure content stays above animated background */
    .stApp > div {
        position: relative;
        z-index: 1;
    }
    
    /* Header Container */
    .cherry-header-container {
        background: rgba(56, 10, 20, 0.55);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 110, 140, 0.25);
        padding: 3rem;
        border-radius: 28px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        margin-bottom: 2.5rem;
        animation: headerFloat 4s ease-in-out infinite;
    }
    
    /* Title Style */
    .cherry-title {
        font-size: 3.3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ff758c 0%, #ff8da1 40%, #ffb199 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.6rem;
        letter-spacing: 1.2px;
        text-shadow: 0 15px 30px rgba(255, 117, 140, 0.25);
    }
    
    /* Subtitle Style */
    .cherry-subtitle {
        font-size: 1.3rem;
        color: #f7d1d8;
        font-weight: 300;
        letter-spacing: 0.8px;
    }

    /* Customizing the Streamlit Button to match theme & float */
    div.stButton > button {
        background: linear-gradient(135deg, #ff4b6e 0%, #ff758c 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 182, 193, 0.4) !important;
        padding: 0.8rem 2.2rem !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        box-shadow: 0 10px 25px rgba(255, 75, 110, 0.45) !important;
        transition: all 0.3s ease !important;
        animation: buttonFloat 3s ease-in-out infinite !important;
        width: 100%;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #ff2a55 0%, #ff4b6e 100%) !important;
        box-shadow: 0 15px 30px rgba(255, 75, 110, 0.7) !important;
        border-color: #ffffff !important;
        transform: translateY(-4px) scale(1.02) !important;
    }
    </style>

    <!-- Ultra-Creative Immersive Background Elements -->
    <div class="immersive-bg">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="cherry-particle">🍒</div>
        <div class="cherry-particle">🍒</div>
        <div class="cherry-particle">🍒</div>
        <div class="cherry-particle">🍒</div>
        <div class="cherry-particle">🍒</div>
        <div class="cherry-particle">🍒</div>
        <div class="cherry-particle">🍒</div>
    </div>

    <!-- Header HTML Structure -->
    <div class="cherry-header-container">
        <div class="cherry-title">🍒 Cherry Travel Assistant</div>
        <div class="cherry-subtitle">Your sweet guide to unforgettable journeys and seamless adventures</div>
    </div>
    """,
    unsafe_allow_html=True,
)
query=st.text_input("Where are you planning to go ")
days=st.number_input("How many days trip you wnat to be planned ",min_value=1,max_value=30)
budget=st.selectbox("Select Budget",['Luxury','Intermediate','Budgeted'])
type=st.radio("Who You Are Traveling With",['Family','Friends','Solo'])

prompt=f'''You are travel assistant planner and you answer in professional way so the user is saying He/She 
has planned the trip to {query} for {days} days and has budget type {budget} and they are travling as a {type},answer this in bullet points anf at last you have to tell 5 
facts about the place the user has entered mainly focus on a bit paranomal facts ,***you should not ask any question to user again*** and give more detail format'''

if st.button("Plan Trip"):

    interaction=client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
        generation_config={
                    "temperature": 0.5,
                    "top_k": 50,
                    
                },
    )
    with st.spinner("Please Wait ....",show_time=True):
        time.sleep(5)
    st.success("Vola !!! Here is your trip planning ")
    st.write(interaction.output_text)


