from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def test_sentiment(self):
        self.client.post("http://localhost:5000/sentiment", 
                         json={"text": "Locust testing is easy"},
                         headers={"Content-Type": "application/json"})