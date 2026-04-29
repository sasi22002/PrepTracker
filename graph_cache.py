import os
import threading
import time
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphCache:
    """Thread-safe cache for generated graphs with automatic cleanup"""
    
    def __init__(self, cache_dir: str = "graph_cache", max_age_hours: int = 24):
        self.cache_dir = cache_dir
        self.max_age = timedelta(hours=max_age_hours)
        self.lock = threading.Lock()
        self._cache_index = {}
        
        # Create cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load existing cache index
        self._load_cache_index()
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def _load_cache_index(self):
        """Load cache index from file"""
        index_file = os.path.join(self.cache_dir, "cache_index.json")
        try:
            if os.path.exists(index_file):
                with open(index_file, 'r') as f:
                    self._cache_index = json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cache index: {e}")
            self._cache_index = {}
    
    def _save_cache_index(self):
        """Save cache index to file"""
        index_file = os.path.join(self.cache_dir, "cache_index.json")
        try:
            with open(index_file, 'w') as f:
                json.dump(self._cache_index, f)
        except Exception as e:
            logger.warning(f"Failed to save cache index: {e}")
    
    def _get_cache_key(self, graph_type: str, params: Dict = None) -> str:
        """Generate cache key based on graph type and parameters"""
        key_data = f"{graph_type}_{json.dumps(params or {}, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_file_path(self, cache_key: str) -> str:
        """Get file path for cached graph"""
        return os.path.join(self.cache_dir, f"{cache_key}.png")
    
    def get_cached_graph(self, graph_type: str, params: Dict = None) -> Optional[str]:
        """Get cached graph as base64 string"""
        cache_key = self._get_cache_key(graph_type, params)
        
        with self.lock:
            if cache_key not in self._cache_index:
                return None
            
            cache_info = self._cache_index[cache_key]
            cache_time = datetime.fromisoformat(cache_info['timestamp'])
            
            # Check if cache is still valid
            if datetime.now() - cache_time > self.max_age:
                self._remove_cache_entry(cache_key)
                return None
            
            # Check if file exists
            cache_file = self._get_cache_file_path(cache_key)
            if not os.path.exists(cache_file):
                self._remove_cache_entry(cache_key)
                return None
            
            # Read and return cached graph
            try:
                with open(cache_file, 'rb') as f:
                    import base64
                    return base64.b64encode(f.read()).decode('utf-8')
            except Exception as e:
                logger.warning(f"Failed to read cached graph {cache_key}: {e}")
                self._remove_cache_entry(cache_key)
                return None
    
    def cache_graph(self, graph_type: str, graph_data: str, params: Dict = None):
        """Cache graph data"""
        cache_key = self._get_cache_key(graph_type, params)
        cache_file = self._get_cache_file_path(cache_key)
        
        try:
            # Save graph to file
            import base64
            graph_bytes = base64.b64decode(graph_data)
            with open(cache_file, 'wb') as f:
                f.write(graph_bytes)
            
            # Update cache index
            with self.lock:
                self._cache_index[cache_key] = {
                    'graph_type': graph_type,
                    'timestamp': datetime.now().isoformat(),
                    'params': params or {}
                }
                self._save_cache_index()
            
            logger.info(f"Cached graph {graph_type} with key {cache_key}")
            
        except Exception as e:
            logger.error(f"Failed to cache graph {graph_type}: {e}")
    
    def _remove_cache_entry(self, cache_key: str):
        """Remove cache entry and file"""
        if cache_key in self._cache_index:
            del self._cache_index[cache_key]
        
        cache_file = self._get_cache_file_path(cache_key)
        try:
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except Exception as e:
            logger.warning(f"Failed to remove cache file {cache_file}: {e}")
    
    def _start_cleanup_thread(self):
        """Start background thread for cache cleanup"""
        def cleanup():
            while True:
                time.sleep(3600)  # Run cleanup every hour
                self._cleanup_expired_cache()
        
        cleanup_thread = threading.Thread(target=cleanup, daemon=True)
        cleanup_thread.start()
    
    def _cleanup_expired_cache(self):
        """Remove expired cache entries"""
        with self.lock:
            expired_keys = []
            current_time = datetime.now()
            
            for cache_key, cache_info in self._cache_index.items():
                cache_time = datetime.fromisoformat(cache_info['timestamp'])
                if current_time - cache_time > self.max_age:
                    expired_keys.append(cache_key)
            
            for cache_key in expired_keys:
                self._remove_cache_entry(cache_key)
            
            if expired_keys:
                self._save_cache_index()
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def clear_cache(self):
        """Clear all cache entries"""
        with self.lock:
            for cache_key in list(self._cache_index.keys()):
                self._remove_cache_entry(cache_key)
            self._save_cache_index()
            logger.info("Cleared all cache entries")

# Global cache instance
graph_cache = GraphCache()

class BackgroundGraphGenerator:
    """Background graph generation with caching"""
    
    def __init__(self):
        self.pending_tasks = {}
        self.lock = threading.Lock()
    
    def generate_graph_async(self, graph_type: str, generator_func: Callable, params: Dict = None) -> bool:
        """Start graph generation in background thread"""
        cache_key = graph_cache._get_cache_key(graph_type, params)
        
        # Check if graph is already cached or being generated
        with self.lock:
            if cache_key in self.pending_tasks:
                return False  # Already being generated
            
            # Check cache first
            cached_graph = graph_cache.get_cached_graph(graph_type, params)
            if cached_graph:
                return False  # Already cached
        
        # Start background generation
        def generate_and_cache():
            try:
                logger.info(f"Starting background generation for {graph_type}")
                graph_data = generator_func()
                
                if graph_data:
                    graph_cache.cache_graph(graph_type, graph_data, params)
                    logger.info(f"Successfully generated and cached {graph_type}")
                else:
                    logger.warning(f"Failed to generate {graph_type}")
                    
            except Exception as e:
                logger.error(f"Error generating {graph_type}: {e}")
            finally:
                # Remove from pending tasks
                with self.lock:
                    if cache_key in self.pending_tasks:
                        del self.pending_tasks[cache_key]
        
        # Add to pending tasks and start thread
        with self.lock:
            self.pending_tasks[cache_key] = True
        
        thread = threading.Thread(target=generate_and_cache, daemon=True)
        thread.start()
        
        return True
    
    def is_generating(self, graph_type: str, params: Dict = None) -> bool:
        """Check if graph is currently being generated"""
        cache_key = graph_cache._get_cache_key(graph_type, params)
        with self.lock:
            return cache_key in self.pending_tasks

# Global background generator instance
background_generator = BackgroundGraphGenerator()
