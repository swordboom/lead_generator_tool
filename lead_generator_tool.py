import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from ml_model import predict_email_deliverability


def get_tech_stack(domain):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(f"https://{domain}")
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        tech_stack = set()

        for script in soup.find_all('script', src=True):
            src = script['src'].lower()
            if 'cloudflare' in src: tech_stack.add('Cloudflare')
            if 'bootstrap' in src: tech_stack.add('Bootstrap')
            if 'react' in src: tech_stack.add('React')
            if 'vue' in src: tech_stack.add('Vue.js')
            if 'angular' in src: tech_stack.add('Angular')
            if 'jquery' in src: tech_stack.add('jQuery')
            if 'next' in src: tech_stack.add('Next.js')
            if 'tailwind' in src: tech_stack.add('Tailwind CSS')

        for link in soup.find_all('link', href=True):
            href = link['href'].lower()
            if 'bootstrap' in href: tech_stack.add('Bootstrap')
            if 'font-awesome' in href or 'fontawesome' in href: tech_stack.add('Font Awesome')

        driver.quit()
        return ', '.join(sorted(tech_stack)) if tech_stack else 'Unknown'

    except Exception as e:
        driver.quit()
        print(f"❌ Error scraping tech stack for {domain}: {e}")
        return 'Error'


def score_linkedin_activity(linkedin_url):
    try:
        import requests
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(linkedin_url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        followers = soup.find(text=lambda x: 'followers' in x.lower())
        if followers:
            number = ''.join([c for c in followers if c.isdigit()])
            return int(number)
        return 0
    except:
        return 0


def try_email_patterns(domain):
    patterns = [
        f"info@{domain}",
        f"contact@{domain}",
        f"support@{domain}",
        f"hello@{domain}",
        f"team@{domain}"
    ]
    for email in patterns:
        prediction = predict_email_deliverability(email)
        if prediction == 'likely_valid':
            return email, prediction
    return patterns[0], 'likely_invalid'  # fallback to first tried email


def enrich_leads(rows):
    enriched_rows = []
    for row in rows:
        domain = row.get('Domain', '')
        try:
            guessed_email, ml_pred = try_email_patterns(domain)
            tech_stack = get_tech_stack(domain)
            linkedin_url = row.get('LinkedIn URL', '')
            engagement_score = score_linkedin_activity(linkedin_url)
            if engagement_score == 0:
                engagement_score = len(domain) * 5  # fallback logic

            row['Email Used'] = guessed_email
            row['Tech Stack'] = tech_stack
            row['Engagement Score'] = engagement_score
            row['ML Deliverability'] = ml_pred

        except Exception as e:
            row['Email Used'] = 'N/A'
            row['Tech Stack'] = 'N/A'
            row['Engagement Score'] = 0
            row['ML Deliverability'] = 'unknown'
            print(f"❌ Failed for domain {domain}: {str(e)}")

        enriched_rows.append(row)
        time.sleep(1)

    return enriched_rows