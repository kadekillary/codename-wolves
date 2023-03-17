#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import argparse
import urllib.request

import requests
from PIL import Image
from instagrapi import Client
from instagrapi.types import Media

from config import configs
from hey_gpt import hey_gpt
from img_model import LeapAI_Inference


def get_session() -> requests.Session:
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {configs['leapai_key']}",
    }

    session = requests.Session()
    session.headers.update(headers)
    return session


def remove_img(img_path: str) -> None:
    os.remove(img_path)


def download_and_resize_img(img_url: str, img_path: str) -> None:
    urllib.request.urlretrieve(img_url, img_path)
    image = Image.open(img_path)
    # instagram needs the image to be 1080x1080 not 512x512
    image.resize((1080, 1080)).save(img_path)


def post_to_ig(img_path: str, img_caption: str) -> Media:
    cl = Client()
    cl.login(configs["ig_user"], configs["ig_pass"])
    # Could eventually use GPT-4 to understand photo context
    # and write a funny/contextual caption
    media = cl.photo_upload(
        # type alignment
        img_path,
        img_caption,
    )
    return media


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model_id", type=str, required=True)
    parser.add_argument("-s", "--subreddit", type=str, required=True)
    parser.add_argument("-k", "--keyword", type=str, default="@me")
    args = parser.parse_args()

    s = get_session()

    img_prompt, img_caption = hey_gpt(args.subreddit, args.keyword)

    img_model = LeapAI_Inference(s, args.model_id)
    get_img = img_model.get_model_img(img_prompt)

    photo_path = "photo-to-upload.jpg"

    download_and_resize_img(get_img, photo_path)

    post_to_ig(photo_path, img_caption)

    remove_img(photo_path)
