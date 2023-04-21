# Yukai Shan
# yukais6@uci.edu
# 80365316

# use urllib to get json object
from datetime import datetime
import HolodexAPI as Holodex
import Visualizer

API_KEY = "b33eda39-dfb0-4337-9c8a-49cd8e69f5d5"


def input_date(msg: str) -> str:
    """
    Prompts the user for a date in the format YYYY-MM-DD
    :param str msg: The message to display to the user
    :return str: The date in the format YYYY-MM-DD
    """
    date_str = input(msg+" ")
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Incorrect data format, should be YYYY-MM-DD")
        return input_date(msg)
    return date_str


def validate_date_range(from_date: str, until_date: str) -> bool:
    """
    Validates that the date range provided is valid
    :param str from_date: The start date of the range (YYYY-MM-DD)
    :param str until_date: The end date of the range (YYYY-MM-DD)
    :return bool: True if the date range is valid ohtherwise False
    """
    if from_date > until_date:
        print("You need a time machine to get that kind of data")
        print("Plase enter a valid date range")
        return False
    return True


def main():
    """
    Main function for the program that takes in user input
    """
    print("This program only works with YouTube Virtual YouTuber channels\n" +
          "That are listed on holodex.net\n")
    channel_id = input("Please enter the channel ID:\n")
    print("Enter the date range for data collection\n")
    valid_date = False
    while not valid_date:
        from_when = input_date("From ( YYYY-MM-DD ):")
        until_when = input_date("Until ( YYYY-MM-DD ):")
        valid_date = validate_date_range(from_when, until_when)
    holodex = Holodex.HolodexAPI(API_KEY)
    vid_data = holodex.get_vid_data(from_when, until_when, channel_id, "50")
    if vid_data is None:
        print("No data and graph will be generated")
        return
    x_label = "Time since Livestream ID [@video]\n(hours)"
    y_label = "Livestream Duration\n(minutes)"
    date_stamp = from_when + " to " + until_when
    title = "Livestream Duration Visualization for @liver\n" + date_stamp
    Visualizer.plot_data(x_label, y_label, title, vid_data)


if __name__ == "__main__":
    main()
