import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
from dotenv import load_dotenv
import os
import traceback
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("AI Web Scraper")

# Input Section
st.subheader("Scrape Website")

url = st.text_input(
    "Website URL  (sample: https://example.com)",
    value=""
)

# Tooltip Description
scrape_help = """
**Scraping Methods Explained:**

- **auto** – Automatically tries: requests → local_selenium → brightdata_remote  
- **requests** – Fastest, works for non-JS static sites  
- **local_selenium** – Uses your computer's Chrome to load JS-heavy sites  
- **brightdata_remote** – Uses BrightData remote browser (requires paid SBR link)
"""

col1, col2 = st.columns(2)

with col1:
    method = st.selectbox(
        "Scraping Method",
        ("auto", "requests", "local_selenium", "brightdata_remote"),
        help=scrape_help
    )

with col2:
    sbr_override = st.text_input(
        "BrightData WebDriver URL (optional)",
        value=os.getenv("SBR_WEBDRIVER", "")
    )

# SCRAPE BUTTON
if st.button("Scrape Site"):
    if not url:
        st.error("URL cannot be empty.")
    else:
        with st.spinner("Scraping..."):
            try:
                html = scrape_website(url, method=method, sbr_override=(sbr_override or None))
                body = extract_body_content(html)
                cleaned = clean_body_content(body)
                st.session_state.dom = cleaned
                st.success("Scraping completed successfully!")
            except Exception as e:
                st.error(f"Scraping failed: {e}")
                st.text_area("Traceback", traceback.format_exc(), height=250)


# Show Extracted Content

if "dom" in st.session_state:
    st.subheader("Extracted DOM Content (Full Text)")
    st.text_area("DOM Content (Full Extracted Text)", value=st.session_state.dom, height=300)

# Parsing Section
st.markdown("---")
st.subheader("Parse Extracted Content")

if "dom" not in st.session_state:
    st.info("Scrape a website first to enable parsing.")
else:
    parse_desc = st.text_area("Describe exactly what you want to extract:")

    model_choice = st.text_input(
        "Ollama Model (select model installed on your device)",
        value=os.getenv("OLLAMA_MODEL", "llama3.2")
    )

    if st.button("Parse Content"):
        if not parse_desc:
            st.error("Parse description cannot be empty.")
        else:
            with st.spinner("Parsing with Ollama... (optimized & faster)"):
                try:
                    # Split DOM into chunks
                    chunks = split_dom_content(st.session_state.dom)

                    def parse_chunk(chunk):
                        return parse_with_ollama([chunk], parse_desc, model_name=model_choice)

                    with ThreadPoolExecutor(max_workers=5) as executor:
                        results = list(executor.map(parse_chunk, chunks))

                    # Combine results
                    parsed_text = "\n".join(r["parsed_text"] for r in results)
                    est_tokens = sum(r["est_tokens"] for r in results)

                    st.success("Parsing completed ✔")
                    st.text_area("Parsed Output", parsed_text, height=250)
                    st.write(f"Estimated Tokens Used: **{est_tokens}**")

                    st.download_button(
                        "Download Parsed Result",
                        parsed_text.encode("utf-8"),
                        file_name="parsed_output.txt"
                    )

                except Exception as e:
                    st.error(f"Parsing failed: {e}")
                    st.text_area("Traceback", traceback.format_exc(), height=250)

# FOOTER
st.markdown(
    """
    <div style='position: fixed; right: 20px; bottom: 10px; font-size: 12px; opacity: 0.7;'>
        Developed by <b>C H Sairam</b>
    </div>
    """,
    unsafe_allow_html=True
)
