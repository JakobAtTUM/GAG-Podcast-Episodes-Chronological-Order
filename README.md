# Geschichten aus der Geschichte - Podcast Episoden in chronologischer Reihenfolge 


Ihr könnt jetzt die Geschichten aus der Geschichte Episoden in chronologischer Reihenfolge hören! Mithilfe der Episodenbeschreibung, Wikipedia und Künstlicher Intelligent habe ich automatisiert ein Jahresdatum für Anfangs- und Enddaten der Folgen generiert. Wie immer bei KI Anwendungen können sich Fehler in die Ergebnisse eingeschlichen haben, ich freue mich wenn ihr bemerkte Fehler meldet.

- In dieser Google Docs Tabelle sind die Episoden nach Reihenfolge sortiert: https://docs.google.com/spreadsheets/d/1NTHLJ2dXjYzTl28tmD_aj-8g-lZU00N_I18T0v9nFoo/edit?usp=sharing

- In dieser Playlist auf Spotify könnt ihr die Episoden chronolgisch sortiert hören: [currently not available] 

# German history Podcast 'Geschichten aus der Geschichte' episodes in chronological order

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

