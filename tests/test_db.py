# tests/test_db.py

# Import necessary libraries for testing and database operations.
import unittest  # Python's built-in testing framework.
from peewee import * # The ORM for interacting with the database.



# Import the specific model we intend to test from our main application.
from app import TimelinePost

# A list of all models the test database will use.
# This makes it easy to manage table creation and deletion.
MODELS = [TimelinePost]

# Configure the tests to use an in-memory SQLite database.
# This is ideal for testing because it's fast, isolated, and requires no setup.
# The ':memory:' flag means the database exists only in RAM and is gone when the connection is closed.
test_db = SqliteDatabase(':memory:')


class TestTimelinePost(unittest.TestCase):
    """
    A test suite for the TimelinePost model.
    """

    def setUp(self):
        """
        This method is run before each test in this class.
        It sets up a clean database environment for each test.
        """
        # Bind the models to the in-memory database. This tells Peewee to direct
        # all database operations for these models to our temporary test_db.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        # Connect to the database and create the required tables.
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        """
        This method is run after each test in this class.
        It cleans up the database environment to ensure tests are isolated.
        """
        # Drop the tables to wipe all data. This is crucial so that one test
        # doesn't affect the outcome of another.
        test_db.drop_tables(MODELS)

        # Close the database connection to free up resources.
        test_db.close()

    def test_timeline_post(self):
        """
        Tests the creation and retrieval of TimelinePost records.
        """
        # Create two new timeline posts in the test database.
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        # Assert that the first post created gets an auto-incrementing ID of 1.
        assert first_post.id == 1

        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        # Assert that the second post created gets an ID of 2.
        assert second_post.id == 2

        # Retrieve all timeline posts from the database, ordered by their ID.
        posts = TimelinePost.select().order_by(TimelinePost.id)

        # Verify that the query returned the correct number of posts.
        assert len(posts) == 2

        # Check that the data for the first post matches what was created.
        assert posts[0].name == 'John Doe'
        assert posts[0].email == 'john@example.com'
        assert posts[0].content == "Hello world, I'm John!"

        # Check that the data for the second post matches what was created.
        assert posts[1].name == 'Jane Doe'
        assert posts[1].email == 'jane@example.com'
        assert posts[1].content == "Hello world, I'm Jane!"