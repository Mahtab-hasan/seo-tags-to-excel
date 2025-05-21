import os

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "./browsers"  # ✅ Correct placement

from flask import Flask, render_template, request, send_file, after_this_request
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd
import uuid
import logging

app = Flask(__name__)


def extract_tags_from_url(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            page.goto(url, timeout=60000)
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")
        data = []
        for tag_name in ["h1", "h2", "h3", "h4", "h5", "p"]:
            for tag in soup.find_all(tag_name):
                text = tag.get_text(strip=True)
                if text:
                    data.append({"Tag": tag_name, "Text": text})
                for span in tag.find_all("span"):
                    span_text = span.get_text(strip=True)
                    if span_text:
                        data.append({"Tag": f"{tag_name} > span", "Text": span_text})
        return data
    except Exception as e:
        app.logger.error(f"Error extracting tags: {str(e)}")
        return [{"Tag": "error", "Text": str(e)}]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "URL is required", 400

        data = extract_tags_from_url(url)
        df = pd.DataFrame(data)

        try:
            os.makedirs("temp", exist_ok=True)
            filename = f"seo_tags_{uuid.uuid4().hex}.xlsx"
            filepath = os.path.join("temp", filename)
            df.to_excel(filepath, index=False)
        except Exception as e:
            app.logger.error(f"File error: {str(e)}")
            return "Error generating file", 500

        @after_this_request
        def remove_file(response):
            try:
                os.remove(filepath)
            except Exception as e:
                app.logger.error(f"Cleanup error: {str(e)}")
            return response

        return send_file(filepath, as_attachment=True)

    return render_template("index.html")


if __name__ != "__main__":
    logging.basicConfig(level=logging.INFO)
