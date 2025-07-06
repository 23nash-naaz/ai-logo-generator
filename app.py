import streamlit as st
import google.generativeai as genai
import json
import re
from typing import Dict, List
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




# Configure the page
st.set_page_config(
    page_title="BrandZ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, responsive, and aesthetic UI
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Roboto:wght@400;500&display=swap');
    .stApp {
        background: linear-gradient(120deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        min-height: 100vh;
        font-family: 'Roboto', sans-serif;
    }
    .main-card {
        background: #ffffffcc;
        border-radius: 18px;
        box-shadow: 0 4px 24px 0 rgba(80, 112, 255, 0.10);
        padding: 2.5rem 2.5rem 2rem 2.5rem;
        margin-bottom: 2.5rem;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #2d3a4a !important;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6a82fb 0%, #fc5c7d 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.7rem 2.2rem;
        margin-top: 1rem;
        transition: 0.2s;
        font-family: 'Montserrat', sans-serif;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #fc5c7d 0%, #6a82fb 100%);
        color: #fff;
        box-shadow: 0 2px 8px 0 rgba(80, 112, 255, 0.15);
    }
    .stTextInput > div > input, .stTextArea > div > textarea {
        border-radius: 8px;
        border: 1.5px solid #6a82fb;
        background: #f5f7fa;
        font-size: 1rem;
        color: #2d3a4a;
        font-family: 'Roboto', sans-serif;
    }
    .stDownloadButton > button {
        background: linear-gradient(90deg, #6a82fb 0%, #fc5c7d 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        margin-top: 1rem;
        font-family: 'Montserrat', sans-serif;
    }
    img {
        box-shadow: 0 4px 24px 0 rgba(80, 112, 255, 0.10);
        border-radius: 12px;
        margin-bottom: 1rem;
        background: #fff;
    }
    .stAlert {
        border-radius: 10px;
        background: #e3eafe;
        color: #2d3a4a;
    }
    @media (max-width: 900px) {
        .main-card { padding: 1.2rem 0.5rem 1rem 0.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Gemini API
@st.cache_resource
def initialize_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

def extract_logo_image_from_response(response_text: str) -> str:
    """Extract base64-encoded SVG or PNG image from Gemini response text."""
    # Look for a base64-encoded image (SVG or PNG)
    svg_match = re.search(r'data:image/svg\+xml;base64,([A-Za-z0-9+/=\n]+)', response_text)
    png_match = re.search(r'data:image/png;base64,([A-Za-z0-9+/=\n]+)', response_text)
    if svg_match:
        return f"data:image/svg+xml;base64,{svg_match.group(1)}"
    elif png_match:
        return f"data:image/png;base64,{png_match.group(1)}"
    return None

def generate_brand_identity(model, company_description: str, target_demographic: str, industry: str, brand_personality: str) -> Dict:
    """Generate complete brand identity using Gemini 2.0 Flash, including a logo image."""
    prompt = f"""
    You are a professional brand designer and marketing strategist. Create a comprehensive brand identity package for the following company:
    
    Company Description: {company_description}
    Target Demographic: {target_demographic}
    Industry: {industry}
    Brand Personality: {brand_personality}
    
    Please provide a complete brand identity package in JSON format with the following structure:
    {{
        "brand_name_suggestions": ["suggestion1", "suggestion2", "suggestion3"],
        "taglines": ["tagline1", "tagline2", "tagline3"],
        "color_palette": {{
            "primary": "#hexcode",
            "secondary": "#hexcode",
            "accent": "#hexcode",
            "neutral": "#hexcode",
            "text": "#hexcode"
        }},
        "color_psychology": "Explanation of color choices",
        "typography": {{
            "primary_font": "Font name and style",
            "secondary_font": "Font name and style",
            "font_rationale": "Why these fonts work"
        }},
        "logo_concepts": [
            {{
                "concept": "Logo concept 1",
                "description": "Detailed description",
                "style": "Design style"
            }},
            {{
                "concept": "Logo concept 2", 
                "description": "Detailed description",
                "style": "Design style"
            }},
            {{
                "concept": "Logo concept 3",
                "description": "Detailed description", 
                "style": "Design style"
            }}
        ],
        "brand_voice": {{
            "tone": "Brand tone description",
            "personality_traits": ["trait1", "trait2", "trait3"],
            "communication_style": "How the brand communicates"
        }},
        "brand_guidelines": {{
            "logo_usage": "Guidelines for logo usage",
            "color_usage": "Guidelines for color application",
            "typography_usage": "Guidelines for font usage",
            "imagery_style": "Style guide for images and graphics"
        }},
        "marketing_applications": {{
            "website_copy": "Sample homepage copy",
            "social_media_bio": "Sample social media bio",
            "elevator_pitch": "30-second brand pitch"
        }}
    }}
    
    Additionally, generate a simple, modern, and unique logo for this brand as a base64-encoded SVG or PNG image. Output the image as a data URI (e.g., data:image/svg+xml;base64,... or data:image/png;base64,...). Place the data URI immediately after the JSON, clearly labeled as 'LOGO_IMAGE:'.
    
    Make sure all hex codes are valid and the brand identity is cohesive and professional.
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                top_p=0.95,
                top_k=40,
                max_output_tokens=4000,
            )
        )
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        logo_image = extract_logo_image_from_response(response.text)
        if json_match:
            result = json.loads(json_match.group())
            if logo_image:
                result["generated_logo_image"] = logo_image
            return result
        else:
            return {"error": "Could not parse brand identity response"}
    except Exception as e:
        return {"error": f"Error generating brand identity: {str(e)}"}

def display_color_palette(colors: Dict):
    """Display color palette with visual swatches"""
    st.subheader("🎨 Color Palette")
    
    cols = st.columns(len(colors))
    for i, (color_name, hex_code) in enumerate(colors.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background-color: {hex_code};
                height: 80px;
                border-radius: 10px;
                border: 2px solid #ddd;
                margin-bottom: 10px;
            "></div>
            <p style="text-align: center; margin: 0;">
                <strong>{color_name.title()}</strong><br>
                {hex_code}
            </p>
            """, unsafe_allow_html=True)

def display_logo_concepts(concepts: List[Dict]):
    """Display logo concepts"""
    st.subheader("💡 Logo Concepts")
    
    for i, concept in enumerate(concepts, 1):
        with st.expander(f"Concept {i}: {concept['concept']}"):
            st.write(f"**Style:** {concept['style']}")
            st.write(f"**Description:** {concept['description']}")

def main():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🧠 BrandZ")
    st.markdown("<p style='font-size:1.2rem;color:#6366f1;'>Generate unique, professional logos and brand assets with AI.</p>", unsafe_allow_html=True)
    
    # Check if API key is configured
    if GEMINI_API_KEY == "your_gemini_api_key_here":
        st.error("⚠️ Please add your Gemini API key in the code!")
        st.markdown("""
        ### How to add your API key:
        1. Get your API key from [Google AI Studio](https://makersuite.google.com/)
        2. Replace `'your_gemini_api_key_here'` with your actual API key in the code
        3. Save the file and refresh the page
        """)
        return
    
    # Initialize Gemini model
    try:
        model = initialize_gemini()
    except Exception as e:
        st.error(f"Failed to initialize Gemini API: {str(e)}")
        st.error("Please check your API key and try again.")
        return
    
    # Input form
    with st.form("brand_input_form"):
        st.subheader("📝 Company Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_description = st.text_area(
                "Company Description",
                placeholder="Describe your company, products/services, and mission...",
                height=100
            )
            
            target_demographic = st.text_input(
                "Target Demographic",
                placeholder="e.g., Young professionals, families, tech enthusiasts..."
            )
        
        with col2:
            industry = st.selectbox(
                "Industry",
                ["Technology", "Healthcare", "Finance", "Education", "Retail", 
                 "Food & Beverage", "Travel", "Fashion", "Real Estate", "Other"]
            )
            
            brand_personality = st.multiselect(
                "Brand Personality",
                ["Professional", "Friendly", "Innovative", "Trustworthy", "Playful",
                 "Luxury", "Minimalist", "Bold", "Caring", "Energetic"],
                default=["Professional", "Trustworthy"]
            )
        
        submitted = st.form_submit_button("🚀 Generate Brand Identity", use_container_width=True)
    
    # Generate and display results
    if submitted:
        if not company_description or not target_demographic:
            st.error("Please fill in all required fields.")
            return
        
        with st.spinner("🤖 Generating your brand identity using Gemini 2.0 Flash... This may take a moment."):
            try:
                brand_identity = generate_brand_identity(
                    model, 
                    company_description, 
                    target_demographic, 
                    industry, 
                    ", ".join(brand_personality)
                )
            except Exception as e:
                st.error(f"Error calling Gemini API: {str(e)}")
                st.error("Please check your API key and internet connection.")
                return
        
        if "error" in brand_identity:
            st.error(brand_identity["error"])
            return
        
        # Display results
        st.success("✅ Brand identity generated successfully using Gemini 2.0 Flash!")
        
        # Display API usage info
        st.info("💡 Generated using Google's Gemini 2.0 Flash API")
        
        # Brand Name Suggestions
        if "brand_name_suggestions" in brand_identity:
            st.subheader("🏢 Brand Name Suggestions")
            cols = st.columns(3)
            for i, name in enumerate(brand_identity["brand_name_suggestions"]):
                with cols[i % len(cols)]:
                    st.info(name)
        
        # Taglines
        if "taglines" in brand_identity:
            st.subheader("✨ Tagline Options")
            for tagline in brand_identity["taglines"]:
                st.write(f"• *{tagline}*")
        
        # Color Palette
        if "color_palette" in brand_identity:
            display_color_palette(brand_identity["color_palette"])
            
            if "color_psychology" in brand_identity:
                st.write(f"**Color Psychology:** {brand_identity['color_psychology']}")
        
        # Typography
        if "typography" in brand_identity:
            st.subheader("🔤 Typography")
            typo = brand_identity["typography"]
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Primary Font:** {typo.get('primary_font', 'N/A')}")
            with col2:
                st.write(f"**Secondary Font:** {typo.get('secondary_font', 'N/A')}")
            
            if "font_rationale" in typo:
                st.write(f"**Rationale:** {typo['font_rationale']}")
        
        # Logo Concepts
        if "logo_concepts" in brand_identity:
            display_logo_concepts(brand_identity["logo_concepts"])
        
        # Brand Voice
        if "brand_voice" in brand_identity:
            st.subheader("🗣️ Brand Voice")
            voice = brand_identity["brand_voice"]
            st.write(f"**Tone:** {voice.get('tone', 'N/A')}")
            st.write(f"**Personality Traits:** {', '.join(voice.get('personality_traits', []))}")
            st.write(f"**Communication Style:** {voice.get('communication_style', 'N/A')}")
        
        # Marketing Applications
        if "marketing_applications" in brand_identity:
            st.subheader("📢 Marketing Applications")
            marketing = brand_identity["marketing_applications"]
            
            tabs = st.tabs(["Website Copy", "Social Media Bio", "Elevator Pitch"])
            
            with tabs[0]:
                st.write(marketing.get("website_copy", "N/A"))
            
            with tabs[1]:
                st.write(marketing.get("social_media_bio", "N/A"))
            
            with tabs[2]:
                st.write(marketing.get("elevator_pitch", "N/A"))
        
        # Brand Guidelines
        if "brand_guidelines" in brand_identity:
            st.subheader("📋 Brand Guidelines")
            guidelines = brand_identity["brand_guidelines"]
            
            with st.expander("View Complete Brand Guidelines"):
                st.write(f"**Logo Usage:** {guidelines.get('logo_usage', 'N/A')}")
                st.write(f"**Color Usage:** {guidelines.get('color_usage', 'N/A')}")
                st.write(f"**Typography Usage:** {guidelines.get('typography_usage', 'N/A')}")
                st.write(f"**Imagery Style:** {guidelines.get('imagery_style', 'N/A')}")
        
        # Download option
        st.subheader("💾 Download Brand Identity")
        brand_json = json.dumps(brand_identity, indent=2)
        st.download_button(
            label="Download as JSON",
            data=brand_json,
            file_name="brand_identity.json",
            mime="application/json",
            use_container_width=True
        )
        
        # Logo download
        if "generated_logo_image" in brand_identity:
            st.subheader("🖼️ Generated Logo")
            st.image(brand_identity["generated_logo_image"], caption="AI-Generated Logo", use_container_width=True, width=256)
            st.download_button(
                label="Download Logo Image",
                data=brand_identity["generated_logo_image"],
                file_name="brand_logo.txt",  # User can rename to .svg or .png as needed
                mime="text/plain",
                use_container_width=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
