import redis
import os
from dotenv import load_dotenv

load_dotenv()

class CacheManager:
    def __init__(self, host, port, password, *args, **kwargs):
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            *args,
            **kwargs
        )
        connection_status = self.redis_client.ping()
        if connection_status:
            print("Connection Succcesfully")

    def store_data(self, key, value, time_to_live=None):
        try:
            if time_to_live is None:
                self.redis_client.set(key, value)
            else:
                self.redis_client.setex(key, time_to_live, value)
        except redis.RedisError as e:
            print(f"An error ocurred while storing data in redis: {e}")

    def check_key(self, key):
        try:
            key_exists = self.redis_client.exists(key)
            if key_exists:
                ttl = self.redis_client.ttl(key)
                return True, ttl
            return False, None
            
        except redis.RedisError as e:
            print(f"An error ocurred while a key in Redis: {e}")
            return False, None
        
    def get_data(self, key):
        try:
            output = self.redis_client.get(key)
            if output is not None:
                result = output.decode("utf-8")
                return result
            else:
                return None
        except redis.RedisError as e:
            print(f"An error ocurred while retrieving data from Redis: {e}")

    def delete_data(self, key):
        try:
            output = self.redis_client.delete(key)
            return output == 1
        except redis.RedisError as e:
            print(f"An error ocurred while deleting fata from Redis: {e}")
            return False
    
    def delete_data_with_pattern(self, pattern):
        try:
            for key in self.redis_client.scan_iter(match=pattern):
                self.delete_data(key)
        except redis.RedisError as e:
            print(f"An error ocurred while deleting data from Redis; {e}")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
cache_manager = CacheManager(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD
)