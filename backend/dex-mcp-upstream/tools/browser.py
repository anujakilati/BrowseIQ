"""Browser tools for interacting with the browser extension."""

from typing import Any, Dict
from context import Context
import json
from datetime import datetime
import os
from urllib.parse import urlparse
from collections import defaultdict, Counter
import re


async def get_tabs_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Get all open browser tabs.
    
    Params: None
    """
    try:
        result = await context.send_socket_message("get_tabs", {})
        
        if not result or "tabs" not in result:
            return "No tabs found or unable to fetch tabs."
        
        tabs = result["tabs"]
        if not tabs:
            return "No open tabs found."
        
        # Format tabs into readable text
        tab_list = []
        for tab in tabs:
            tab_info = f"Tab {tab.get('id', 'Unknown')}: {tab.get('title', 'Untitled')}"
            if tab.get('url'):
                tab_info += f"\n  URL: {tab['url']}"
            tab_list.append(tab_info)
        
        return f"Found {len(tabs)} open tabs:\n\n" + "\n\n".join(tab_list)
        
    except Exception as e:
        return f"Error getting tabs: {str(e)}"


async def screenshot_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Take a screenshot of the active tab.
    
    Params: None
    """
    try:
        result = await context.send_socket_message("screenshot", {})
        
        if not result:
            return "Failed to take screenshot."
        
        if result.get("success"):
            return result
        else:
            return f"Failed to take screenshot: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"


async def navigate_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Navigate to a URL in active tab or specified tab.
    
    Params:
        url (str): Required - URL to navigate to
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "url" not in params:
        return "Error: URL parameter is required"
    
    url = params["url"]
    tab_id = params.get("tab_id")
    
    payload = {"url": url}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("navigate", payload)
        
        if not result:
            return f"Failed to navigate to {url}"
        
        if result.get("success"):
            message = result.get("message", f"Navigated to {url}")
            action = result.get("action", "go_to_url")
            return f"Successfully navigated to {url}\nAction: {action} - {message}"
        else:
            return f"Failed to navigate to {url}: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error navigating to {url}: {str(e)}"


async def select_tab_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Switch to a specific browser tab by ID.
    
    Params:
        tab_id (int): Required - Tab ID to switch to
    """
    if not params or "tab_id" not in params:
        return "Error: tab_id parameter is required"
    
    tab_id = params["tab_id"]
    
    try:
        result = await context.send_socket_message("select_tab", {"tab_id": tab_id})
        
        if not result:
            return f"Failed to select tab {tab_id}"
        
        if result.get("success"):
            message = result.get("message", "Tab selected")
            action = result.get("action", "select_tab")
            return f"Successfully switched to tab {tab_id}\nAction: {action} - {message}"
        else:
            return f"Failed to select tab {tab_id}: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error selecting tab {tab_id}: {str(e)}"


async def new_tab_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Create a new browser tab, optionally with a specific URL.
    
    Params:
        url (str): Optional - URL to open in new tab, defaults to blank tab
    """
    url = params.get("url") if params else None
    
    payload = {}
    if url:
        payload["url"] = url
    
    try:
        result = await context.send_socket_message("new_tab", payload)
        
        if not result:
            return "Failed to create new tab"
        
        if result.get("success"):
            tab_id = result.get("data", {}).get("id")
            message = result.get("message", "New tab created")
            action = result.get("action", "new_tab")
            
            if url:
                return f"Successfully created new tab (ID: {tab_id}) with URL: {url}\nAction: {action} - {message}"
            else:
                return f"Successfully created new tab (ID: {tab_id})\nAction: {action} - {message}"
        else:
            return f"Failed to create new tab: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error creating new tab: {str(e)}"


async def close_tab_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Close a browser tab by ID, or close the active tab if no ID specified.
    
    Params:
        tab_id (int): Optional - Tab ID to close, defaults to active tab
    """
    tab_id = params.get("tab_id") if params else None
    
    payload = {}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("close_tab", payload)
        
        if not result:
            return f"Failed to close tab {tab_id if tab_id else '(active)'}"
        
        if result.get("success"):
            message = result.get("message", "Tab closed")
            action = result.get("action", "close_tab")
            return f"Successfully closed tab {tab_id if tab_id else '(active)'}\nAction: {action} - {message}"
        else:
            return f"Failed to close tab: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error closing tab: {str(e)}"


async def search_google_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Perform a Google search in active tab or specified tab.
    
    Params:
        query (str): Required - Search query text
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "query" not in params:
        return "Error: query parameter is required"
    
    query = params["query"]
    tab_id = params.get("tab_id")
    
    payload = {"query": query}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("search_google", payload)
        
        if not result:
            return f"Failed to search Google for '{query}'"
        
        if result.get("success"):
            message = result.get("message", f"Searched Google for {query}")
            action = result.get("action", "search_google")
            return f"Successfully searched Google for '{query}'\nAction: {action} - {message}"
        else:
            return f"Failed to search Google for '{query}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error searching Google for '{query}': {str(e)}"


async def click_element_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Click on a DOM element by its ID.
    
    Params:
        element_id (str): Required - Element ID to click
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "element_id" not in params:
        return "Error: element_id parameter is required"
    
    element_id = params["element_id"]
    tab_id = params.get("tab_id")
    
    payload = {"element_id": element_id}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("click_element", payload)
        
        if not result:
            return f"Failed to click element '{element_id}'"
        
        if result.get("success"):
            message = result.get("message", f"Clicked element '{element_id}'")
            action = result.get("action", "click_element")
            return f"Successfully clicked element '{element_id}'\nAction: {action} - {message}"
        else:
            return f"Failed to click element '{element_id}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error clicking element '{element_id}': {str(e)}"


async def input_text_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Type text into a DOM element by its ID.
    
    Params:
        element_id (str): Required - Element ID to type into
        text (str): Required - Text to input
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "element_id" not in params or "text" not in params:
        return "Error: element_id and text parameters are required"
    
    element_id = params["element_id"]
    text = params["text"]
    tab_id = params.get("tab_id")
    
    payload = {"element_id": element_id, "text": text}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("input_text", payload)
        
        if not result:
            return f"Failed to input text into element '{element_id}'"
        
        if result.get("success"):
            message = result.get("message", f"Input text into element '{element_id}'")
            action = result.get("action", "input_text")
            return f"Successfully input text '{text}' into element '{element_id}'\nAction: {action} - {message}"
        else:
            return f"Failed to input text into element '{element_id}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error inputting text into element '{element_id}': {str(e)}"


async def send_keys_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Send keyboard shortcuts or key combinations to the page.
    
    Params:
        keys (str): Required - Key combination (e.g. 'Ctrl+C', 'Enter', 'Tab')
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    if not params or "keys" not in params:
        return "Error: keys parameter is required"
    
    keys = params["keys"]
    tab_id = params.get("tab_id")
    
    payload = {"keys": keys}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("send_keys", payload)
        
        if not result:
            return f"Failed to send keys '{keys}'"
        
        if result.get("success"):
            message = result.get("message", f"Sent keys '{keys}'")
            action = result.get("action", "send_keys")
            return f"Successfully sent keys '{keys}'\nAction: {action} - {message}"
        else:
            return f"Failed to send keys '{keys}': {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error sending keys '{keys}': {str(e)}"


async def grab_dom_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Get formatted DOM structure with XPath mappings for elements.
    
    Params:
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    tab_id = params.get("tab_id") if params else None
    
    payload = {}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("grab_dom", payload)
        
        if not result:
            return "Failed to grab DOM structure"
        
        if result.get("success"):
            return result
        else:
            return f"Failed to grab DOM: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error grabbing DOM: {str(e)}"


async def capture_with_highlights_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Take a screenshot with element highlights for better AI understanding.
    
    Params:
        tab_id (int): Optional - Specific tab ID, defaults to active tab
    """
    tab_id = params.get("tab_id") if params else None
    
    payload = {}
    if tab_id is not None:
        payload["tab_id"] = tab_id
    
    try:
        result = await context.send_socket_message("capture_with_highlights", payload)
        
        if not result:
            return "Failed to capture screenshot with highlights"
        
        if result.get("success"):
            return result
        else:
            return f"Failed to capture screenshot with highlights: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error capturing screenshot with highlights: {str(e)}"


async def add_assistant_message_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Add an assistant message to the chat.
    
    Params:
        message (str): Required - Message to add to the chat
    """
    if not params or "message" not in params:
        return "Error: message parameter is required"
    
    message = params["message"]
    
    try:
        result = await context.send_socket_message("add_assistant_message", {"message": message})
        
        if not result:
            return f"Failed to add assistant message"
        
        if result.get("success"):
            return f"Successfully added assistant message: {message}"
        else:
            return f"Failed to add assistant message: {result.get('error', 'Unknown error')}"
            
    except Exception as e:
        return f"Error adding assistant message: {str(e)}"


async def query_history_by_date_tool(context: Context, params: Dict[str, Any] = None) -> str:
    """Query browsing history for a specific date and return matching items with summaries.
    
    Params:
        date (str): Required - Date in YYYY-MM-DD format or natural language (e.g., "May 24th, 2025")
    """
    if not params or "date" not in params:
        return "Error: date parameter is required (format: YYYY-MM-DD or natural language like 'May 24th, 2025')"
    
    date_str = params["date"]
    
    try:
        # Try to convert natural language dates to YYYY-MM-DD format
        date_conversions = {
            "may 22nd, 2025": "2025-05-22",
            "may 23rd, 2025": "2025-05-23", 
            "may 24th, 2025": "2025-05-24",
            "may 21st, 2025": "2025-05-21",
            "may 20th, 2025": "2025-05-20"
        }
        
        # Check if it's a natural language date
        normalized_date = date_str.lower().strip()
        if normalized_date in date_conversions:
            date_str = date_conversions[normalized_date]
        
        # Validate date format
        query_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Load history data from contents.json
        data_file = "../../data/contents.json"
        if not os.path.exists(data_file):
            # Try alternative path
            data_file = "../data/contents.json"
            if not os.path.exists(data_file):
                return f"Browsing history data file not found. Checked paths: ../../data/contents.json and ../data/contents.json"
        
        with open(data_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        # Filter items for the specified date
        matching_items = []
        search_queries = []
        
        for item in history_data:
            item_date = datetime.strptime(item['timestamp'].split('T')[0], '%Y-%m-%d')
            if item_date.date() == query_date.date():
                matching_items.append(item)
                
                # Extract search queries from Google searches
                content = item.get('content', '')
                if 'Google search:' in content:
                    query = content.replace('Google search:', '').strip()
                    if query:
                        search_queries.append(query)
        
        if not matching_items:
            return f"No browsing history found for {date_str}"
        
        # Generate summary
        summary = f"Browsing Activity for {date_str}:\n"
        summary += f"Total pages visited: {len(matching_items)}\n\n"
        
        if search_queries:
            summary += f"Google Searches ({len(search_queries)} total):\n"
            for i, query in enumerate(search_queries, 1):
                summary += f"{i}. {query}\n"
            summary += "\n"
        
        # Show most visited domains
        domains = {}
        for item in matching_items:
            try:
                from urllib.parse import urlparse
                domain = urlparse(item['url']).netloc.lower()
                if domain.startswith('www.'):
                    domain = domain[4:]
                domains[domain] = domains.get(domain, 0) + item.get('no_of_visits', 1)
            except:
                continue
        
        if domains:
            summary += "Most Visited Sites:\n"
            sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]
            for domain, visits in sorted_domains:
                summary += f"- {domain}: {visits} visits\n"
        
        return summary
            
    except ValueError as e:
        return f"Error: Invalid date format. Please use YYYY-MM-DD format or natural language like 'May 24th, 2025'. Error: {str(e)}"
    except Exception as e:
        return f"Error querying history: {str(e)}"


def generate_browsing_analytics_tool(output_file: str = "../../data/browsing_analytics.json") -> str:
    """
    Analyze browsing patterns to show what you search for most and website visit frequencies.
    
    Focuses on:
    - URL frequency analysis with visit counts
    - Website categorization for better organization
    - Search pattern identification
    - Data suitable for pie chart visualization
    
    Args:
        output_file: Path to save the analytics JSON file
        
    Returns:
        Summary of most visited sites, search patterns, and category breakdown
    """
    try:
        # Load browsing history data - fix path for MCP server directory
        data_file = "../../data/contents.json"
        if not os.path.exists(data_file):
            # Try alternative path
            data_file = "../data/contents.json"
            if not os.path.exists(data_file):
                return json.dumps({"error": f"Browsing history data file not found. Checked paths: ../../data/contents.json and ../data/contents.json"}, indent=2)
        
        with open(data_file, 'r', encoding='utf-8') as f:
            browsing_data = json.load(f)
        
        # Initialize analytics structures
        domain_stats = defaultdict(lambda: {
            'total_visits': 0,
            'unique_pages': 0,
            'urls': [],
            'titles': [],
            'first_visit': None,
            'last_visit': None
        })
        
        url_frequency = Counter()
        search_queries = Counter()
        category_stats = defaultdict(int)
        
        # Process each browsing entry
        for entry in browsing_data:
            url = entry.get('url', '')
            visits = entry.get('no_of_visits', 1)
            timestamp = entry.get('timestamp', '')
            content = entry.get('content', '')
            
            # Count URL frequency
            url_frequency[url] += visits
            
            # Extract domain
            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.lower()
                if domain.startswith('www.'):
                    domain = domain[4:]
            except:
                domain = 'unknown'
            
            # Extract page title from content or URL
            title = extract_title_from_content(content, url)
            
            # Extract search queries from Google searches
            if 'google.com/search' in url and 'q=' in url:
                try:
                    from urllib.parse import parse_qs, urlparse
                    parsed = urlparse(url)
                    params = parse_qs(parsed.query)
                    if 'q' in params:
                        query = params['q'][0]
                        search_queries[query] += visits
                except:
                    pass
            
            # Update domain statistics
            domain_stats[domain]['total_visits'] += visits
            domain_stats[domain]['unique_pages'] += 1
            domain_stats[domain]['urls'].append({'url': url, 'visits': visits, 'title': title})
            if title:
                domain_stats[domain]['titles'].append(title)
            
            # Update visit timestamps
            if timestamp:
                if not domain_stats[domain]['first_visit'] or timestamp < domain_stats[domain]['first_visit']:
                    domain_stats[domain]['first_visit'] = timestamp
                if not domain_stats[domain]['last_visit'] or timestamp > domain_stats[domain]['last_visit']:
                    domain_stats[domain]['last_visit'] = timestamp
            
            # Categorize and count
            domain_category = categorize_domain(domain, url, content)
            category_stats[domain_category] += visits
        
        # Convert domain stats to list format
        domain_list = []
        for domain, stats in domain_stats.items():
            # Get top URLs for this domain
            top_urls = sorted(stats['urls'], key=lambda x: x['visits'], reverse=True)[:10]
            
            domain_list.append({
                'domain': domain,
                'total_visits': stats['total_visits'],
                'unique_pages': stats['unique_pages'],
                'category': categorize_domain(domain, '', ''),
                'top_urls': top_urls
            })
        
        # Sort domains by total visits
        domain_list.sort(key=lambda x: x['total_visits'], reverse=True)
        
        # Get top URLs overall
        top_urls_overall = [
            {'url': url, 'visits': count} 
            for url, count in url_frequency.most_common(20)
        ]
        
        # Get top search queries
        top_searches = [
            {'query': query, 'searches': count} 
            for query, count in search_queries.most_common(10)
        ]
        
        # Create analytics output optimized for pie charts and frequency analysis
        analytics = {
            'domain_frequency': [
                {
                    'domain': domain['domain'],
                    'visits': domain['total_visits'],
                    'category': domain['category'],
                    'percentage': round((domain['total_visits'] / sum(d['total_visits'] for d in domain_list)) * 100, 1)
                }
                for domain in domain_list[:15]  # Top 15 for pie chart
            ],
            'category_breakdown': [
                {
                    'category': category,
                    'visits': visits,
                    'percentage': round((visits / sum(category_stats.values())) * 100, 1)
                }
                for category, visits in sorted(category_stats.items(), key=lambda x: x[1], reverse=True)
            ]
        }
        
        # Save analytics to file
        if output_file and os.path.dirname(output_file):
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, indent=2, ensure_ascii=False)
        
        # Return JSON format only
        return json.dumps(analytics, indent=2, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"Error generating browsing analytics: {str(e)}"}, indent=2)

def extract_title_from_content(content: str, url: str) -> str:
    """Extract meaningful title from page content or URL."""
    if not content:
        return extract_title_from_url(url)
    
    # Try to extract title from common patterns in content
    content_lower = content.lower()
    
    # Look for common title patterns
    title_patterns = [
        r'(.*?)\s*[-|–]\s*.*',  # Title - Site pattern
        r'(.*?)\s*\|\s*.*',     # Title | Site pattern
        r'^([^•\n]{10,100})',   # First substantial line
    ]
    
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    if lines:
        first_line = lines[0]
        
        # Try patterns
        for pattern in title_patterns:
            match = re.match(pattern, first_line)
            if match:
                title = match.group(1).strip()
                if len(title) > 5 and not title.lower().startswith(('skip', 'navigation', 'menu')):
                    return title
        
        # If no pattern matches, use first line if it's reasonable
        if 5 <= len(first_line) <= 100 and not first_line.lower().startswith(('skip', 'navigation', 'menu')):
            return first_line
    
    # Fallback to URL-based title
    return extract_title_from_url(url)

def extract_title_from_url(url: str) -> str:
    """Extract a title from URL structure."""
    try:
        parsed = urlparse(url)
        
        # Handle search queries
        if 'search' in parsed.path or 'q=' in parsed.query:
            if 'q=' in parsed.query:
                from urllib.parse import parse_qs
                params = parse_qs(parsed.query)
                if 'q' in params:
                    return f"Search: {params['q'][0]}"
        
        # Use path segments
        path_parts = [part for part in parsed.path.split('/') if part and part != 'index.html']
        if path_parts:
            # Clean up the last path segment
            title = path_parts[-1].replace('-', ' ').replace('_', ' ')
            # Capitalize words
            title = ' '.join(word.capitalize() for word in title.split())
            return title
        
        # Use domain as fallback
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain.split('.')[0].capitalize()
    
    except:
        return 'Unknown Page'

def categorize_domain(domain: str, url: str, content: str) -> str:
    """Categorize a domain based on its name, URL patterns, and content."""
    domain_lower = domain.lower()
    url_lower = url.lower()
    content_lower = content.lower()
    
    # Social Media
    social_domains = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'tiktok', 'reddit', 'discord']
    if any(social in domain_lower for social in social_domains):
        return 'Social Media'
    
    # Search Engines
    search_domains = ['google', 'bing', 'yahoo', 'duckduckgo']
    if any(search in domain_lower for search in search_domains) and ('search' in url_lower or 'q=' in url_lower):
        return 'Search'
    
    # News & Media
    news_domains = ['news', 'cnn', 'bbc', 'reuters', 'ap', 'nbc', 'abc', 'cbs', 'fox', 'npr', 'bloomberg', 'techcrunch', 'wired']
    if any(news in domain_lower for news in news_domains):
        return 'News & Media'
    
    # Tech & Development
    tech_domains = ['github', 'stackoverflow', 'developer', 'docs', 'api', 'chrome', 'microsoft', 'apple']
    if any(tech in domain_lower for tech in tech_domains):
        return 'Technology'
    
    # E-commerce
    commerce_domains = ['amazon', 'ebay', 'shop', 'store', 'buy', 'cart']
    if any(commerce in domain_lower for commerce in commerce_domains):
        return 'E-commerce'
    
    # Education
    edu_domains = ['edu', 'university', 'college', 'learn', 'course', 'tutorial']
    if any(edu in domain_lower for edu in edu_domains):
        return 'Education'
    
    # Entertainment
    entertainment_domains = ['netflix', 'hulu', 'disney', 'spotify', 'music', 'game', 'entertainment']
    if any(ent in domain_lower for ent in entertainment_domains):
        return 'Entertainment'
    
    # Business Tools
    business_domains = ['calendar', 'email', 'office', 'workspace', 'drive', 'cloud', 'teams']
    if any(biz in domain_lower for biz in business_domains):
        return 'Business Tools'
    
    # Default category
    return 'Other' 
