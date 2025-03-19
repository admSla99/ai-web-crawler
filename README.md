# AI Web Crawler

A simple yet powerful web crawler designed specifically for collecting training data for AI models. Built with Crawl4AI, this crawler automatically converts web content to markdown format and includes quality scoring.

## Features

- Asynchronous web crawling
- Automatic HTML to Markdown conversion
- Content quality scoring
- Configurable content filtering
- JSON output format
- Rate limiting support

## Installation

1. Create and activate virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:

```bash
playwright install
```

## Usage

1. Update the URLs in `crawler.py`:

```python
urls = [
    "https://example.com",
    "https://example.org"
]
```

2. Run the crawler:

```bash
python crawler.py
```

The crawler will save the results in the `ai_training_data` directory in JSON format.

## Configuration

You can configure the crawler by modifying these parameters in `crawler.py`:

- `threshold`: Content quality threshold (0.0 to 1.0)
- `headless`: Browser visibility (True/False)
- `delay`: Delay between requests (seconds)

## Output Format

The crawler saves data in JSON format with the following structure:

```json
{
    "url": "crawled_url",
    "timestamp": "ISO-8601 timestamp",
    "content": {
        "raw_markdown": "original markdown",
        "filtered_markdown": "filtered content"
    },
    "metadata": {
        "length": "content length",
        "quality_score": "calculated quality score"
    }
}
```

## License

MIT 