#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import json
import time
import argparse
from typing import Optional
from dataclasses import dataclass

import requests


leap_ai_urls = {
    "create_model": "https://api.tryleap.ai/api/v1/images/models",
    "upload_images": "https://api.tryleap.ai/api/v1/images/models/{model_id}/samples",
    "queue_training": "https://api.tryleap.ai/api/v1/images/models/{model_id}/queue",
    "check_training": "https://api.tryleap.ai/api/v1/images/models/{model_id}/versions/{version_id}",
    "create_image": "https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences",
    "check_image": "https://api.tryleap.ai/api/v1/images/models/{model_id}/inferences/{inference_id}",
}


@dataclass
class File:
    name: str

    def to_fmt(self) -> tuple:
        return (self.name, open(self.name, "rb"), "image/jpeg")


class LeapAI_Tuner:
    def __init__(
        self, session: requests.Session, keyword: str, title: str, imgs_path: str
    ):
        self.session = session
        self.keyword = keyword
        self.title = title
        self.imgs_path = imgs_path
        self._model_id = None

    def _create_model(self) -> int:
        payload = {
            "title": self.title,
            "subjectKeyword": self.keyword,
        }

        response = self.session.post(leap_ai_urls["create_model"], json=payload)
        response.raise_for_status()
        model_id = json.loads(response.text)["id"]
        self._model_id = model_id
        print(f"model_id: {model_id}")
        return model_id

    def _upload_imgs_to_model(self) -> None:
        all_imgs = glob.glob(f"{self.imgs_path}/*.jpeg")

        del self.session.headers["content-type"]

        for img in all_imgs:
            print(f"uploading image: {img}")
            files = {"files": File(img).to_fmt()}
            response = self.session.post(
                leap_ai_urls["upload_images"].format(model_id=self._model_id),
                files=files,
            )
            response.raise_for_status()

    def _check_training(self, version_id: str) -> str:
        response = self.session.get(
            leap_ai_urls["check_training"].format(
                model_id=self._model_id, version_id=version_id
            )
        )
        response.raise_for_status()
        status = json.loads(response.text)["status"]
        return status

    def _queue_training(self) -> None:
        response = self.session.post(
            leap_ai_urls["queue_training"].format(model_id=self._model_id)
        )
        response.raise_for_status()
        data = json.loads(response.text)
        version_id = data["id"]

        while (status := self._check_training(version_id)) != "finished":
            print(f"training status: {status}")
            time.sleep(10)
        print("training status: finished!")

    def tune_model(self) -> None:
        self._create_model()
        self._upload_imgs_to_model()
        self._queue_training()


class LeapAI_Inference:
    def __init__(self, session: requests.Session, model_id: int):
        self.session = session
        self.model_id = model_id

    def _check_img(self, inference_id: str, img_url: Optional[str]) -> Optional[str]:
        if img_url:
            return img_url

        response = self.session.get(
            leap_ai_urls["check_image"].format(
                model_id=self.model_id, inference_id=inference_id
            )
        )
        response.raise_for_status()
        data = json.loads(response.text)
        status = data["state"]
        print(f"image status: {status}")

        if status != "finished":
            time.sleep(10)
            return self._check_img(inference_id, None)
        else:
            return self._check_img(inference_id, data["images"][0]["uri"])

    def get_model_img(
        self,
        prompt: str,
        width: int = 512,
        height: int = 512,
        steps: int = 50,
    ) -> Optional[str]:
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "steps": steps,
        }
        response = self.session.post(
            leap_ai_urls["create_image"].format(model_id=self.model_id), json=payload
        )
        response.raise_for_status()
        inference_id = json.loads(response.text)["id"]

        img_url = self._check_img(inference_id, None)

        return img_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, help="path to images", required=True)
    parser.add_argument("-k", "--keyword", default="@me")
    parser.add_argument("-t", "--title", default="my_model")
    args = parser.parse_args()

    from config import configs

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {configs['leapai_key']}",
    }

    session = requests.Session()
    session.headers.update(headers)

    tuner = LeapAI_Tuner(session, args.keyword, args.title, args.path)
    tuner.tune_model()
