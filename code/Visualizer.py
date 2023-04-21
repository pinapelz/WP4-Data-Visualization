# Yukai Shan
# yukais6@uci.edu
# 80365316

from datetime import datetime
import matplotlib.pyplot as plt


def process_data(vids: list):
    """
    Split the data from Holodex API into list of deltas
    and list of stream durations. Skips streams that are not
    streamed on YouTube as they do not have a published date

    :param list vids: List of videos from Holodex API
    :return: List of hours since the latest video, list of video durations
             latest video id, streamer English name
    """
    # API iso format for date and time
    iso_format = "%Y-%m-%dT%H:%M:%S.000Z"
    # Get the date of the latest video
    start_index = 0
    for i, vid in enumerate(vids):
        try:
            latest_video_date = vid['published_at']
            latest_video_id = vid['id']
            liver_name = vid['channel']['english_name']
            start_index = i
            break
        except KeyError:
            print("Latest stream not on YouTube. Checking next stream...")
    latest_video_date = datetime.strptime(latest_video_date, iso_format)
    list_of_deltas = []  # List of hours since the latest video
    list_of_duration = []  # List of video duration in minutes
    for i in range(start_index, len(vids)):
        try:
            # Getting delta time since the latest video
            published_date = vids[i]['published_at']
            published = datetime.strptime(published_date, iso_format)
            # deltatime objet since the latest video
            delta_time = latest_video_date - published
            delta_hours = int(delta_time.total_seconds() // 3600)
            # Getting video duration in minutes
            duration = int(vids[i]['duration'])
            minutes = duration // 60
            list_of_duration.append(minutes)
            list_of_deltas.append(delta_hours)
        except KeyError:
            # If the video is not streamed on YouTube
            # it will not have a published date So we will skip it
            print("Skipped video " + vids[i]['id'] +
                  "it's not streamed on YouTube")
    return (list_of_deltas, list_of_duration, latest_video_id, liver_name)


def remove_zeroes(x_data: list, y_data: list):
    """
    Removs stream durations that are 0 minutes long
    :param list x_data: List of hours since closest stream to end range date
    :param list y_data: List of video durations
    :return: x_data and y_data with 0 minutes long streams removed
    """
    new_x = []
    new_y = []
    for i, y in enumerate(y_data):
        if y != 0:
            new_x.append(x_data[i])
            new_y.append(y)
    return new_x, new_y


def plot_data(x_label: str, y_label: str, title: str, videos: list):
    """
    Plots the data from Holodex API into a graph

    :param str x_label: Label for the x axis
    :param str y_label: Label for the y axis
    :param str title: Title of the graph
    :param list videos: List of JSON video data strings from Holodex API
    """
    parsed_data = process_data(videos)
    x_data = parsed_data[0]
    y_data = parsed_data[1]
    latest_video_id = parsed_data[2]
    liver_name = parsed_data[3]
    x_data, y_data = remove_zeroes(x_data, y_data)
    print(x_data)
    print(y_data)
    # Replacing the @video and @liver with the latest video id and streamer
    x_label = x_label.replace("@video", latest_video_id)
    title = title.replace("@liver", liver_name)
    plt.style.use('seaborn')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_data, y_data, marker='o', linestyle='none', color='red')
    plt.savefig("WorkoutProject4-yukais6.jpg")
