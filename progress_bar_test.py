import unittest
from io import BytesIO
from flask import Flask
from html2image import Html2Image
from progress_bar import app, calculate_percentage, create_html_content


class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup the test client"""
        cls.client = app.test_client()

    def test_calculate_percentage(self):
        """Test the calculate_percentage function"""
        self.assertEqual(calculate_percentage(50, 100), 50.0)
        self.assertEqual(calculate_percentage(0, 100), 0.0)
        self.assertEqual(calculate_percentage(5, 0), 0.0)
        self.assertEqual(calculate_percentage(10, 20), 50.0)

    def test_create_html_content(self):
        """Test the create_html_content function"""
        html = create_html_content(
            "Test Progress", 50, 100, 50.0, '#4caf50', 400, 50, 16, 'Roboto')
        self.assertIn('<div class="progress-container">', html)
        self.assertIn('font-family: \'Roboto\', Arial, sans-serif;', html)
        # Ensure progress bar width is set to 50%
        self.assertIn('width: 50.0%;', html)

    def test_progress_bar_route(self):
        """Test the /progress-bar route"""
        response = self.client.get(
            '/progress-bar?x=50&y=100&color=4caf50&label=Test&width=400&height=50&fontsize=16&font=Roboto')

        # Check if the response is valid (status code 200)
        self.assertEqual(response.status_code, 200)

        # Check if the response is an image (Content-Type should be 'image/png')
        self.assertEqual(response.content_type, 'image/png')

        # Check if the response contains image data
        img_data = BytesIO(response.data)
        img_data.seek(0)
        self.assertGreater(len(img_data.read()), 0)

    def test_progress_bar_missing_params(self):
        """Test the /progress-bar route with missing parameters (should handle default values)"""
        response = self.client.get('/progress-bar')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/png')

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        # No specific clean up is needed as we are using the Flask test client
        pass


if __name__ == '__main__':
    unittest.main()
