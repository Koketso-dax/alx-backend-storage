#!/usr/bin/env python3
""" Module for testing web.py """
import unittest
from unittest.mock import patch, MagicMock
from datetime import timedelta
from web import track_get_page, get_page, client
import time


class TestTrackGetPage(unittest.TestCase):
    @patch('web.client')
    def test_get_page_cached(self, mock_client):
        # Set up the mock Redis client to return a cached page
        mock_client.get.return_value = b'cached page'

        # Call the decorated function
        result = get_page('http://google.com')

        # Check that the result is the cached page
        self.assertEqual(result, 'cached page')

        # Check that the count was incremented
        mock_client.incr.assert_called_once_with('count:http://google.com')

        # Check that the page was not fetched from the network
        mock_client.setex.assert_not_called()

    @patch('web.client')
    @patch('web.requests.get')
    def test_get_page_uncached(self, mock_get, mock_client):
        # Set up the mock Redis client to return no cached page
        mock_client.get.return_value = None

        # Set up the mock requests.get function to return a response
        mock_response = MagicMock()
        mock_response.text = 'fetched page'
        mock_get.return_value = mock_response

        # Call the decorated function
        result = get_page('http://google.com')

        # Check that the result is the fetched page
        self.assertEqual(result, 'fetched page')

        # Check that the count was incremented
        mock_client.incr.assert_called_once_with('count:http://google.com')

        # Check that the page was fetched from the network and cached
        mock_get.assert_called_once_with('http://google.com')
        mock_client.set.assert_called_once_with('http://google.com',
                                                'fetched page', ex=timedelta(seconds=10))

    @patch('web.client')
    @patch('web.requests.get')
    def test_cache_expiration(self, mock_get, mock_client):
        # Set up the mock Redis client to return no cached page
        mock_client.get.return_value = None

        # Set up the mock requests.get function to return a response
        mock_response = MagicMock()
        mock_response.text = 'fetched page'
        mock_get.return_value = mock_response

        # Call the decorated function
        result = get_page('http://google.com')

        # Check that the result is the fetched page
        self.assertEqual(result, 'fetched page')

        # Check that the page was fetched from the network and cached
        mock_get.assert_called_once_with('http://google.com')
        mock_client.set.assert_called_once_with('http://google.com',
                                                'fetched page', ex=timedelta(seconds=10))

        # Wait for 10 seconds
        time.sleep(10)

        # Check that the page is no longer cached
        self.assertIsNone(client.get('http://google.com'))

    @patch('web.client')
    @patch('web.requests.get')
    def test_count_increment(self, mock_get, mock_client):
        # Set up the mock Redis client to return no cached page
        mock_client.get.return_value = None

        # Set up the mock requests.get function to return a response
        mock_response = MagicMock()
        mock_response.text = 'fetched page'
        mock_get.return_value = mock_response

        # Call the decorated function multiple times
        for i in range(5):
            result = get_page('http://google.com')

        # Check that the count was incremented correctly
        self.assertEqual(mock_client.incr.call_count, 5)

if __name__ == '__main__':
    unittest.main()
