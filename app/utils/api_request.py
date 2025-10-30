import requests

GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"


class ApiRequest:
    @staticmethod
    def fetch_google_books_api(query: str = "programming", max_results: int = 100, start_index: int = 0):
        params = {
            "q": query,
            "maxResults": max_results,
            "startIndex": start_index
        }

        response = requests.get(GOOGLE_BOOKS_API, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch books from Google Books API")

        data = response.json()
        books = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            industry_identifiers = volume_info.get("industryIdentifiers", [])
            title = volume_info.get("title", "No Title")
            description = volume_info.get("description", "No Description")
            author = volume_info.get("authors", ["Unknown"])[0]
            publisher = volume_info.get("publisher", "Unknown Publisher")
            published_date = volume_info.get("publishedDate", "Unknown Date")
            isbn = industry_identifiers[0].get("identifier", "No ISBN") if industry_identifiers else "No ISBN"
            cover_url = volume_info.get("imageLinks", {}).get("thumbnail", "")
            books.append({"title": title, "description": description, "author": author, "publisher": publisher,
                          "published_date": published_date, "isbn": isbn, "cover_url": cover_url})
        return books
