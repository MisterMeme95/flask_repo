# tests/test_app.py

import unittest # Import the standard Python unit testing framework
import os       # Import the os module for interacting with the operating system

# Set an environment variable to indicate that tests are running.
# This is crucial for separating test database logic from production.
os.environ['TESTING'] = 'true'

# Import the Flask app instance and the TimelinePost model from your main application file.
# The 'app' variable usually refers to your `Flask(__name__)` instance.
# 'TimelinePost' is likely your Peewee model (or SQLAlchemy, Django ORM, etc.) for timeline entries.
from app import app, TimelinePost

# Define a test class that inherits from unittest.TestCase.
# Each method starting with 'test_' within this class will be run as a separate test.
class AppTestCase(unittest.TestCase):
    # setUp method is called before each individual test method (e.g., before test_home, before test_timeline).
    # It's used to set up the environment required for the tests.
    def setUp(self):
        # Create a test client for the Flask app.
        # This client simulates requests to your Flask application without needing a running server.
        self.client = app.test_client()
        # Create tables in the database specifically for testing.
        # This ensures a clean slate for each test to avoid interference from previous tests.
        TimelinePost.create_table()

    # tearDown method is called after each individual test method has completed.
    # It's used to clean up resources created during setUp or the test itself.
    def tearDown(self):
        # Drop tables after each test to ensure the database is clean and ready for the next test,
        # or for subsequent test runs.
        TimelinePost.drop_table()

    # Test case for the home page ("/")
    def test_home(self):
        # Send a GET request to the root URL of the application.
        response = self.client.get("/")
        # Assert that the HTTP status code of the response is 200 (OK).
        assert response.status_code == 200
        # Get the response data as a string (HTML content).
        html = response.get_data(as_text=True)
        # Assert that the expected title tag is present in the HTML.
        assert "<title>MLH Fellow</title>" in html
        # Additional home page test: Check if the word "timeline" (case-insensitive)
        # is present in the HTML content, indicating a link or reference to the timeline.

    # Test case for the timeline API endpoint ("/api/timeline_post")
    def test_timeline(self):
        # Test 1: Initial GET request should return an empty list of posts.
        response = self.client.get("/api/timeline_post")
        # Assert that the HTTP status code is 200.
        assert response.status_code == 200
        # Assert that the response content type is JSON.
        assert response.is_json
        # Parse the JSON response.
        json = response.get_json()
        # Assert that the JSON response contains a key named "timeline_posts".
        assert "timeline_posts" in json
        # Assert that the "timeline_posts" list is initially empty.
        assert len(json["timeline_posts"]) == 0

        # Test 2: POST a new timeline post.
        # Define the data to be sent in the POST request.
        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post!"
        }
        # Send a POST request to the timeline API endpoint with the defined data.
        post_response = self.client.post("/api/timeline_post", data=post_data)
        # Assert that the POST request was successful (HTTP status code 200).
        assert post_response.status_code == 200
        # Parse the JSON response from the POST request (usually returns the created object).
        post_json = post_response.get_json()
        # Assert that the returned JSON matches the data sent.
        assert post_json["name"] == "Test User"
        assert post_json["email"] == "test@example.com"
        assert post_json["content"] == "This is a test post!"

        # Test 3: GET request should now return one post.
        # Send another GET request to retrieve the timeline posts.
        response = self.client.get("/api/timeline_post")
        # Assert the status code is 200.
        assert response.status_code == 200
        # Parse the JSON response.
        json = response.get_json()
        # Assert "timeline_posts" key exists.
        assert "timeline_posts" in json
        # Assert that there is now exactly one post in the list.
        assert len(json["timeline_posts"]) == 1
        # Assert that the content of the retrieved post matches the one that was just created.
        assert json["timeline_posts"][0]["name"] == "Test User"
        assert json["timeline_posts"][0]["email"] == "test@example.com"
        assert json["timeline_posts"][0]["content"] == "This is a test post!"

    # Test case for handling malformed timeline post requests.
    def test_malformed_timeline_post(self):
        # Test 1: POST request missing the 'name' field.
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world, I'm John!"})
        # Assert that the request returns a 400 Bad Request status code.
        assert response.status_code == 400
        # Get the response data as text.
        html = response.get_data(as_text=True)
        # Assert that the response contains the specific error message for an invalid name.
        assert "Invalid name" in html

        # Test 2: POST request with empty 'content'.
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""})
        # Assert that the request returns a 400 Bad Request status code.
        assert response.status_code == 400
        # Get the response data as text.
        html = response.get_data(as_text=True)
        # Assert that the response contains the specific error message for invalid content.
        assert "Invalid content" in html

        # Test 3: POST request with a malformed 'email' address.
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        # Assert that the request returns a 400 Bad Request status code.
        assert response.status_code == 400
        # Get the response data as text.
        html = response.get_data(as_text=True)
        # Assert that the response contains the specific error message for an invalid email.
        assert "Invalid email" in html