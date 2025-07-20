# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert "About Me" in html
        assert "I'm a developer"

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post."
            }
        post_response = self.client.post("/api/timeline_post", data=post_data)
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Test User"
        assert post_json["email"] == "test@example.com"
        assert post_json["content"] == "This is a test post."

        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        get_json = get_response.get_json()
        assert len(get_json["timeline_posts"]) == 1
        assert get_json["timeline_posts"][0]["content"] == "This is a test post."

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
        "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

    # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
        "name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

    # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
        "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

