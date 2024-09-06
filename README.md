# Instagram News Poster

## Description
This project is an automated system that scrapes news from reputable sources, generates summaries using OpenAI's GPT model, and posts them to Instagram. It's designed to keep followers informed about current events through concise, AI-generated summaries paired with a consistent visual template.

## Features
- Scrapes news from Al Jazeera and NPR
- Generates summaries using OpenAI's GPT-3.5-turbo model
- Posts news summaries to Instagram with a custom image
- Fallback to a simple summary generation if AI summarization fails
- Robust error handling and logging
- Uses a pre-made image for consistent branding

## Requirements
- Python 3.7+
- Instagram Account
- OpenAI API Key
- Custom news image (news_image.jpg)

## Dependencies
- requests
- beautifulsoup4
- pandas
- instagrapi
- openai

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/lazarryan/instagram-poster.git
   cd instagram-poster
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install requests beautifulsoup4 pandas instagrapi openai
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Place your custom `news_image.jpg` in the project root directory.

## Configuration

The script uses two news sources by default:

1. Al Jazeera (https://www.aljazeera.com/news/)
2. NPR (https://www.npr.org/sections/news/)

You can modify the `SOURCES` list in the script to add or remove news sources. Each source requires specific configuration for web scraping:

python
SOURCES = [
{
'name': 'Source Name',

'url': 'https://source.url/news',

'base_url': 'https://source.url',

'article_tag': 'article',

'article_class': 'article-class',

'title_tag': 'h2',

'title_class': 'title-class'
},
# Add more sources here if needed

## Usage

Run the script with:
python3 app.py

The script will:
1. Scrape the latest news from configured sources
2. Select a random news item
3. Generate a summary using OpenAI's GPT-3.5-turbo model
4. Create an Instagram post with the summary and the custom image
5. Post to Instagram

## Key Functions

- `scrape_news(sources)`: Scrapes news from the configured sources
- `generate_summary_and_insights(title, link)`: Generates a summary using OpenAI's GPT model
- `fallback_summary(title, link)`: Provides a simple summary if AI generation fails
- `post_to_instagram(img_path, caption)`: Posts the news summary to Instagram
- `use_premade_news_image()`: Retrieves the path of the custom news image

## Error Handling and Logging

The script includes comprehensive error handling and logging. Check the console output or log files for information about the script's execution, including any errors or warnings.

## Customization

- To change the AI model or adjust the summary generation, modify the `generate_summary_and_insights` function.
- To change the image used for posts, replace `news_image.jpg` with your desired image (keeping the same filename).
- Adjust the `max_caption_length` in the `main` function to change the maximum length of Instagram captions.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/lazarryan/instagram-poster/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Disclaimer

This project is for educational purposes only. Ensure you comply with the terms of service of all APIs and websites used in this project, including Instagram, OpenAI, and the news sources you scrape from.
