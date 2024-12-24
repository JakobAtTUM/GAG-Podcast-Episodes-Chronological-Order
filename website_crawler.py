"""
Web Scraping Module for Geschichte.fm Podcast Episodes
This module provides functionality to extract episode titles and summaries from
Geschichte.fm podcast website pages using BeautifulSoup4.

Dependencies:
    - requests: For making HTTP requests
    - BeautifulSoup4: For parsing HTML content
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict


def extract_relevant_episode_data(html_content: Optional[str] = None,
                                  url: Optional[str] = None) -> Optional[Dict[str, str]]:
    """
    Extracts episode title and summary from Geschichte.fm podcast pages.

    Processes either direct HTML content or fetches from a URL. Extracts the title
    and first two paragraphs of content, cleaning up common unwanted text patterns.

    Args:
        html_content (str, optional): Raw HTML content to parse
        url (str, optional): URL to fetch content from

    Returns:
        dict: Dictionary containing:
            - title (str): Episode title
            - summary (str): Combined and cleaned first two paragraphs
        None: If extraction fails

    Raises:
        ValueError: If neither html_content nor url is provided
    """
    try:
        # Initialize BeautifulSoup object from either source
        soup = _initialize_soup(html_content, url)

        # Extract and clean title
        title = _extract_title(soup)

        # Extract and process summary
        summary = _extract_summary(soup)

        if not summary:
            return None

        return {
            "title": title,
            "summary": summary
        }

    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def _initialize_soup(html_content: Optional[str], url: Optional[str]) -> BeautifulSoup:
    """
    Creates a BeautifulSoup object from either HTML content or URL.

    Args:
        html_content (str, optional): Raw HTML content
        url (str, optional): URL to fetch content from

    Returns:
        BeautifulSoup: Initialized BeautifulSoup object

    Raises:
        ValueError: If neither input is provided
    """
    if html_content:
        return BeautifulSoup(html_content, 'html.parser', from_encoding='utf-8')
    elif url:
        response = requests.get(url)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')
    else:
        raise ValueError("Either html_content or url must be provided")


def _extract_title(soup: BeautifulSoup) -> str:
    """
    Extracts and cleans the episode title from the page.

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        str: Cleaned episode title
    """
    title_element = soup.find('h1', {'class': 'page-title'})
    return title_element.get_text().strip() if title_element else ""


def _extract_summary(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts and processes the episode summary from the first two paragraphs.

    Args:
        soup (BeautifulSoup): Parsed HTML content

    Returns:
        str: Cleaned and combined summary text
        None: If content div is not found
    """
    content_div = soup.find('div', class_='entry-content')
    if not content_div:
        print("Content div not found")
        return None

    # Extract first two paragraphs
    paragraphs = content_div.find_all('p')[:2]

    # Combine paragraphs
    summary = " ".join(p.get_text() for p in paragraphs if p)

    # Clean up unwanted text patterns
    unwanted_phrases = ['Vielen Dank', 'AUS UNSERER WERBUNG', 'Weiterlesen']
    for phrase in unwanted_phrases:
        summary = summary.split(phrase)[0].strip()

    return summary

