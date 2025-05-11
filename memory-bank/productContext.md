# Product Context

This file provides a high-level overview of the project and the expected product that will be created. Initially it is based upon projectBrief.md (if provided) and all other available project-related information in the working directory. This file is intended to be updated as the project evolves, and should be used to inform all other modes of the project's goals and context.
2025-05-06 19:34:50 - Log of updates made will be appended as footnotes to the end of this file.

*

## Project Goal

* The AI Web Crawler is a specialized web scraping tool designed to collect structured football data from sportnet.sme.sk Futbalnet pages. The project aims to automatically extract relevant content while filtering out non-essential sections, converting the data to markdown format, and scoring the content quality for AI training purposes.

## Key Features

* Asynchronous web crawling
* Automatic HTML to Markdown conversion
* Content quality scoring
* Intelligent content filtering
* Targeted extraction of football data
* Exclusion of "Správy z Futbalnetu" and "Inzercia" sections
* Focus on program and match information
* JSON output format
* Rate limiting support

## Overall Architecture

* **Language**: Python
* **Main Libraries**:
    * crawl4ai (≥0.5.0)
    * beautifulsoup4 (≥4.9.0)
    * requests (≥2.28.0)
    * playwright (≥1.40.0)
* **Browser Automation**: Playwright
* **Data Format**: JSON
* **Project Structure**:
    * `crawler.py`: Main crawler implementation with custom content filtering
    * `send_to_n8n.py`: Script to send crawled data to n8n webhook
    * `requirements.txt`: Project dependencies
    * `setup_venv.bat/sh`: Scripts for setting up virtual environment
    * `.github/workflows/weekly-crawler.yml`: GitHub Actions workflow for automated crawling
    * `ai_training_data/`: Directory where crawled data is stored (gitignored)
* **Automated Workflow**: GitHub Actions for weekly crawling, data sending to n8n, and artifact upload.