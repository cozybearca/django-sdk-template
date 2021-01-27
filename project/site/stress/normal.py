from locust import constant, task
from locust.contrib.fasthttp import FastHttpUser


class NormalUser(FastHttpUser):
    weight = 1
    wait_time = constant(1)
    network_timeout = 0.05

    @task
    def index_page(self):
        self.client.get("/")


class BrowseImage(FastHttpUser):
    weight = 10
    wait_time = constant(1)
    network_timeout = 0.05

    @task
    def get_image(self):
        self.client.get("/media/product-images/0_8xY6j9u.png_compressed.jpg")
