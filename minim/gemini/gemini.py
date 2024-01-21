#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Gemini Module

"""
from dataclasses import dataclass

import google.generativeai as genai

from minim.pkg_globals import USERNAME
from minim.utils import docker_secret

genai.configure(api_key=docker_secret("gemini"))


@dataclass
class Gemini:
    model_name: str = "gemini-pro"

    def __post_init__(self):
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=[])
        self.chat_history = self.chat.history

    def get_chat_response(self, prompt: str, stream=True) -> str:
        response = self.chat.send_message(prompt, stream=stream)
        for i, chunk in enumerate(response):
            if i == 0:
                print(f'\nmini-M (Gemini): ...')
            print(chunk.text, end="", flush=True)
        print("\n")
        response.resolve()
        return response


if __name__ == "__main__":
    gemini = Gemini()

    while True:
        message = input(f'{USERNAME}: ')
        if message == "quit":
            break
        elif message == "chat.history":
            print(gemini.chat_history)
        elif message == "model.gemini-pro":
            gemini = Gemini()
        elif message == "model.gemini-vision":
            gemini = Gemini(model_name="gemini-pro-vision")
        else:
            response = gemini.get_chat_response(prompt=message)
            print("Gemini: " + response)
