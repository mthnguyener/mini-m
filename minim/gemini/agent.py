#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Gemini Agent Module

"""
import json
import os
import requests
import sys
from typing import Dict, List

import minim.gemini.write_file_function as write_file
from minim.pkg_globals import PACKAGE_ROOT
from minim.utils import docker_secret

api_key = docker_secret("gemini")


def parse_function_response(prompt: List):
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


def start_g_agent(prompt: Dict, domain: str = None, prompts: List[Dict] = None):
    default_domain = knowledge_domain = domain

    if prompts is None:
        prompts = []

    prompts.append(prompt)

    dirname = PACKAGE_ROOT / "data/minim"

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(f'{dirname}/history.json', "w") as f:
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
        "parts": prompt
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

        user_prompt = input("\nYou: ")

        if user_prompt == "minim.domain":
            new_domain = input(f'\nmini-M: Which domain should I focus on?: ')
            knowledge_domain = new_domain
            print(f"mini-M: Knowledge domain was changed successfully!")
        elif user_prompt == "minim.domain.default":
            knowledge_domain = default_domain
            print(f"mini-M: Knowledge domain has been reverted back "
                  f"to default!")
        elif user_prompt == "bye bud":
            print(f"mini-M: Goodbye "
                  f"{os.environ.get('COMPOSE_PROJECT_NAME')}")
            sys.exit(1)

        if (user_prompt == "minim.domain" or
                user_prompt == "minim.domain.default"):
            print(f"mini-M: Now that my knowledge domain has been "
                  f"updated, how can I help you?")
            user_prompt = input("\nYou: ")

        prompt = {
            "role": "user",
            "parts": [{"text": knowledge_domain + "\n\n" + user_prompt}]
        }

    start_g_agent(domain=knowledge_domain, prompt=prompt, prompts=prompts)


if __name__ == "__main__":
    username = os.environ.get('COMPOSE_PROJECT_NAME')

    print(f"mini-M: Hiya, {username}! How can I help you?")

    prompts = []

    default_domain = (
        "You are an AI bot with a vast library of functions at your disposal. "
        "You can access and execute functions to accomplish various tasks "
        "across diverse domains, including coding, writing, data manipulation, "
        "and more. Your primary mode of operation is through function calls"
    )

    user_prompt = input("\nYou: ")

    knowledge_domain = default_domain

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
