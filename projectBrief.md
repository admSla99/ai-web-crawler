# AI Web Crawler Project Brief

## Project Overview
The AI Web Crawler is a specialized web scraping tool designed to collect structured football data from sportnet.sme.sk Futbalnet pages. The project aims to automatically extract relevant content while filtering out non-essential sections, converting the data to markdown format, and scoring the content quality for AI training purposes.

## Repository Information
- **Repository Name**: ai-web-crawler
- **Owner**: admSla99
- **Created**: March 19, 2025
- **Last Updated**: May 5, 2025
- **Description**: A web crawler designed for collecting AI training data, built with Crawl4AI

## Key Features
- Asynchronous web crawling
- Automatic HTML to Markdown conversion
- Content quality scoring
- Intelligent content filtering
- Targeted extraction of football data
- Exclusion of "Správy z Futbalnetu" and "Inzercia" sections
- Focus on program and match information
- JSON output format
- Rate limiting support

## Technical Stack
- **Language**: Python
- **Main Libraries**:
  - crawl4ai (≥0.5.0)
  - beautifulsoup4 (≥4.9.0)
  - requests (≥2.28.0)
  - playwright (≥1.40.0)
- **Browser Automation**: Playwright
- **Data Format**: JSON

## Project Structure
- **crawler.py**: Main crawler implementation with custom content filtering
- **send_to_n8n.py**: Script to send crawled data to n8n webhook
- **requirements.txt**: Project dependencies
- **setup_venv.bat/sh**: Scripts for setting up virtual environment
- **.github/workflows/weekly-crawler.yml**: GitHub Actions workflow for automated crawling
- **ai_training_data/**: Directory where crawled data is stored (gitignored)

## Automated Workflow
The project includes a GitHub Actions workflow that:
- Runs every Sunday at 23:59 UTC
- Installs required dependencies
- Runs the crawler script
- Sends collected data to an n8n webhook
- Uploads crawled data as a GitHub Actions artifact

## Data Format
The crawler saves data in JSON format with the following structure:
```json
{
    "id": "unique_id_from_url",
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

## Setup Instructions
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
1. Update the URLs in `crawler.py` with sportnet.sme.sk futbalnet URLs
2. Run the crawler:
   ```bash
   python crawler.py
   ```

## Webhook Integration
The project sends data to an n8n webhook with the following structure:
```json
{
  "data": [
    {
      "id": "unique_id_from_url",
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
