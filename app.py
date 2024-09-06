import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import random
import time
import logging
from requests.exceptions import RequestException
from instagrapi import Client
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
INSTAGRAM_USERNAME = os.environ.get('INSTAGRAM_USERNAME', 'your_instagram_username')
INSTAGRAM_PASSWORD = os.environ.get('INSTAGRAM_PASSWORD', 'your_instagram_password')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'your_openai_api_key')

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# News sources configuration
SOURCES = [
    {
        'name': 'Al Jazeera',
        'url': 'https://www.aljazeera.com/news/',
        'base_url': 'https://www.aljazeera.com',
        'article_tag': 'article',
        'article_class': 'gc',
        'title_tag': 'h3',
        'title_class': 'gc__title'
    },
    {
        'name': 'NPR',
        'url': 'https://www.npr.org/sections/news/',
        'base_url': 'https://www.npr.org',
        'article_tag': 'article',
        'article_class': 'item',
        'title_tag': 'h2',
        'title_class': 'title'
    }
]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
]

def make_request_with_retries(url, max_retries=3):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except RequestException as e:
            if attempt == max_retries - 1:
                raise
            sleep_time = 2 ** attempt
            logging.warning(f"Request failed. Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)

def safe_find(element, tag, class_=None):
    try:
        if class_:
            return element.find(tag, class_=class_).text.strip()
        else:
            return element.find(tag).text.strip()
    except AttributeError:
        return None

def scrape_news(sources):
    news_items = []
    
    for source in sources:
        try:
            response = make_request_with_retries(source['url'])
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = soup.find_all(source['article_tag'], class_=source['article_class'])
            
            if not articles:
                logging.warning(f"No articles found for {source['name']}")
                continue
            
            for article in articles[:5]:
                title = safe_find(article, source['title_tag'], source['title_class'])
                if title:
                    link_element = article.find('a')
                    link = link_element['href'] if link_element else None
                    if link and not link.startswith('http'):
                        link = source['base_url'] + link
                    
                    if link:
                        news_items.append({
                            'source': source['name'],
                            'title': title,
                            'link': link
                        })
        except Exception as e:
            logging.error(f"Error scraping {source['name']}: {str(e)}")
        
        time.sleep(5)  # Wait 5 seconds between each source
    
    if not news_items:
        logging.warning("No news items were scraped. Check the website structures and network connection.")
    
    return pd.DataFrame(news_items)

def use_premade_news_image():
    img_path = "news_image.jpg"  # Ensure this image is in the same directory as your script
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"The image file '{img_path}' does not exist.")
    return img_path

def generate_summary_and_insights(title, link):
    try:
        prompt = f"Summarize the following news article in 3-4 sentences and provide 1-2 key insights or implications:\n\nTitle: {title}\nLink: {link}"
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles and provides insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        return fallback_summary(title, link)

def fallback_summary(title, link):
    domain = link.split('/')[2]
    return f"Breaking news from {domain}: {title}. This story is developing. Click the link to read the full article and stay informed on this important topic."

def post_to_instagram(img_path, caption):
    try:
        client = Client()
        client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        client.photo_upload(img_path, caption)
        logging.info("Successfully posted to Instagram")
    except Exception as e:
        logging.error(f"Error posting to Instagram: {str(e)}")

def main():
    news_df = scrape_news(SOURCES)
    
    if news_df.empty:
        logging.warning("No news items available. Skipping this run.")
        return
    
    selected_news = news_df.sample(n=1).iloc[0]  # Select one random news item
    
    summary_and_insights = generate_summary_and_insights(selected_news['title'], selected_news['link'])
    
    img_path = use_premade_news_image()
    
    max_caption_length = 2200  # Instagram's maximum caption length
    caption = f"{selected_news['title']}\n\n{summary_and_insights}\n\nSource: {selected_news['source']}\nRead more: {selected_news['link']}"
    if len(caption) > max_caption_length:
        truncated_length = max_caption_length - len(selected_news['title']) - len(selected_news['source']) - len(selected_news['link']) - 20
        summary_and_insights = summary_and_insights[:truncated_length] + "..."
        caption = f"{selected_news['title']}\n\n{summary_and_insights}\n\nSource: {selected_news['source']}\nRead more: {selected_news['link']}"
    
    post_to_instagram(img_path, caption)

if __name__ == "__main__":
    main()
    logging.info("Script completed. Waiting for the next run...")
