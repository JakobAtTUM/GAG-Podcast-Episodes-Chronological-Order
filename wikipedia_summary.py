import wikipedia
from typing import Optional, Tuple


def get_wikipedia_summary(search_term: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Searches Wikipedia for a term and returns the title and first paragraph of the best matching article.

    Args:
        search_term (str): The search term to look up on Wikipedia

    Returns:
        Tuple[Optional[str], Optional[str]]: (article_title, first_paragraph)
            Returns (None, None) if no article is found or an error occurs
    """
    try:
        # Search for the page
        wikipedia.set_lang("de")
        search_results = wikipedia.search(search_term)

        if not search_results:
            print(f"No Wikipedia article found for: {search_term}")
            return None, None

        # Get the first (best matching) result
        page_title = search_results[0]

        # Get the page content
        page = wikipedia.page(page_title, auto_suggest=False)

        # Get the summary (first paragraph)
        summary = page.summary #.split('\n')[0]

        return page.title, summary

    except wikipedia.DisambiguationError as e:
        # Handle disambiguation pages
        print(f"Multiple matches found for '{search_term}'. Try being more specific.")
        print("Possible matches:", e.options[:5])  # Show first 5 options
        return None, None

    except wikipedia.PageError:
        print(f"No Wikipedia article found for: {search_term}")
        return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None