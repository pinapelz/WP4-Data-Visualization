# Yukai Shan
# yukais6@uci.edu
# 80365316

import urllib.request
import json
from datetime import datetime


class HolodexException(Exception):
    """
    Exception class for HolodexAPI
    raised when the API key is not set
    """


class HolodexAPI():
    """
    Class for interacting with the Holodex API
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __handle_http_error__(self, ex: urllib.error.HTTPError) -> None:
        """
        Handles HTTP errors
        :param urllib.error.HTTPError e: The error to handle
        """
        print("HTTP Error: " + str(ex.code))
        if ex.code == 401:
            print("Please check that your API key is correct")
        elif ex.code == 404:
            print("Query not found. Please check your query parameters")

    def __handle_url_error__(self, ex: urllib.error.URLError) -> None:
        """
        Handles URL errors
        :param urllib.error.URLError e: The error to handle
        """
        print("URL Error: " + str(ex.reason))
        if ex.reason == "Name or service not known":
            print("Please check that you are connected to the internet")

    def _download_url(self, url: str) -> dict:
        if self.api_key is None:
            raise HolodexException("API key is not set")
        opener = urllib.request.build_opener()
        opener.addheaders = [('Authorization', self.api_key)]
        urllib.request.install_opener(opener)
        response = None
        r_obj = None
        response = urllib.request.urlopen(url)
        json_results = response.read()
        r_obj = json.loads(json_results)
        response.close()
        # This data isn't actually used, but it's nice to have a copy of it
        with open("holodex_data.json", "w", encoding="UTF-8") as file:
            json.dump(r_obj, file)
        return r_obj

    def get_vid_data(self, time_from: str, time_until: str, channel_id: str,
                     limit: str) -> dict:
        """
        Retrieve the data on all past streams in a
        date range for a channel from the Holodex API

        :param str time_from: The start date of the range (YYYY-MM-DD)
        :param str time_until: The end date of the range (YYYY-MM-DD)
        :param str channel_id: The ID of the channel to get data for
        :param str limit: The maximum number of videos
        :return dict: A dictionary of video data in a date range
        """
        time_from_obj = datetime.strptime(time_from, '%Y-%m-%d')
        time_from_iso = time_from_obj.isoformat()
        time_until_obj = datetime.strptime(time_until, '%Y-%m-%d')
        time_until_iso = time_until_obj.isoformat()
        base_url = "https://holodex.net/api/v2/videos"
        try:
            api_data = self._download_url(base_url+"?channel_id=" +
                                          channel_id+"&from="+time_from_iso +
                                          "&to=" + time_until_iso +
                                          "&status=past&limit="+limit)
            if api_data == []:
                raise HolodexException("No data found" +
                                       "check your query parameters")
        except urllib.error.HTTPError as ex:
            self.__handle_http_error__(ex)
            return None
        except urllib.error.URLError as ex:
            self.__handle_url_error__(ex)
            return None
        except HolodexException as ex:
            print("Holodex Exception: " + str(ex))
            return None

        return api_data
