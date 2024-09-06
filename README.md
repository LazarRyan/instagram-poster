# Instagram News Poster

## Description
This project is an automated system that scrapes news from reputable sources, generates summaries using AI, and posts them to Instagram. It's designed to keep followers informed about current events through concise, AI-generated summaries paired with a consistent visual template.

## Features
- Scrapes news from multiple sources (currently Al Jazeera and NPR)
- Generates summaries using OpenAI's GPT model
- Posts news summaries to Instagram with a custom image
- Fallback to a simple summary generation if AI summarization fails
- Robust error handling and logging

## Requirements
- Python 3.7+
- Instagram Account
- OpenAI API Key

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
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   INSTAGRAM_USERNAME=your_instagram_username
   INSTAGRAM_PASSWORD=your_instagram_password
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Place your custom `news_image.jpg` in the project root directory.

## Usage

Run the script with:
python3 app.py
 
The script will:
1. Scrape the latest news from configured sources
2. Select a random news item
3. Generate a summary using OpenAI's GPT model
4. Create an Instagram post with the summary and the custom image
5. Post to Instagram

## Configuration

You can modify the `SOURCES` list in the script to add or remove news sources. Each source requires specific configuration for web scraping.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/lazarryan/instagram-poster/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Disclaimer

This project is for educational purposes only. Ensure you comply with the terms of service of all APIs and websites used in this project.
