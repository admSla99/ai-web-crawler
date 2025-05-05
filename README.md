# AI Web Crawler for Sportnet.sme.sk Futbalnet

A specialized web crawler designed for collecting structured football data from sportnet.sme.sk futbalnet pages. Built with Crawl4AI, this crawler automatically extracts relevant content while excluding non-essential sections like "Správy z Futbalnetu" and "Inzercia". The extracted content is converted to markdown format and includes quality scoring for AI training purposes.

## Features

- Asynchronous web crawling
- Automatic HTML to Markdown conversion
- Content quality scoring
- Intelligent content filtering
- Targeted extraction of football data
- Exclusion of "Správy z Futbalnetu" and "Inzercia" sections
- Focus on program and match information
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

1. Update the URLs in `crawler.py` with sportnet.sme.sk futbalnet URLs:

```python
urls = [
    "https://sportnet.sme.sk/futbalnet/k/fk-fc-raznany/tim/dospeli-m-a/program/",
    # Add more futbalnet URLs as needed
]
```

2. Run the crawler:

```bash
python crawler.py
```

The crawler will:
- Extract content from the specified futbalnet pages
- Remove "Správy z Futbalnetu" and "Inzercia" sections
- Process the entire page content
- Save the results in the `ai_training_data` directory in JSON format

## Configuration

You can configure the crawler by modifying these parameters in `crawler.py`:

- `threshold`: Content quality threshold (0.0 to 1.0)
- `min_word_threshold`: Minimum word count for content blocks (default: 50)
- `headless`: Browser visibility (True/False)
- `delay`: Delay between requests (seconds)
- `excluded_tags`: HTML tags to exclude (e.g., 'form', 'header', 'footer', 'nav')

### Content Filtering

The crawler uses a custom content filter that:

1. Identifies and removes the "Správy z Futbalnetu" section
2. Processes the entire page content
3. Applies the standard PruningContentFilter to improve content quality

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

## Automated Workflow

This project includes a GitHub Actions workflow that automatically runs the crawler on a weekly schedule and sends the data to an n8n webhook.

### Setup

1. In your GitHub repository, go to Settings > Secrets and Variables > Actions
2. Add a new repository secret named `N8N_WEBHOOK_URL` with your n8n webhook URL
3. The workflow will run automatically every Sunday at 23:59 UTC

### Workflow Details

The GitHub Actions workflow:
- Runs on a weekly schedule (Sunday at 23:59 UTC)
- Installs all required dependencies
- Runs the crawler script
- Sends the collected data to your n8n webhook
- Uploads the crawled data as a GitHub Actions artifact

You can also manually trigger the workflow from the Actions tab in your GitHub repository.

### Webhook Data Format

The data sent to the n8n webhook has the following structure:

```json
{
  "data": [
    {
      "url": "crawled_url_1",
      "timestamp": "ISO-8601 timestamp",
      "content": {
        "raw_markdown": "original markdown",
        "filtered_markdown": "filtered content"
      },
      "metadata": {
        "length": "content length",
        "quality_score": "calculated quality score"
      }
    },
    // Additional crawled pages...
  ],
  "metadata": {
    "total_files": 2,
    "total_items": 2
  }
}
```

## License

MIT