import configparser
import google.generativeai as genai
import json

def get_gemini_response(prompt: str, temperature: float = 1) -> dict:
    """
    Send a prompt to Gemini Pro and get response

    Args:
        prompt (str): The input text prompt
        temperature (float): Controls randomness (0.0 to 1.0)
                           0.0 = focused/deterministic
                           1.0 = more creative/random
    """

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Set up your Spotify API credentials from the config file
    api_key = config['gemini']['api_key']
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    # Modify the prompt to explicitly request structured output
    structured_prompt = f"""
    {prompt}

    Please provide your answer ONLY in the following JSON format:
    {{
        "start_date": "YYYY", // The starting year of the historical event/period
        "end_date": "YYYY"    // The ending year of the historical event/period
    }}
    """

    # Configure generation parameters
    generation_config = {
        'temperature': temperature,
        'top_p': 1.0,
        'top_k': 1,
        'max_output_tokens': 2048,
    }

    response = model.generate_content(
        structured_prompt,
        generation_config=generation_config
    )

    try:
        # Parse the response as JSON
        result = json.loads(response.text)
        return result
    except json.JSONDecodeError:
        # Fallback in case the response isn't proper JSON
        return {
            "start_date": "Unknown",
            "end_date": "Unknown"
        }


def create_prompt(text):
        prompt_template = """
        Sie sind ein Spezialist für die Extraktion historischer Daten. Ihre Aufgabe ist es, die Beschreibungen von Podcast-Episoden zu analysieren und den Zeitraum zu bestimmen, über den gesprochen wird. Bitte geben Sie die Anfangs- und Enddaten der erwähnten historischen Ereignisse oder Zeiträume an.

        Regeln:
        1. Verwenden Sie immer das Format +YYYY für Jahreszahlen (z. B. +1789 statt „18. Jahrhundert“ oder „1700er“)
        2. Wenn keine genauen Daten genannt werden, nutzen Sie Ihr Wissen, um eine fundierte Schätzung vorzunehmen.
        3. Wenn ein einjähriges Ereignis erwähnt wird, verwenden Sie dasselbe Jahr als Anfangs- und Enddatum.
        5. Wenn eine Zeitspanne nur grob angegeben ist, z.B. Mittelalter oder altes Ägypten, dann wähle die Zeitspanne für das Mittelalter oder alte Ägypten aus.

        Hier sind einige Beispiele:

        Beispiel 1:
        Input: "Wir springen in dieser Folge ins Jahr 53 vdZw., als sich in einer Ebene in Mesopotamien zwei Heere gegenüber stehen. Auf der einen Seite das des Partherreichs, angeführt von Surena, auf der anderen eines der Römischen Republik, angeführt von M. Licinius Crassus. Wir werden in dieser Folge über diese Schlacht, die Osterweiterung Roms und die Folgen der Schlacht für die Römische Republik sprechen."
        Output: {{"start_date": "-0053", "end_date": "-0053"}}

        Beispiel 2:
        Input: "Im November 1532 nehmen spanische Konquistadoren unter dem Kommando von Francisco Pizarro den letzten König der Inka gefangen: Atahualpa. Dabei gelangen sie an Unmengen Gold und Silber. Spätestens jetzt sind viele Konquistadoren überzeugt, dass die Gerüchte um ein sagenumwobenes Goldland wahr sind. Liegen die Ursprünge der Eldorado-Legende vielleicht bei einem kleinen Bergsee bei Guatavita im heutigen Kolumbien? Wir sprechen in der Folge über deutsche Konquistadoren, die sich für die Welser in Klein-Venedig auf die Jagd nach Eldorado machten und über Philipp von Hutten, den Generalkapitän Venezuelas, dessen Goldsuche auf tragische Weise endete – ohne Goldfund."
        Output: {{"start_date": "+1532", "end_date": "+1532"}}

        Beispiel 3:
        Input: "Wir springen diesmal in die 2. Hälfte des 18. Jahrhunderts. Automaten, also mechanische Konstrukte, die selbständig jene Dinge tun, die eigentlich lebenden Wesen vorbehalten waren, sind gerade der große Renner. Und auch in Wien konstruiert der Beamte Wolfgang von Kempelen einen solchen Automaten um die Kaiserin zu beeindrucken. Wir sprechen über diesen Automaten – den Schachtürken – und die Erfolge, die er bald darauf in ganz Europa feiern wird. Doch der faszinierende Automat birgt ein Geheimnis, das die Menschen selbst lang nach dem Ableben seines Erschaffers beschäftigen wird."
        Output: {{"start_date": "+1750", "end_date": "+1800"}}
        
        Beispiel 4:
        Input: "Wir springen nach Amsterdam: 1661 beginnt dort der Katholik Jan Hartmann, eine Kirche in sein Grachtenhaus zu bauen. Es entstand eine beeindruckende Kirche, die bis zum Ende des 19. Jahrhunderts genutzt wurde, ehe sie 1888 zu einem Museum wurde, das noch heute besucht werden kann: das Museum Ons’ Lieve Heer op Solder. Um zu klären, warum Jan Hartmann das gemacht hat, sprechen wir über eine faszinierende Zeit in der niederländischen Geschichte: Die Reformation, den Achtzigjährigen Krieg und das Goldene Zeitalter, in dem Amsterdam zu einer der bedeutendsten Städte der Welt wurde."
        Output: {{"start_date": "+1661", "end_date": "+1888"}}
        

        Analysieren Sie nun bitte die folgende Episodenbeschreibung und geben Sie den Zeitraum im gleichen Format an:

        {input_text}

        Denken Sie daran:
            - Geben Sie genaue Daten an, wenn sie klar angegeben sind.
            - Nehmen Sie fundierte Schätzungen auf der Grundlage des historischen Kontexts vor, wenn keine genauen Daten angegeben sind.
            - Geben Sie Ihre Antwort im JSON-Format mit den Feldern „start_date“ und „end_date“ zurück.
            - Nehmen Sie eine fundierte Schätzung vor, wenn keine Daten angegeben sind.

        """

        return prompt_template.format(input_text=text)



