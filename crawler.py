import asyncio
import json
import hashlib
from datetime import datetime
from pathlib import Path
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    CacheMode
)
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class SimpleAICrawler:
    def __init__(self, output_dir="crawled_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Basic browser configuration
        self.browser_config = BrowserConfig(
            headless=True,  # Run in background
            user_agent="SimpleAICrawler/1.0"  # Crawler identification
        )
        
        # Markdown generator configuration with filter
        self.md_generator = DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.4,  # Content filtering threshold
                threshold_type="fixed"
            )
        )
        
        # Crawler configuration
        self.crawler_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Always get fresh content
            markdown_generator=self.md_generator
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
                
                # Prepare data for AI
                data = {
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "content": {
                        "raw_markdown": result.markdown.raw_markdown,
                        "filtered_markdown": result.markdown.fit_markdown
                    },
                    "metadata": {
                        "length": len(result.markdown.fit_markdown),
                        "quality_score": self._calculate_quality_score(result)
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
        "https://github.com/modelcontextprotocol/servers",
        "https://sk.wikipedia.org/wiki/Prv%C3%A1_svetov%C3%A1_vojna",
        "https://sk.wikipedia.org/wiki/Druh%C3%A1_svetov%C3%A1_vojna"
    ]
    
    crawler = SimpleAICrawler(output_dir="ai_training_data")
    
    print("Starting crawling...")
    results = asyncio.run(crawler.crawl_multiple_urls(urls))
    
    print(f"\nCrawling completed. Processed URLs: {len(results)}")
    print("Summary:")
    print(f"- New URLs crawled: {len([r for r in results if r.get('timestamp') == datetime.now().strftime('%Y-%m-%d')])}") 
    print(f"- Cached URLs used: {len([r for r in results if r.get('timestamp') != datetime.now().strftime('%Y-%m-%d')])}")
    print(f"Data has been saved to: {crawler.output_dir}")

if __name__ == "__main__":
    main()