#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Mini-M Module

"""
from dataclasses import dataclass
import os
import sys

from minim.gemini.agent import start_g_agent
from minim.gemini.gemini import Gemini


@dataclass
class MiniM:
    g_model_name: str = "gemini-pro"

    def __post_init__(self):
        # Gemini
        self.gemini = Gemini(model_name=self.g_model_name)

    def get_chat_response(self, prompt: str, stream=True) -> str:
        g_response = self._g_chat_response(prompt=prompt, stream=stream)
        return g_response

    def _g_chat_response(self, prompt: str, stream=True) -> str:
        response = self.gemini.get_chat_response(prompt, stream=stream)
        return response


if __name__ == "__main__":
    username = os.environ.get('COMPOSE_PROJECT_NAME')

    print(f"\nmini-M: Hi, {username}!")

    prompts = []

    default_domain = knowledge_domain = (
        "You are an AI bot with a vast library of functions at your disposal. "
        "You can access and execute functions to accomplish various tasks "
        "across diverse domains, including coding, writing, data manipulation, "
        "and more. Your primary mode of operation is through function calls"
    )

    user_prompt = input("\nYou: ")

    if user_prompt == "minim.domain":
        new_domain = input(f'\nmini-M: Which domain should I focus on?: ')
        knowledge_domain = new_domain
        print(f"mini-M: Knowledge domain was changed successfully!")
    elif user_prompt == "minim.domain.default":
        knowledge_domain = default_domain
        print(f"mini-M: Knowledge domain has been reverted back to default!")
    elif user_prompt == "bye bud":
        print(f"mini-M: Goodbye {username}")
        sys.exit(1)

    if (user_prompt == "minim.domain" or
            user_prompt == "minim.domain.default"):
        print(f"mini-M: Now that my knowledge domain has been updated,"
              f" how can I help you?")
        user_prompt = input("\nYou: ")

    prompt = {
        "role": "user",
        "parts": [{"text": knowledge_domain + "\n\n" + user_prompt}]
    }

    start_g_agent(domain=knowledge_domain, prompt=prompt,
                  prompts=prompts)
