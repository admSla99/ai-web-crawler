import asyncio
import json
import hashlib
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode
)
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class CustomContentFilter(PruningContentFilter):
    """Custom content filter that extends PruningContentFilter to exclude specific sections"""

    def __init__(self, threshold=0.4, threshold_type="fixed", min_word_threshold=50):
        super().__init__(threshold=threshold, threshold_type=threshold_type, min_word_threshold=min_word_threshold)

    def filter_content(self, html_content):
        """Pre-process HTML to remove unwanted sections before applying standard filtering"""
        soup = BeautifulSoup(html_content, 'html.parser')

        print("Starting custom content filtering...")

        # Find and remove the "Správy z Futbalnetu" section
        spravy_section = soup.find(lambda tag: tag.name == 'h2' and 'Správy z Futbalnetu' in tag.text)
        if spravy_section:
            print("Found 'Správy z Futbalnetu' section - removing it")
            # Find the parent container
            parent = spravy_section.parent
            if parent:
                parent.decompose()
                print("Removed 'Správy z Futbalnetu' section")

        # Process the entire page content (without looking for specific sections)
        print("Processing entire page content")

        # Apply the standard PruningContentFilter to the modified HTML
        filtered_html = str(soup)
        print("Applying standard PruningContentFilter...")
        return super().filter_content(filtered_html)

class SimpleAICrawler:
    def __init__(self, output_dir="crawled_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Basic browser configuration
        self.browser_config = BrowserConfig(
            headless=True,  # Run in background
            user_agent="SimpleAICrawler/1.0"  # Crawler identification
        )

        # Create custom content filter that focuses on <div class="content"> and removes unwanted sections
        custom_filter = CustomContentFilter()

        # Markdown generator configuration with custom filter
        self.md_generator = DefaultMarkdownGenerator(
            content_filter=custom_filter
        )

        # Crawler configuration
        self.crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Always get fresh content
            markdown_generator=self.md_generator,
            # Exclude common non-content tags
            excluded_tags=['form', 'header', 'footer', 'nav']
        )

    def _get_url_hash(self, url):
        """Generate consistent hash for URL"""
        return hashlib.md5(url.encode()).hexdigest()

    def _get_filepath_for_url(self, url):
        """Get filepath for URL data"""
        filename = f"data_{self._get_url_hash(url)}.json"
        return self.output_dir / filename

    def is_url_crawled(self, url):
        """Check if URL has already been crawled"""
        filepath = self._get_filepath_for_url(url)
        return filepath.exists()

    async def crawl_url(self, url, force_crawl=False):
        try:
            # Check if URL was already crawled
            filepath = self._get_filepath_for_url(url)
            if not force_crawl and filepath.exists():
                print(f"URL already crawled, skipping: {url}")
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)

            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                # Add delay before each crawl
                await asyncio.sleep(2.0)  # 2 seconds between requests

                result = await crawler.arun(
                    url=url,
                    config=self.crawler_config
                )

                # Post-process the markdown to remove any remaining "Správy z Futbalnetu" sections
                raw_markdown = result.markdown.raw_markdown
                filtered_markdown = result.markdown.fit_markdown

                # Function to remove "Správy z Futbalnetu" section from markdown
                def remove_spravy_section(markdown_text):
                    # Split the markdown by the "Správy z Futbalnetu" heading
                    if "## Správy z Futbalnetu" in markdown_text:
                        parts = markdown_text.split("## Správy z Futbalnetu")
                        # Keep only the content before the heading
                        return parts[0].strip()
                    return markdown_text

                # Apply the cleaning to both raw and filtered markdown
                cleaned_raw_markdown = remove_spravy_section(raw_markdown)
                cleaned_filtered_markdown = remove_spravy_section(filtered_markdown)

                print(f"Removed 'Správy z Futbalnetu' section from final markdown")

                # Prepare data for AI
                data = {
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "content": {
                        "raw_markdown": cleaned_raw_markdown,
                        "filtered_markdown": cleaned_filtered_markdown
                    },
                    "metadata": {
                        "length": len(cleaned_filtered_markdown),
                        "quality_score": self._calculate_quality_score_for_text(cleaned_filtered_markdown)
                    }
                }

                # Save data
                self._save_data(data)
                return data

        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            return None

    def _calculate_quality_score(self, result):
        # Simple content quality calculation
        content = result.markdown.fit_markdown
        return self._calculate_quality_score_for_text(content)

    def _calculate_quality_score_for_text(self, content):
        # Simple content quality calculation for a text string
        if not content:
            return 0.0

        # Basic quality metrics
        words = len(content.split())
        sentences = len(content.split('.'))

        if sentences == 0:
            return 0.0

        avg_sentence_length = words / sentences

        # Score based on length and average sentence length
        score = min(1.0, (words / 1000) * 0.5 + (min(20, avg_sentence_length) / 20) * 0.5)
        return round(score, 2)

    def _save_data(self, data):
        filepath = self._get_filepath_for_url(data['url'])
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def crawl_multiple_urls(self, urls, force_crawl=False):
        results = []
        for url in urls:
            if not force_crawl and self.is_url_crawled(url):
                print(f"Skipping already crawled URL: {url}")
                with open(self._get_filepath_for_url(url), 'r', encoding='utf-8') as f:
                    results.append(json.load(f))
                continue

            result = await self.crawl_url(url, force_crawl)
            if result:
                results.append(result)
        return results

def main():
    # Usage example
    urls = [
        "https://sportnet.sme.sk/futbalnet/k/fk-fc-raznany/tim/dospeli-m-a/program/",
        "https://sportnet.sme.sk/futbalnet/z/obfz-presov/s/8-liga-dospeli-obfz-presov/tabulky/"
    ]

    crawler = SimpleAICrawler(output_dir="ai_training_data")

    print("Starting crawling...")
    # Force a fresh crawl to test our changes
    results = asyncio.run(crawler.crawl_multiple_urls(urls, force_crawl=True))

    # Print a summary of the results
    if results and len(results) > 0:
        print("\nCrawling results:")
        for result in results:
            print(f"URL: {result['url']}")
            print(f"Content length: {result['metadata']['length']} characters")
            print(f"Quality score: {result['metadata']['quality_score']}")

            # Print a sample of the filtered content
            filtered_content = result['content']['filtered_markdown']
            sample_length = min(200, len(filtered_content))
            print(f"Sample of filtered content: {filtered_content[:sample_length]}...")

    print(f"\nCrawling completed. Processed URLs: {len(results)}")
    print("Summary:")
    print(f"- New URLs crawled: {len([r for r in results if r.get('timestamp') == datetime.now().strftime('%Y-%m-%d')])}")
    print(f"- Cached URLs used: {len([r for r in results if r.get('timestamp') != datetime.now().strftime('%Y-%m-%d')])}")
    print(f"Data has been saved to: {crawler.output_dir}")

if __name__ == "__main__":
    main()