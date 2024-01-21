#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" User Input Module

"""
import re
import sys
from typing import Dict, List, Tuple

from minim.exceptions import InputTooLongError, InvalidCharactersError
from minim.pkg_globals import USERNAME

ALLOWED_CHARS = r"[a-zA-Z0-9\s]"
DEFAULT_DOMAIN = (
    "You are an AI bot with a vast library of functions at your disposal. "
    "You can access and execute functions to accomplish various tasks "
    "across diverse domains, including coding, writing, data manipulation, "
    "and more. Your primary mode of operation is through function calls")
DEFAULT_TOPIC = "general"
MAX_LENGTH = 15


def update_topic():
    """Update the topic title"""
    try:
        new_topic = input(
            "Enter topic name (one word, maximum {} "
            "characters, no special characters): ".format(MAX_LENGTH))
        if len(new_topic) > MAX_LENGTH:
            raise InputTooLongError
        elif not re.match(ALLOWED_CHARS, new_topic):
            raise InvalidCharactersError
    except InputTooLongError:
        print(f'Input exceeds character limit ({MAX_LENGTH}).')
    except InvalidCharactersError:
        print("Input contains invalid characters. Please try again.")
    else:
        topic = new_topic
        print(f"Budd-E: Knowledge domain was changed successfully!")
        return topic


def minim_action(knowledge_domain: str, knowledge_topic: str, prompts: List,
                 user_prompt: str) -> Tuple[str, str, List]:
    """Budd-E action based on user prompts

    :param knowledge_domain: Knowledge domain for Budd-E
    :param knowledge_topic: Knowledge topic used for saving files
    :param prompts: List of prompts from user
    :param user_prompt: Prompt from user
    :return: Knowledge domain, Knowledge topic, list of prompts
    """

    if user_prompt == "minim.domain":
        new_domain = input(f'\nBudd-E: Which domain should I focus on?: ')
        knowledge_domain = new_domain
        knowledge_topic = update_topic()
        prompts = []
    elif user_prompt == "minim.domain.default":
        knowledge_domain = DEFAULT_DOMAIN
        knowledge_topic = DEFAULT_TOPIC
        print(f"Budd-E: Knowledge domain has been reverted back "
              f"to default!")
    elif user_prompt == "bye bud" or user_prompt == "exit":
        print(f"\nBudd-E: Goodbye {USERNAME}")
        sys.exit(0)

    return knowledge_domain, knowledge_topic, prompts


def user_input(knowledge_domain: str, knowledge_topic: str,
               prompts: List[Dict] = None) -> Tuple[str, str, Dict, List]:
    """User prompt helper

    :param knowledge_domain: Knowledge domain for Budd-E
    :param knowledge_topic: Knowledge topic used for saving files
    :param prompts: List of prompts from user
    :return: Knowledge domain, Knowledge topic, prompt, list of prompts
    """
    user_prompt = input(f'\n{USERNAME}: ')

    knowledge_domain, knowledge_topic, prompts = \
        minim_action(knowledge_domain=knowledge_domain,
                     knowledge_topic=knowledge_topic, prompts=prompts,
                     user_prompt=user_prompt)

    if (user_prompt == "minim.domain"
            or user_prompt == "minim.domain.default"):
        print(f'\nBudd-E: Now that my knowledge domain has been '
              f'updated, how can I help {USERNAME}?')
        user_prompt = input(f'\n{USERNAME}: ')

    prompt = {
        "role": "user",
        "parts": [{
            "text": knowledge_domain + "\n\n" + user_prompt
        }]
    }

    return knowledge_domain, knowledge_topic, prompt, prompts


if __name__ == "__main__":
    pass
