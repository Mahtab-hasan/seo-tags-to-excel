from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd
import os
import uuid

app = Flask(__name__)

def extract_tags_from_url(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            page.goto(url, timeout=60000)
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, 'html.parser')
        data = []
        for tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'p']:
            for tag in soup.find_all(tag_name):
                text = tag.get_text(strip=True)
                if text:
                    data.append({'Tag': tag_name, 'Text': text})
                for span in tag.find_all('span'):
                    span_text = span.get_text(strip=True)
                    if span_text:
                        data.append({'Tag': f'{tag_name} > span', 'Text': span_text})
        return data
    except Exception as e:
        return [{'Tag': 'error', 'Text': str(e)}]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        data = extract_tags_from_url(url)
        df = pd.DataFrame(data)
        os.makedirs("temp", exist_ok=True)
        filename = f"seo_tags_{uuid.uuid4().hex}.xlsx"
        filepath = os.path.join("temp", filename)
        df.to_excel(filepath, index=False)
        return send_file(filepath, as_attachment=True)

    return render_template("index.html")

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
