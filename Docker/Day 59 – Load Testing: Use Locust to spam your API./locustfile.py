from locust import HttpUser, task, between
import random, uuid

MESSAGE = ["hello", "What is AI?", "explain machine learning", "hello", "What is AI?"]


class ChatUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(3)
    def chat(self):
        if random.random() < 0.7:
            message = random.choice(MESSAGE)
        else:
            message = f"tell me about topic {uuid.uuid4().hex[:6]}"
        self.client.post("/chat", json={"message": message}, name="/chat")

    @task(1)
    def healthcheck(self):
        self.client.get("/health", name="/health")
