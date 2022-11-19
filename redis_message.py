from redis import Redis


class RedisMessage:
    def __init__(self) -> None:
        self.redis: Redis = ...

    def connect(self, host, port):
        try:
            self.redis = Redis(host=host, port=port, decode_responses=True)
            self.redis.ping()
            return True
        except:
            return False


class Server(RedisMessage):
    def __init__(self):
        super().__init__()

    def send_message(self, channel, msg):
        self.redis.publish(channel=channel, message=msg)

    def receive_messages(self, channel, set_message):
        subscriber = self.redis.pubsub(ignore_subscribe_messages=True)
        subscriber.subscribe(channel)
        for msg in subscriber.listen():
            set_message(msg['data'])
