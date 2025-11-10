import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
from typing import Dict, List, Set
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

class Boto3DocsScraper:
    def __init__(self, base_url: str = "https://boto3.amazonaws.com/v1/documentation/api/latest/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data = {
            "services": {}
        }
        self.lock = Lock()  # Thread-safe access to shared data
    
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch a page and return BeautifulSoup object"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(0.1)  # Reduced delay for parallel processing
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def get_all_services(self) -> Dict[str, str]:
        """Scrape the index page to get all services"""
        print("\n=== Scraping Services Index ===")
        soup = self.fetch_page(urljoin(self.base_url, "reference/services/index.html"))
        
        if not soup:
            return {}
        
        services = {}
        
        # The services index page has a section titled "Available Services"
        # Find the main content area
        main_content = soup.find('article') or soup.find('section', id='available-services')
        
        if main_content:
            # Find the toctree-wrapper in the main content (not sidebar)
            toctree = main_content.find('div', class_='toctree-wrapper')
            
            if toctree:
                # Get all links in the toctree
                links = toctree.find_all('a', class_='reference internal')
                
                for link in links:
                    href = link.get('href')
                    service_name = link.get_text().strip()
                    
                    # Services are direct HTML files in this directory
                    # Skip index.html and any anchors
                    if href and href.endswith('.html') and href != 'index.html' and '#' not in href:
                        # Construct full URL
                        service_url = urljoin(self.base_url, f"reference/services/{href}")
                        services[service_name] = service_url
                        print(f"Found service: {service_name}")
        
        print(f"\nTotal services found: {len(services)}")
        return services
    
    def get_service_methods(self, service_url: str) -> List[Dict[str, str]]:
        """Get all methods for a specific service"""
        soup = self.fetch_page(service_url)
        
        if not soup:
            return []
        
        methods = []
        
        # Find the "Client" section which contains the methods
        # Look for toctree-wrapper that contains method links
        toctree_wrappers = soup.find_all('div', class_='toctree-wrapper')
        
        for toctree in toctree_wrappers:
            links = toctree.find_all('a', class_='reference internal')
            for link in links:
                href = link.get('href')
                method_name = link.get_text().strip()
                
                # Filter for actual method links (contain 'client/' in the path)
                # and exclude section headers like "Client", "Paginators", etc.
                if href and ('client/' in href or 'paginator/' in href or 'waiter/' in href):
                    # Skip if it's just a section header (no specific method)
                    if not href.endswith('#client') and not href.endswith('#paginators') and not href.endswith('#waiters'):
                        # Construct full URL - href is relative to service page
                        method_url = urljoin(service_url, href)
                        
                        methods.append({
                            "name": method_name,
                            "url": method_url
                        })
        
        return methods
    
    def get_method_documentation(self, method_url: str) -> Dict[str, str]:
        """Extract documentation from a method page"""
        soup = self.fetch_page(method_url)
        
        if not soup:
            return {"error": "Failed to fetch page"}
        
        doc_data = {
            "url": method_url,
            "title": "",
            "description": "",
            "syntax": "",
            "parameters": [],
            "returns": "",
            "examples": [],
            "full_text": ""
        }
        
        # Get title
        title = soup.find('h1')
        if title:
            doc_data["title"] = title.get_text().strip()
        
        # Get main content
        main_content = soup.find('article') or soup.find('div', class_='document')
        
        if main_content:
            # Extract all text content
            doc_data["full_text"] = main_content.get_text(separator='\n', strip=True)
            
            # Try to extract structured information
            
            # Description (usually first paragraph(s))
            desc_section = main_content.find('p')
            if desc_section:
                doc_data["description"] = desc_section.get_text().strip()
            
            # Syntax/Request Syntax (code blocks)
            code_blocks = main_content.find_all('div', class_='highlight')
            if code_blocks:
                doc_data["syntax"] = code_blocks[0].get_text().strip()
                if len(code_blocks) > 1:
                    doc_data["examples"] = [cb.get_text().strip() for cb in code_blocks[1:]]
            
            # Parameters (look for definition lists)
            dl = main_content.find('dl')
            if dl:
                params = []
                dts = dl.find_all('dt')
                dds = dl.find_all('dd')
                for dt, dd in zip(dts, dds):
                    param_name = dt.get_text().strip()
                    param_desc = dd.get_text().strip()
                    params.append({
                        "name": param_name,
                        "description": param_desc
                    })
                doc_data["parameters"] = params
            
            # Returns (look for return type section)
            return_section = main_content.find(string=re.compile(r'Return [Tt]ype|Returns'))
            if return_section:
                return_parent = return_section.find_parent()
                if return_parent and return_parent.find_next_sibling():
                    doc_data["returns"] = return_parent.find_next_sibling().get_text().strip()
        
        return doc_data
    
    def process_method(self, service_name: str, method_info: Dict[str, str], method_num: int, total_methods: int) -> tuple:
        """Process a single method (used by thread pool)"""
        method_name = method_info["name"]
        method_url = method_info["url"]
        
        print(f"  [{method_num}/{total_methods}] Processing method: {service_name}.{method_name}")
        
        method_doc = self.get_method_documentation(method_url)
        return (method_name, method_doc)
    
    def save_service_to_json(self, filename: str = "boto3_docs.json"):
        """Save current data to JSON file (incremental save)"""
        with self.lock:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def scrape_all(self, max_services: int = None, max_methods_per_service: int = None, max_workers: int = 20, output_file: str = "boto3_docs.json"):
        """Main scraping function with parallel method fetching"""
        print("Starting Boto3 documentation scraper...")
        print(f"Using {max_workers} parallel workers for method fetching")
        print(f"Output file: {output_file}")
        
        # Step 1: Get all services
        services = self.get_all_services()
        
        if max_services:
            services = dict(list(services.items())[:max_services])
        
        # Step 2: For each service, get methods
        for service_num, (service_name, service_url) in enumerate(services.items(), 1):
            print(f"\n=== Processing service [{service_num}/{len(services)}]: {service_name} ===")
            
            self.data["services"][service_name] = {
                "url": service_url,
                "methods": {}
            }
            
            methods = self.get_service_methods(service_url)
            print(f"Found {len(methods)} methods")
            
            if max_methods_per_service:
                methods = methods[:max_methods_per_service]
            
            # Step 3: Process methods in parallel
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all method processing tasks
                future_to_method = {
                    executor.submit(
                        self.process_method, 
                        service_name, 
                        method_info, 
                        i, 
                        len(methods)
                    ): method_info 
                    for i, method_info in enumerate(methods, 1)
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_method):
                    try:
                        method_name, method_doc = future.result()
                        with self.lock:
                            self.data["services"][service_name]["methods"][method_name] = method_doc
                    except Exception as e:
                        method_info = future_to_method[future]
                        print(f"  Error processing {method_info['name']}: {e}")
            
            # Save after each service is completed
            print(f"  Completed {service_name}. Saving to {output_file}...")
            self.save_service_to_json(output_file)
            
            # Print progress
            total_methods = sum(len(service["methods"]) for service in self.data["services"].values())
            print(f"  Progress: {service_num}/{len(services)} services, {total_methods} total methods scraped")
        
        return self.data
    
    def save_to_json(self, filename: str = "boto3_docs.json"):
        """Save scraped data to JSON file"""
        print(f"\nSaving data to {filename}...")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"Data saved successfully!")
        
        # Print summary
        total_methods = sum(len(service["methods"]) for service in self.data["services"].values())
        print(f"\nSummary:")
        print(f"  Services scraped: {len(self.data['services'])}")
        print(f"  Total methods: {total_methods}")


if __name__ == "__main__":
    scraper = Boto3DocsScraper()
    
    # For testing, limit to first 3 services and 5 methods each
    # Remove these limits for full scraping (will take much longer)
    print("=" * 60)
    print("BOTO3 DOCUMENTATION SCRAPER")
    print("=" * 60)
    
    output_file = "boto3_docs.json"
    
    scraper.scrape_all(
        #max_services=3,  # Remove this for all services
        #max_methods_per_service=5,  # Remove this for all methods
        max_workers=20,  # Parallel workers for method fetching
        output_file=output_file
    )
    
    # Final save and summary
    scraper.save_to_json(output_file)
    
    print("\n" + "=" * 60)
    print("Scraping completed!")
    print("=" * 60)
