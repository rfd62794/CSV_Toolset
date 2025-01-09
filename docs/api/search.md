# API Documentation Search

## Overview
The API documentation search system provides fast, accurate, and context-aware search capabilities across all API documentation. It uses Elasticsearch for efficient full-text search and supports advanced query features.

## Components

### 1. Search Engine
```python
class APIDocSearch:
    def __init__(self):
        self.es = Elasticsearch()
        self.index = "api_docs"
        
    def search(self, query: str, **kwargs) -> List[SearchResult]:
        """
        Perform a search across API documentation
        
        Args:
            query: Search query string
            **kwargs: Additional search parameters
            
        Returns:
            List of search results
        """
        body = self.build_query(query, **kwargs)
        results = self.es.search(index=self.index, body=body)
        return self.process_results(results)
```

### 2. Document Indexing
```python
class DocumentIndexer:
    def index_document(self, doc: APIDocument):
        """Index an API documentation document"""
        document = {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "path": doc.path,
            "type": doc.type,
            "module": doc.module,
            "tags": doc.tags,
            "updated_at": doc.updated_at
        }
        return self.es.index(
            index="api_docs",
            id=doc.id,
            body=document
        )
```

## Search Features

### 1. Query Building
```python
class QueryBuilder:
    def build_query(self, query: str, **kwargs) -> dict:
        """Build an Elasticsearch query"""
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "title^3",
                                    "content",
                                    "tags^2"
                                ]
                            }
                        }
                    ],
                    "filter": self.build_filters(**kwargs)
                }
            },
            "highlight": {
                "fields": {
                    "content": {},
                    "title": {}
                }
            }
        }
```

### 2. Result Processing
```python
@dataclass
class SearchResult:
    id: str
    title: str
    content: str
    path: str
    type: str
    module: str
    relevance: float
    highlights: List[str]

class ResultProcessor:
    def process_results(self, raw_results: dict) -> List[SearchResult]:
        """Process Elasticsearch results into SearchResult objects"""
        results = []
        for hit in raw_results["hits"]["hits"]:
            result = SearchResult(
                id=hit["_id"],
                title=hit["_source"]["title"],
                content=hit["_source"]["content"],
                path=hit["_source"]["path"],
                type=hit["_source"]["type"],
                module=hit["_source"]["module"],
                relevance=hit["_score"],
                highlights=self.extract_highlights(hit)
            )
            results.append(result)
        return results
```

## Integration

### 1. API Integration
```python
@app.route("/api/docs/search")
def search_api():
    query = request.args.get("q", "")
    filters = {
        "type": request.args.get("type"),
        "module": request.args.get("module")
    }
    
    results = api_search.search(query, **filters)
    return jsonify({
        "results": [asdict(r) for r in results]
    })
```

### 2. Frontend Integration
```javascript
class APISearchWidget {
    constructor(element) {
        this.element = element;
        this.searchInput = element.querySelector("input");
        this.resultsContainer = element.querySelector(".results");
        
        this.searchInput.addEventListener(
            "input",
            debounce(this.handleSearch.bind(this), 300)
        );
    }
    
    async handleSearch() {
        const query = this.searchInput.value;
        if (query.length < 2) return;
        
        const results = await this.fetchResults(query);
        this.displayResults(results);
    }
}
```

## Configuration

### 1. Search Settings
```yaml
search:
  index_name: "api_docs"
  min_score: 0.5
  max_results: 20
  highlight:
    pre_tags: ["<strong>"]
    post_tags: ["</strong>"]
    fragment_size: 150
    number_of_fragments: 3
  
  weights:
    title: 3
    content: 1
    tags: 2
    
  analyzers:
    default:
      type: "standard"
      stopwords: "_english_"
```

### 2. Indexing Settings
```yaml
indexing:
  batch_size: 100
  refresh_interval: "1s"
  number_of_shards: 1
  number_of_replicas: 1
  
  mappings:
    properties:
      title:
        type: "text"
        analyzer: "standard"
      content:
        type: "text"
        analyzer: "standard"
      tags:
        type: "keyword"
```

## Performance

### 1. Caching
```python
class SearchCache:
    def __init__(self):
        self.cache = TTLCache(
            maxsize=1000,
            ttl=3600
        )
    
    def get_cached_results(
        self,
        query: str,
        **kwargs
    ) -> Optional[List[SearchResult]]:
        """Get cached search results"""
        cache_key = self.generate_cache_key(query, **kwargs)
        return self.cache.get(cache_key)
```

### 2. Query Optimization
```python
class QueryOptimizer:
    def optimize_query(self, query: dict) -> dict:
        """Optimize an Elasticsearch query"""
        return {
            **query,
            "_source": {
                "includes": [
                    "title",
                    "path",
                    "type",
                    "module"
                ]
            },
            "size": 20,
            "track_scores": True
        }
```

## Monitoring

### 1. Search Analytics
```python
class SearchAnalytics:
    def track_search(self, query: str, results: List[SearchResult]):
        """Track search analytics"""
        analytics = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "results_count": len(results),
            "top_result": results[0].id if results else None,
            "response_time": self.response_time
        }
        self.store_analytics(analytics)
```

### 2. Performance Monitoring
```python
class SearchMonitor:
    def monitor_performance(self):
        """Monitor search performance metrics"""
        return {
            "query_time_avg": self.calculate_avg_query_time(),
            "cache_hit_rate": self.calculate_cache_hit_rate(),
            "zero_results_rate": self.calculate_zero_results_rate(),
            "popular_queries": self.get_popular_queries()
        }
```

## Security

### 1. Query Sanitization
```python
class QuerySanitizer:
    def sanitize_query(self, query: str) -> str:
        """Sanitize search query"""
        # Remove potential injection attempts
        sanitized = re.sub(r'[^\w\s-]', '', query)
        # Limit query length
        return sanitized[:100]
```

### 2. Access Control
```python
class SearchSecurity:
    def check_access(self, user: User, doc: APIDocument) -> bool:
        """Check if user has access to document"""
        if doc.is_public:
            return True
        return user.has_access_to(doc.module)
``` 