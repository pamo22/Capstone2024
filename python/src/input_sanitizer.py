from urllib.parse import urlparse

def sanitize_title(title):
    return title.replace("'", "''").strip()


def sanitize_url(url):
    parsed_url = urlparse(url)
    if all([parsed_url.scheme, parsed_url.netloc]):
        return url
    else:
        raise ValueError("Invalid URL")


def sanitize_frequency(frequency):
    try:
        freq = int(frequency)
        if freq > 0:
            return freq
        else:
            raise ValueError("Frequency must be a positive integer")
    except ValueError:
        raise ValueError("Frequency must be a valid integer")


def sanitize_inputs(title, url, frequency):
    try:
        sanitized_title = sanitize_title(title)
        sanitized_url = sanitize_url(url)
        sanitized_frequency = sanitize_frequency(frequency)
        return {
            "title": sanitized_title,
            "url": sanitized_url,
            "frequency": sanitized_frequency
        }
    except ValueError as e:
        print(f"Input error: {e}")
        return None


inputs = sanitize_inputs("Hello Title", "https://example.com", "1")
if inputs:
    print("Sanitized inputs:", inputs)
else:
    print("Invalid inputs provided")
