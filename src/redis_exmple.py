import redis

redis_client=redis.Redis(host="127.0.0.1",port=6379,db=0,encoding="UTF-8",decode_responses=True)
redis_client.set("key","value")
redis_client.expire("key",10)

print(redis_client.get("key"))

