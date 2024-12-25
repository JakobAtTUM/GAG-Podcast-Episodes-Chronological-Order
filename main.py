"""
Web Crawler for Geschichte.fm Podcast Episodes
This module crawls podcast episodes from Geschichten aus der Geschichte (geschichte.fm), extracts episode information,
and determines the historical time period discussed in each episode using an LLM.

Dependencies:
    - llm_call: Contains functions for LLM prompt modification and Gemini API calls
    - website_crawler: Contains web scraping functionality
    - write_to_csv: Contains CSV writing utilities
"""
from llm_call import get_wikipedia_search_term_from_episode_information, get_year_from_episode_information
from website_crawler import extract_relevant_episode_data
from wikipedia_summary import get_wikipedia_summary
from write_to_csv import write_to_csv


def crawl_gag_episode(url: str):
    """
    Crawls a single podcast episode page and extracts relevant information.

    Args:
        url (str): The URL of the podcast episode to crawl

    Returns:
        dict: Dictionary containing episode data with keys:
            - title: Episode title
            - summary: Episode summary
            - year_from: Start year of historical period
            - year_until: End year of historical period
    """

    # Extract content from webpage
    print(f"Crawling from url: {url}")
    episode_information_dict = extract_relevant_episode_data(url=url)
    print(f"crawled episode information from GAG website: {episode_information_dict}")

    # searching for wikipedia context and adding context to the episode summary
    wikipedia_search_term = get_wikipedia_search_term_from_episode_information(str(episode_information_dict))
    print(f"wikipedia search term: {wikipedia_search_term}")


    try:
        wikipedia_summary = get_wikipedia_summary(wikipedia_search_term)
        print(f"wikipedia summary: {wikipedia_summary}")
        if wikipedia_summary is not None:
            episode_information_dict["Wikipedia-Informationen"] = str(wikipedia_summary)

        # Get time period prediction from LLM
        llm_year_estimate = get_year_from_episode_information(episode_information_dict, 4)
        print(f"llm_year_estimate: {llm_year_estimate}")



        # Compile results
        result = {
            "title": episode_information_dict['title'],
            "summary": episode_information_dict['summary'],
            "year_from": llm_year_estimate['start_date'],
            "year_until": llm_year_estimate['end_date'],
            "url" : url
        }
        return result

    except ValueError as e:
        # Handles safety filter triggers and content policy violations
        print(f"Safety filter triggered: {e}")
    except ConnectionError as e:
        # Handles API connection issues
        print(f"Connection error: {e}")
    except Exception as e:
        # Catches any other unexpected errors
        print(f"Unexpected error: {e}")

    result = {
        "title": episode_information_dict['title'],
        "summary": episode_information_dict['summary'],
        "year_from": None,
        "year_until": None,
        "url": url,
    }
    return result


def main():
    """
    Main execution function that processes a range of podcast episodes.
    Crawls each episode page, extracts information, and saves to CSV.
    """
    start_at_episode = 93
    end_at_episode = 93

    for episode_num in range(start_at_episode, end_at_episode+1):
        print(f"Crawling episode: {episode_num}")

        # Construct URL based on episode number: Episodes <= 270 use 'zs' format, > 270 use 'gag' format,
        # since GAG move from the name "Zeitsprung" to "Geschichten aus der Geschichte" at Episode 270
        if episode_num <= 270:
            url = f"https://www.geschichte.fm/podcast/zs{str(episode_num).zfill(2)}/"
        else:
            url = f"https://www.geschichte.fm/archiv/gag{str(episode_num).zfill(2)}/"

        # Process episode and write results
        result = crawl_gag_episode(url)
        if result["year_from"] not in [None, "unknown", "Unknown"]:
            write_to_csv(result, "output/episode_data.csv")
        else:
            write_to_csv(result, "output/errors_while_parsing.csv")

        print(f"Finished parsing episode: {episode_num} \n\n")


if __name__ == '__main__':
    main()
