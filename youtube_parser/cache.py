from typing import Optional, List, Dict

import redis


class RedisCache:
    def __init__(self, db: int):
        self._redis = redis.Redis(host="redis", port=6379, db=db)

    def set(self, name: str, value: str) -> None:
        self._redis.set(name, value)

    def mset(self, mapping: Dict[str, str]):
        self._redis.mset(mapping)

    def get(self, name: str) -> Optional[str]:
        return self._redis.get(name)

    def filter(self, names: List[str]) -> List[str]:
        """
        :return only unique names
        """
        result: List[str] = []
        redis_names = self._redis.mget(names)

        for name, exists in zip(names, redis_names):
            if exists is None:
                result.append(name)

        return result
