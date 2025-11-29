import os
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")  
DEFAULT_TIMEOUT = 20

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
]

def _requests_fallback(website, timeout=DEFAULT_TIMEOUT, tries=3):
    headers = {"User-Agent": USER_AGENTS[int(time.time()) % len(USER_AGENTS)]}
    session = requests.Session()
    retries = Retry(total=tries, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))
    try:
        resp = session.get(website, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        raise RuntimeError(f"Requests fallback failed: {exc}") from exc

# Local selenium using webdriver manager
def _selenium_local(website, timeout=DEFAULT_TIMEOUT, headless=True):
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
    except Exception as e:
        raise RuntimeError(
            "Local Selenium path requires selenium and webdriver-manager packages. "
            "Install them: pip install selenium webdriver-manager"
        ) from e

    opts = ChromeOptions()
    if headless:
         
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
 
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(website)
        time.sleep(1.0)  
        html = driver.page_source
        return html
    finally:
        try:
            driver.quit()
        except Exception:
            pass

# Remote / BrightData 
from selenium.webdriver import Remote

try:
    from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
    from selenium.webdriver import ChromeOptions
except Exception:
    ChromiumRemoteConnection = None
    ChromeOptions = None

def _selenium_via_brightdata(website, sbr_url, timeout=DEFAULT_TIMEOUT):
    if not sbr_url:
        raise ValueError("SBR_WEBDRIVER (remote webdriver URL) is not set.")
    if not isinstance(sbr_url, str) or not sbr_url.lower().startswith(("http://", "https://")):
        raise ValueError("SBR_WEBDRIVER must be a valid URL starting with http:// or https://")
    if ChromiumRemoteConnection is None:
        raise RuntimeError("selenium remote Chromium classes unavailable in this environment.")

    sbr_connection = ChromiumRemoteConnection(sbr_url, "goog", "chrome")
    opts = ChromeOptions()
    with Remote(sbr_connection, options=opts) as driver:
        driver.set_page_load_timeout(timeout)
        driver.get(website)
        try:
            solve_res = driver.execute(
                "executeCdpCommand",
                {"cmd": "Captcha.waitForSolve", "params": {"detectTimeout": 10000}},
            )
            print("Captcha solve status:", solve_res.get("value", {}).get("status"))
        except Exception:
            pass
        html = driver.page_source
        return html

# Public API
def scrape_website(website, method="auto", sbr_override=None):
    """
    method: "auto" | "requests" | "local_selenium" | "brightdata_remote"
    sbr_override: optional override URL for remote webdriver
    """
    if not website:
        raise ValueError("website is empty")

    method = (method or "auto").lower()
    sbr_url = sbr_override if sbr_override else SBR_WEBDRIVER

    # Direct method choices:
    if method == "requests":
        return _requests_fallback(website)
    if method == "local_selenium":
        return _selenium_local(website)
    if method == "brightdata_remote":
        return _selenium_via_brightdata(website, sbr_url)

    # auto flow: try requests -> local_selenium -> brightdata
    try:
        return _requests_fallback(website)
    except Exception as e_req:
        print("Requests fallback failed, trying local selenium:", e_req)

    try:
        return _selenium_local(website)
    except Exception as e_local:
        print("Local selenium failed, trying remote (BrightData) if configured:", e_local)

    if sbr_url:
        try:
            return _selenium_via_brightdata(website, sbr_url)
        except Exception as e_remote:
            print("Remote BrightData attempt failed:", e_remote)

    raise RuntimeError(
        "All scraping methods failed. Ensure the page is reachable, or choose a simpler method (requests). "
        "If you want to use BrightData, set SBR_WEBDRIVER in .env or provide an override."
    )

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]
