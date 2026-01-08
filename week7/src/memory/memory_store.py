import redis
import json

class RedisChatMemory:
    def __init__(self, host='localhost', port=6379, db=0, window_size=5):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.window_size = window_size

    def export_to_json(self, session_id, filename="HISTORY-LOGS.json"):
        history = self.get_history(session_id)
        log_data = {session_id: history}
        
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=4)

    def save_message(self, session_id, role, content):
        key = f"chat:{session_id}"
        message = json.dumps({"role": role, "content": content})
        self.redis_client.rpush(key, message)
        self.redis_client.ltrim(key, -self.window_size, -1)
        self.redis_client.expire(key, 86400)  # auto delete after 24 hours

    def get_history(self, session_id):
        key = f"chat:{session_id}"
        raw_history = self.redis_client.lrange(key, 0, -1)
        return [json.loads(msg) for msg in raw_history]