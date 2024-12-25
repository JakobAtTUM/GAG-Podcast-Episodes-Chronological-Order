# Geschichten aus der Geschichte - Podcast Episodes in chronologischer Reihenfolge (history podcast episodes in chronological order)

```bath
gewidmet meiner wunderbaren Mama
```


View the complete chronological episode list:
- View in Google Docs: https://docs.google.com/spreadsheets/d/1NTHLJ2dXjYzTl28tmD_aj-8g-lZU00N_I18T0v9nFoo/edit?usp=sharing
- ⚠️ As the episodes are automatically parsed using a Large Language Model using only their episode description, there will be errors in the dataset. If you notice errors, please leave a comment in my google sheets document so that I can change it.


## 📝 Technical Project Description
This project  creates a chronological ordering of the "Geschichten aus der Geschichte" (GAG) podcast episodes by analyzing episode descriptions using web crawling and Large Language Models (LLM). 

1. Crawls the podcast website (geschichte.fm) for episode episode descriptions and titles using beautiful soup
2. Determines keywords from the episode information and crawles the wikipedia page for additional information
3. Uses Google's Gemini LLM to determine the historical time period based on episode title, description and wikipedia context

The results are stored in episodes_data.csv. Episodes which were not sucessfully parsed are in errors_while_parsing.csv

## 🚀 Ideas for future contributions (please contribute to this project)
- Make the dates more robust using by incorporating additional data sources.
- Automatically update the episodes in the correct order to spotify.
- Use the dates to do some interesting data science.
- ... and many more, please feel free to make suggestions


🤝 Contributing
Contributions are welcome!

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

