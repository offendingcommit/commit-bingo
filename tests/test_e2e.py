import unittest
import threading
import time
import multiprocessing
import requests
from unittest.mock import patch
import sys
import os
import signal
from contextlib import contextmanager

# Create a context manager to run the server in another process for e2e tests
@contextmanager
def run_app_in_process(timeout=10):
    """Run the app in a separate process and yield a client session."""
    # Define a function to run the app
    def run_app():
        # Add the parent directory to path so we can import the app
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        try:
            # Import and run the app
            from app import main
            main()
        except Exception as e:
            print(f"Error in app process: {e}")
            
    # Start the process
    process = multiprocessing.Process(target=run_app)
    process.start()
    
    try:
        # Wait for the app to start up
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check if the server is responding
                response = requests.get("http://localhost:8080", timeout=0.1)
                if response.status_code == 200:
                    # Server is up
                    break
            except requests.exceptions.RequestException:
                # Server not yet started, wait a bit
                time.sleep(0.1)
        else:
            raise TimeoutError("Server did not start within the timeout period")
        
        # Yield control back to the test
        yield
    finally:
        # Clean up: terminate the process
        process.terminate()
        process.join(timeout=5)
        if process.is_alive():
            os.kill(process.pid, signal.SIGKILL)


class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for the app. These tests require the app to be running."""
    
    @unittest.skip("Skip E2E test that requires running a server - only run manually")
    def test_home_page_loads(self):
        """Test that the home page loads and contains the necessary elements."""
        with run_app_in_process():
            # Make a request to the home page
            response = requests.get("http://localhost:8080")
            self.assertEqual(response.status_code, 200)
            
            # Check for the presence of key elements in the HTML
            self.assertIn("COMMIT !BINGO", response.text)
            self.assertIn("FREE MEAT", response.text)
            
            # The board should have 5x5 = 25 cells
            # Look for cards or grid elements
            self.assertIn("board-container", response.text)
    
    @unittest.skip("Skip E2E test that requires running a server - only run manually")
    def test_stream_page_loads(self):
        """Test that the stream page loads and contains the necessary elements."""
        with run_app_in_process():
            # Make a request to the stream page
            response = requests.get("http://localhost:8080/stream")
            self.assertEqual(response.status_code, 200)
            
            # Check for the presence of key elements in the HTML
            self.assertIn("COMMIT !BINGO", response.text)
            self.assertIn("FREE MEAT", response.text)
            
            # The board should be present
            self.assertIn("stream-board-container", response.text)
            
            # The stream page should have a different background color
            self.assertIn("#00FF00", response.text)  # STREAM_BG_COLOR

if __name__ == '__main__':
    unittest.main()