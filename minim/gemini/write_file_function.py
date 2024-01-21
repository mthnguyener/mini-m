#! /usr/bin/env python3
# -*- coding: utf-8 -*-
""" Gemini Write File Function Module

"""
import os

from minim.pkg_globals import PACKAGE_ROOT


definitions = [
    {
        "name": "write_file",
        "description": "Writes to a file",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "filename": {
                    "type": "STRING",
                    "description": "Filename"
                },
                "content": {
                    "type": "STRING",
                    "description": "Content to write"
                }
            },
            "required": ["filename"]
        }
    }
]


def parse_content(content: str):
    """Parse the content

    :param content: Content to parse
    """
    content = content.replace("\\n", "|n|")
    content = content.replace("\\'", "\'")
    content = content.replace("\\\"", "\"")
    content = content.replace("|n|", "\n")
    return content


def write_file(content: str, filename: str):
    """Write content to a file

    :param content: Content used to write to file
    :param filename: Filename to write to
    """
    content = parse_content(content)
    confirmation = input(f"\nmini-M: Should I proceed with writing to "
                         f"{filename}? (YES/NO) ")
    if confirmation.lower() == "yes" or confirmation.lower() == "y":
        dirname = PACKAGE_ROOT / "data/minim" / os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(dirname / filename, "w") as f:
            f.write(content)
        return {f'status: Wrote to {filename} successfully!'}
    else:
        return {f'status: ERROR writing to file: {filename}...'}


if __name__ == "__main__":
    pass
