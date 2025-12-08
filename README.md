# AI-Web-Scraper

A Streamlit-based web scraping + parsing app that combines multiple scraping strategies (requests, local Selenium, BrightData remote) with LangChain + Ollama for extracting structured information from web pages.

## Table of Contents

+ Features
+ Technologies Used
+ Quick Start
+ Full Setup & Installation
  1. Clone repository
  2. Create a Python virtual environment (recommended)
  3. Install required Python libraries
  4. Install Ollama and pull a model (Windows & macOS)
+ Screenshots of Project (Input & Output)
+ License

## Features 

- Multi-strategy scraping: requests (fast), local_selenium (JS rendering), brightdata_remote (remote Chromium).
- Robust requests fallback with user-agent rotation and retry/backoff.
- Local Selenium uses webdriver-manager to auto-download a compatible ChromeDriver.
- Ollama-based parsing via LangChain (configurable model via env or UI).
- Streamlit UI with method selection, error messages, parsed output download, and token  estimate.
- Graceful fallbacks — app won’t crash if BrightData or local ChromeDriver is not configured.


## Technologies Used

+ Python 3.9+ (recommended)
+ Streamlit — frontend UI
+ Selenium + webdriver-manager — local browser automation
+ Requests, BeautifulSoup (bs4), lxml, html5lib — HTML fetching & parsing
+ LangChain + langchain_ollama — prompt/LLM orchestration
+ Ollama (local model runtime) — LLM inference
+ python-dotenv — environment variable loading
+ concurrent.futures — parallel parsing for performance
+ webdriver-manager — automatic chromedriver handling

## Quick Start

1. Create virtualenv and install deps:
```python
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows (PowerShell/CMD)
pip install -r requirements.txt
pip install webdriver-manager requests
```
2. Install Ollama and pull a model.
3. Copy `.env.example` to `.env` and update `OLLAMA_MODEL` (e.g., `llama3.2`) and `SBR_WEBDRIVER` if using BrightData.
4. Run the app:
   ```bash
   streamlit run main.py
   ```

## Full Setup & Installation

1. Clone repository
   ```bash
   git clone "https://github.com/SairamCh01/AI-Web-Scraper"
   cd <repo-folder>
   ```
2. Create a Python virtual environment (recommended)
   ```python
   python -m venv venv
   # macOS / Linux
   source venv/bin/activate
   # Windows (PowerShell)
   venv\Scripts\Activate.ps1
   # or Windows (CMD)
   venv\Scripts\activate
   ```
3. Install required Python Libraries
   Make sure `requirements.text` contains the project package. Example recommended  `requirement.txt` entries:
  ```bash
  streamlit
  langchain
  langchain_ollama
  selenium
  webdriver-manager
  beautifulsoup4
  lxml
  html5lib
  python-dotenv
  requests
  ```
  Install them: 
  ```python
  pip install -r requirements.txt
  # ensure webdriver-manager & requests present
  pip install webdriver-manager requests
  ```
**Note:** If you already have some packages installed, pip will skip reinstallation. If you run into compatibility issues, consider creating a fresh virtual environment.

4. Install Ollama and pull a model (Windows & macOS0)
  Important: Ollama is developed independently; always prefer the official installation instructions from the Ollama website if they change. The steps below provide a practical approach.

**For macOS:**

i. Install Ollama (recommended via Homebrew):
   ```bash
   brew install ollama
   ```
   Or follow the official macOS installer provided by Ollama.
   
ii. Pull a model (example uses llama3.2 — change to the exact model name you want):
  ```bash
  ollama pull llama3.2
  ```

iii. Verify model is installed and available:
  ```bash
  ollama ls
  ```
  You should see llama3.2 in the list.

** For Windows: **

i. Download and install Ollama for Windows using the official Windows installer available on the Ollama website. If you prefer a WSL setup, you can install Ollama inside WSL following Linux instructions.

ii. After installation, open a PowerShell/Command Prompt and pull the model:
   ```bash
   ollama pull llama3.2
   ```

iii. Verify:
  ```bash
  ollama ls
  ```

**Common checks**: 

+ If ollama ls does not list your model, adjust the model name and re-run ollama pull <model-name>.
+ In the Streamlit UI you can override the model name (input labeled Ollama Model (select model installed on your device)). Ensure you match the exact model name visible in ollama ls.

## Screenshots (Input & Output)
**Input:** What is Java ? 
<img width="1508" height="941" alt="image" src="https://github.com/user-attachments/assets/271f88e2-1e55-4a5c-9fd4-e3e18261582f" />
<img width="1902" height="935" alt="image" src="https://github.com/user-attachments/assets/19be47b1-960f-462e-97eb-19f2ae33106d" />
**Output:**
<img width="1868" height="901" alt="image" src="https://github.com/user-attachments/assets/291e159a-60ad-417b-bc29-6fdb79bcf457" />
<img width="1918" height="932" alt="image" src="https://github.com/user-attachments/assets/660e390e-de18-4002-9e67-6e7af31489c6" />




## License 
MIT License

Copyright (c) 2025 C H Sairam

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.                           

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



