import configparser
import google.generativeai as genai
import json
import re

def get_gemini_response(prompt: str, temperature: float = 0.3):
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

    # Configure generation parameters
    generation_config = {
        'temperature': temperature,
        'top_p': 1.0,
        'top_k': 1,
        'max_output_tokens': 40,
    }

    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    return response


def get_year_from_episode_information(text: str, max_reps: int = 3) -> dict:
    """
    Extracts historical dates from podcast episode descriptions using Gemini LLM.

    This function analyzes podcast episode descriptions to determine the historical
    time period being discussed. It makes multiple attempts with increasing
    temperature if the initial attempt fails to extract valid dates.

    Args:
        text (str): The podcast episode description text to analyze
        max_reps (int, optional): Maximum number of retry attempts. Defaults to 3

    Returns:
        dict: A dictionary containing:
            - 'start_date': The starting year in format '+/-YYYY'
            - 'end_date': The ending year in format '+/-YYYY'
            If dates cannot be determined, returns 'Unknown' for both values
    """

    # Define the prompt template for the LLM
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
            - Nehmen Sie nur fundierte Schätzung der Jahreszahlen vor, wenn sie den historischen Kontext gut einschätzen können.
            - Geben Sie Ihre Antwort im JSON-Format mit den Feldern „start_date“ und „end_date“ zurück.

        

        Please provide your answer ONLY in the following JSON format:
        {{
            "start_date": "YYYY", // The starting year of the historical event/period
            "end_date": "YYYY"    // The ending year of the historical event/period
        }}
        """


    # Format the prompt with the input text
    prompt = prompt_template.format(input_text=text)

    # Initial attempt to get dates
    try:
        response = get_gemini_response(prompt, temperature=0.3)
        response_data = json.loads(response.text)
    except json.JSONDecodeError:
        response_data = {
            "start_date": "Unknown",
            "end_date": "Unknown"
        }

    # Regex pattern for valid date format (+/-YYYY)
    valid_date_pattern = r'^[+-]\d{4}$'

    # Retry logic if start_date is not in correct format
    if not re.match(valid_date_pattern, str(response_data['start_date'])):
        for attempt in range(max_reps):
            print(f"Date extraction attempt {attempt + 1}/{max_reps}")

            # Increase temperature with each attempt (max 1.0)
            temperature = min(0.3 + 0.1 * attempt, 1.0)

            try:
                response = get_gemini_response(prompt, temperature)
                response_data = json.loads(response.text)

                # Check if we got a valid date
                if re.match(valid_date_pattern, str(response_data['start_date'])):
                    print(f"Successfully extracted dates: {response_data}")
                    return response_data

            except json.JSONDecodeError:
                continue

        # If all attempts fail, return unknown dates
        print(f"Unable to extract any dates.")
        response_data = {
            "start_date": "Unknown",
            "end_date": "Unknown"
        }
        return response_data
    else:
        return response_data

def get_year_from_episode_informationOld(text, max_reps = 3):
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
            - Nehmen Sie nur fundierte Schätzung der Jahreszahlen vor, wenn sie den historischen Kontext gut einschätzen können.
            - Geben Sie Ihre Antwort im JSON-Format mit den Feldern „start_date“ und „end_date“ zurück.

        

        Please provide your answer ONLY in the following JSON format:
        {{
            "start_date": "YYYY", // The starting year of the historical event/period
            "end_date": "YYYY"    // The ending year of the historical event/period
        }}
        """

        prompt = prompt_template.format(input_text=text)

        try:
            # Parse the response as JSON
            response = get_gemini_response(prompt, 0.3)
            response = json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback in case the response isn't proper JSON
            response = {
                "start_date": "Unknown",
                "end_date": "Unknown"
            }

        # Retry LLM call up to max_reps times if date is unknown, to see if it guesses a valid date with multiple trials
        # Increases Model Temperature with each guess up to 1
        if not re.match(r'^[+-]\d{4}$', str(response['start_date'])):
            for i in range(max_reps):
                print(f"Did not find start_date for attempt number {i}/{max_reps}; trying again")
                response = get_gemini_response(prompt, min(0.3 + 0.1*i, 1))
                if re.match(r'^[+-]\d{4}$', str(response['start_date'])):
                    print(f"Did find start_date; updated year result to: {response}")
                    return response
                response = {
                    "start_date": "Unknown",
                    "end_date": "Unknown"
                }
        return response



def get_wikipedia_search_term_from_episode_information(text):
    prompt_template = """
    Ihre Aufgabe ist es, den wichtigsten historischen Suchbegriff aus einer Podcast-Episodenbeschreibung zu extrahieren.
    Dieser Suchbegriff soll genutzt werden, um der den relevantesten Wikipedia-Artikel zu finden. 

    Anweisungen zur Bearbeitung der Episodenbeschreibung:
    1. Identifizieren Sie das zentrale historische Thema, die Person, das Ereignis oder das Konzept
    2. Bevorzugen Sie spezifische Eigennamen gegenüber allgemeinen Begriffen
    3. Wenn mehrere Begriffe existieren, wählen Sie den historisch bedeutendsten aus
    4. Geben Sie nur den Suchbegriff in deutscher Sprache zurück, da er für die deutsche Wikipedia verwendet wird
    5. Fügen Sie keinen erklärenden Text oder mehrere Optionen ein.

    Beispiel 1:
    Input: „Frühes Mittelalter in Italien: Die Zeiten sind rau, alle wollen ein Stück vom Kuchen des ehemaligen weströmischen Reichs abhaben. Einer von ihnen ist Alboin, Langobardenkönig. Und wie so oft, war auch ihm kein Greisenalter vergönnt.“
    Output: „Alboin“
    
    Input: "Mit Kind und Kegel: Wer oder was ist eigentlich der »Kegel«? In diesem Zeitsprung gehen wir dieser Frage nach, sehen uns einen dieser Kegel genauer an und reisen gemeinsam von Regensburg nach Madrid und Brüssel. Wieder mal mit der großartigen stimmlichen Unterstützung\xa0von Martin Hemmer.'
    Output: "Kind und Kegel"

    Analysieren Sie nun bitte die folgende Episodenbeschreibung und antworten Sie mit einen einzelnen Suchbegriff:

    {input_text}
    """
    prompt = prompt_template.format(input_text=text)


    try:
        # Parse the response as JSON
        response = get_gemini_response(prompt, 0.2)
        response = response.candidates[0].content.parts[0].text.strip()
        return response
    except Exception as e:
        # Fallback in case the response isn't proper JSON
        return None



