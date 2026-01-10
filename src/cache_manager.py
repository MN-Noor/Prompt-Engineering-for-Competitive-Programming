import os
import json

class CacheManager:
    def __init__(self, cache_path):
        self.cache_path = cache_path
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_reasoning(self, problem_id):
        return self.cache.get(problem_id)

    def save_reasoning(self, problem_id, reasoning):
        self.cache[problem_id] = reasoning
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)