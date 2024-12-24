"""
Web Crawler for Geschichte.fm Podcast Episodes
This module crawls podcast episodes from Geschichten aus der Geschichte (geschichte.fm), extracts episode information,
and determines the historical time period discussed in each episode using an LLM.

Dependencies:
    - llm_call: Contains functions for LLM prompt modification and Gemini API calls
    - website_crawler: Contains web scraping functionality
    - write_to_csv: Contains CSV writing utilities
"""
import re
from llm_call import create_prompt, get_gemini_response
from website_crawler import extract_relevant_episode_data
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

    try:
        print(f"Crawling from url: {url}")

        # Extract content from webpage
        crawled_result = extract_relevant_episode_data(url=url)
        print(f"crawled result: {crawled_result}")

        # Get time period prediction from LLM by first adding creating the prompt
        # and then asking for a year guess (get_gemini_response())
        prompt = create_prompt(crawled_result['summary'])
        year_result = get_gemini_response(prompt)
        print(f"year result: {year_result}")

        # Retry LLM call up to 5 times if date is unknown, to see if it guesses a valid date with multiple trials
        if not re.match(r'^[+-]\d{4}$', str(year_result['start_date'])):
            for i in range(5):
                print(f"Did not find start_date for attempt number {i}/5; try again")
                year_result = get_gemini_response(prompt)
                if re.match(r'^[+-]\d{4}$', str(year_result['start_date'])):
                    print(f"Did find start_date; updated year result to: {year_result}")
                    break

        # Compile results
        result = {
            "title": crawled_result['title'],
            "summary": crawled_result['summary'],
            "year_from": year_result['start_date'],
            "year_until": year_result['end_date']
        }
        return result

    except ValueError as e:
        # Handles safety filter triggers and content policy violations
        print(f"Safety filter triggered: {e} at crawled result: {crawled_result}")
    except ConnectionError as e:
        # Handles API connection issues
        print(f"Connection error: {e}")
    # except Exception as e:
    #     # Catches any other unexpected errors
    #     print(f"Unexpected error: {e}")

    result = {
        "title": crawled_result['title'],
        "summary": "",
        "year_from": "",
        "year_until": ""
    }
    return result


def main():
    """
    Main execution function that processes a range of podcast episodes.
    Crawls each episode page, extracts information, and saves to CSV.
    """
    start_at_episode = 7
    end_at_episode = 100

    for episode_num in range(start_at_episode, end_at_episode+1):
        print(f"Crawling episode: {episode_num}")

        # Construct URL based on episode number
        # Episodes < 270 use 'zs' format, >= 270 use 'gag' format, since GAG move from the name
        # "Zeitsprung" to "Geschichten aus der Geschichte" at Episode 270
        if episode_num < 270:
            url = f"https://www.geschichte.fm/podcast/zs{str(episode_num).zfill(2)}/"
        else:
            url = f"https://www.geschichte.fm/archiv/gag{str(episode_num).zfill(2)}/"

        # Process episode and write results
        result = crawl_gag_episode(url)
        if re.match(r'^[+-]\d{4}$', str(result['year_from'])):
            write_to_csv(result, "output/episode_data.csv")
        else:
            write_to_csv(result, "output/errors_while_parsing.csv")


        print(f"Finished parsing episode: {episode_num}")


if __name__ == '__main__':
    main()
