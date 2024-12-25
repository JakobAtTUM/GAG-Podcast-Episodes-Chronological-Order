# Geschichten aus der Geschichte - Podcast Episodes in chronological Order

```bath
gewidmet meiner wunderbaren Mama
```

This project  creates a chronological ordering of the "Geschichten aus der Geschichte" (GAG) podcast episodes by analyzing episode descriptions using web crawling and Large Language Models (LLM).

View the complete chronological episode list:
- View in Google Docs: https://docs.google.com/spreadsheets/d/1NTHLJ2dXjYzTl28tmD_aj-8g-lZU00N_I18T0v9nFoo/edit?usp=sharing
- ⚠️ As the episodes are automatically parsed using a Large Language Model using only their episode description, there will be errors in the dataset. If you notice errors, please leave a comment in my google sheets document so that I can change it.

## 📝 Description

The "Geschichten aus der Geschichte" podcast presents historical episodes in a non-chronological order. This tool:
1. Crawls the podcast website (geschichte.fm)
2. Extracts episode descriptions
3. Uses Google's Gemini LLM to determine the historical time period

## 🚀 Ideas for future contributions (please contribute to this project)
- Make the dates more robust using RAG (Retrieval Agumented Generation) by incorporating additional data sources such as wikipedia or wikidata.
- Write functions to automatically update the episodes to spotify.
- Use the dates to do some interesting data science.
- ... and many more, please feel free to make suggestions

## 📋 Prerequisites

```python
# Required Python packages
requests>=2.31.0
beautifulsoup4>=4.12.2
pandas>=2.1.0
google-generativeai>=0.3.0
```

💻 Usage
Run the main script:
```bash
python main.py
```

This will:
Crawl all episodes from geschichte.fm
Extract relevant information
Determine historical dates using Gemini
Save the chronologically sorted episodes to output/episode_data.csv

Web Crawling: Fetches episode pages from geschichte.fm Extracts titles and descriptions using BeautifulSoup4
Date Extraction: Processes episode descriptions through Gemini LLM Uses few-shot learning for accurate date determination Handles BCE/CE date formats
Data Processing: Sorts episodes based on extracted dates Handles edge cases and uncertain datesExports results to CSV

📊 Output Format
The generated CSV file contains:
title: Episode title
summary: Episode description
year_from: Start year of the historical period (format: +/-YYYY)
year_until: End year of the historical period (format: +/-YYYY)

Data validation checks

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

