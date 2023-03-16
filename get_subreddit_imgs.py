#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import urllib.request

import praw
from PIL import Image

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="get_subreddit_imgs",
        description="Downloads images from a subreddit",
    )
    parser.add_argument(
        "-s", "--subreddit", type=str, help="subreddit to download from", required=True
    )
    parser.add_argument("-p", "--posts", type=int, default=100)
    args = parser.parse_args()

    reddit = praw.Reddit("bot1", user_agent="bot1 user agent")
    subreddit = reddit.subreddit(args.subreddit)

    # create directory
    dir = f"{args.subreddit}_imgs"
    try:
        os.mkdir(dir)
    except OSError as error:
        print(error)

    for submission in subreddit.top(limit=args.posts):
        if submission.url.endswith(".jpg"):
            # download image
            image_name = f"{dir}/{submission.id}.jpg"
            urllib.request.urlretrieve(submission.url, image_name)
            print(f"downloaded: {image_name}")

            # resize image
            image = Image.open(image_name)
            # need to resize for best results in model training
            image.resize((512, 512)).save(
                f"{image_name.removesuffix('.jpg')}_resized.jpg"
            )
            os.remove(image_name)
            print(f"resized: {image_name}")
