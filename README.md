# AI-Powered Brand Identity Generator

This project generates complete brand packages (logos, color schemes, fonts, taglines) based on company descriptions and target demographics using Gemini 2.0 Flash API and Streamlit.

## Features
- Streamlit web UI for user input
- AI-powered generation of:
  - Logos (placeholder or AI-generated)
  - Color schemes
  - Font suggestions
  - Taglines
- Easy export of brand assets

## Setup
1. Install dependencies:
   ```sh
   pip install streamlit google-generativeai
   ```
2. Run the app:
   ```sh
   streamlit run app.py
   ```

## Configuration
- You will need access to the Gemini 2.0 Flash API and an API key.
- Set your API key as an environment variable or directly in the code (not recommended for production).

## Notes
- Logo generation may use placeholder images if image generation is not available via the API.
- Fonts are suggested from Google Fonts.
