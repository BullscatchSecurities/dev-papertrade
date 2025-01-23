
import os
import redis
from redis import ConnectionPool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
REDIS_CONNECTION = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_PORT", 6379) 


try:
    REDIS_CONNECTION_POOL = ConnectionPool(
        host=REDIS_CONNECTION,
        port=REDIS_PORT,
        db=0,
        max_connections=560,
        password=REDIS_PASSWORD,
    )

    # Create Redis client
    REDIS_CLIENT = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)

    # Test connection
    REDIS_CLIENT.ping()
    print("Redis connection successful!")

except redis.ConnectionError as e:
    print(f"Redis connection failed: {e}")
    REDIS_CLIENT = None
except Exception as e:
    print(f"An error occurred: {e}")
    REDIS_CLIENT = None



# # from redis_config import REDIS_CLIENT

# if REDIS_CLIENT:
#     try:
#         # Example: Set a key-value pair
#         REDIS_CLIENT.set("test_key", "test_value")
#         print("Value set in Redis:", REDIS_CLIENT.get("test_key").decode("utf-8"))
#     except Exception as e:
#         print(f"An error occurred while using Redis: {e}")
# else:
#     print("Redis client is not initialized. Check the connection settings.")



