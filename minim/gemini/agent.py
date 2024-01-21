#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Gemini Agent Module

"""
import json
import os
import requests
import sys
from typing import Dict, List, Tuple

import minim.gemini.write_file_function as write_file
from minim.input import user_input
from minim.pkg_globals import PACKAGE_ROOT
from minim.utils import docker_secret

api_key = docker_secret("gemini")


def parse_function_response(prompt: List) -> Tuple[str, str]:
    """ Parse the response

    :param prompt: Prompt from user
    :return: Function being called and response
    """
    function_call = prompt[0]["functionCall"]
    function_name = function_call["name"]

    print(f'\nmini-M: Calling function {function_name}!')

    try:
        arguments = function_call["args"]

        if hasattr(write_file, function_name):
            function_response = getattr(write_file, function_name)(
                **arguments)
        else:
            function_response = "ERROR: Unknown function called..."
    except TypeError:
        function_response = "ERROR: Invalid arguments..."

    return function_name, function_response


def start_g_agent(prompt: Dict,
                  domain: str = None,
                  prompts: List[Dict] = None,
                  topic: str = None):
    """Start Gemini Agent

    :param prompt: Prompt from user
    :param domain: Knowledge domain
    :param prompts: List of prompts from user
    :param topic: Knowledge topic
    """
    knowledge_domain = domain
    knowledge_topic = topic

    if prompts is None:
        prompts = []

    prompts.append(prompt)

    dirname = PACKAGE_ROOT / "data/minim"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(f'{dirname}/{knowledge_topic}_history.json', "w") as f:
        json.dump(prompts, f, indent=4)

    data = {
        "contents": [prompts],
        "tools": [{
            "functionDeclarations": write_file.definitions
        }]
    }

    response = requests.post(f'https://generativelanguage.googleapis.com/'
                             f'v1beta/models/gemini-pro:generateContent?key='
                             f'{api_key}', json=data)

    if response.status_code != 200:
        print(response.text)
        print("ERROR: Unable to make request")
        sys.exit(1)

    response = response.json()

    if "content" not in response["candidates"][0]:
        print("ERROR: No content in response")
        print(response)
        sys.exit(1)

    prompt = response["candidates"][0]["content"]["parts"]
    prompts.append({
        "role": "model",
        "parts": prompt,
    })

    if "functionCall" in prompt[0]:
        content = prompt[0]["functionCall"]["args"]["content"]

        function_name, function_response = parse_function_response(
            prompt=prompt)

        prompt = {
            "role": "function",
            "parts": [{
                "functionResponse": {
                    "name": function_name,
                    "response": {
                        "name": function_name,
                        "content": content
                    }
                }
            }]
        }
    else:
        print(f'\nmini-M: {prompt[0]["text"]}')

        knowledge_domain, knowledge_topic, prompt, prompts = \
            user_input(knowledge_domain=knowledge_domain,
                       knowledge_topic=knowledge_topic,
                       prompts=prompts)

    start_g_agent(domain=knowledge_domain,
                  prompt=prompt,
                  prompts=prompts,
                  topic=knowledge_topic)

if __name__ == "__main__":
    pass
