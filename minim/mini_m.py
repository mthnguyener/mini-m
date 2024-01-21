#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Mini-M Module

"""
from dataclasses import dataclass

from minim.gemini.agent import start_g_agent
from minim.gemini.gemini import Gemini
from minim.input import DEFAULT_DOMAIN, DEFAULT_TOPIC, user_input
from minim.pkg_globals import USERNAME

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
    print(f"\nmini-M: Hi, {USERNAME}!")

    knowledge_domain = DEFAULT_DOMAIN
    knowledge_topic = DEFAULT_TOPIC

    knowledge_domain, knowledge_topic, prompt, prompts = \
        user_input(knowledge_domain=knowledge_domain,
                   knowledge_topic=knowledge_topic)

    start_g_agent(domain=knowledge_domain,
                  prompt=prompt,
                  prompts=prompts,
                  topic=knowledge_topic)
