"""Script to create an OpenAI assistant with RAG on a directory of files"""

import argparse
import os
from typing import List
from pathlib import Path
import logging
import openai


def get_file_paths(
    directory: str,
    extensions: List[str],
    max_number_files: int,
    max_file_size: int,
) -> List[str]:
    """Returns files in a directory with the specified options.

    Recursively walks through the directory and returns a list of file paths
    that do not exceed the maximum number of files or the maximum file size.
    Skip files that are not of the specified extensions or are larger than the
    maximum file size.

    Args:
        directory: The directory to walk through
        extensions: The file extensions to include
        max_number_files: The maximum number of files to include
        max_file_size: The maximum file size in bytes

    Returns:
        A list of file paths relative to the directory
    """

    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            path_from_root = os.path.join(root, file)
            if len(file_paths) >= max_number_files:
                logging.warning(
                    f"Skipping {path_from_root} because the maximum number of files has been reached.\n"
                )
                return file_paths

            if os.path.splitext(file)[1] in extensions:
                file_size = os.path.getsize(os.path.join(root, file))
                if file_size > max_file_size:
                    file_size_mb = file_size / 1024 / 1024
                    logging.warning(
                        f"Skipping {path_from_root} because it is {file_size_mb}MB, which is larger than 512MB.\n"
                    )
                else:
                    file_paths.append(path_from_root)
            else:
                logging.warning(
                    f"Skipping {path_from_root} because it is not a supported file type.\n"
                )
    return file_paths


def upload_files(file_paths: List[str]) -> List[str]:
    """Uploads each file to OpenAI and returns a list of the file IDs

    Args:
        file_paths: The file paths to upload

    Returns:
        A list of the file IDs
    """

    openai_file_ids = []
    for file_path in file_paths:
        try:
            # Use path since it is the only way to preserve the file name for the upload currently
            response = openai.files.create(file=Path(file_path), purpose="assistants")
            openai_file_ids.append(response.id)
            logging.info(f"Uploaded {file_path}.\n")
        except openai.APIStatusError as e:
            logging.error(f"Error uploading {file_path}: {e.message}. Skipping...\n")
    return openai_file_ids


def create_assistant(name: str, instructions: str, file_ids: List[str]) -> str:
    """Creates an OpenAI assistant and returns the assistant ID

    Args:
        name: The name of the assistant
        instructions: The instructions for the assistant
        file_ids: The file IDs to use for the assistant

    Returns:
        The assistant ID
    """

    assistant = openai.beta.assistants.create(
        instructions="Assist me!",
        name=name,
        model="gpt-3.5-turbo-1106",
        tools=[{"type": "retrieval"}],
        file_ids=file_ids,
    )
    return assistant.id


def build_assistant_url(
    assistant_id: str,
) -> str:
    """Builds the url to access the assistant

    Args:
        assistant_id: The assistant ID

    Returns:
        The url to access the assistant
    """

    return f"https://platform.openai.com/playground?mode=assistant&assistant={assistant_id}"


def main():
    """Main function"""

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # OpenAI only supports these extensions for Retrieval Augmented Generation
    ACCEPTED_EXTENSIONS = [
        ".c",
        ".cpp",
        ".docx",
        ".html",
        ".java",
        ".json",
        ".md",
        ".pdf",
        ".php",
        ".pptx",
        ".py",
        ".rb",
        "tex",
        ".txt",
    ]

    # OpenAI only supports 20 files per assistant
    MAX_FILES = 20

    # OpenAI only allows files under 512MB
    MAX_FILE_SIZE = 512 * 1024 * 1024

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    assert OPENAI_API_KEY, "Please set OPENAI_API_KEY environment variable!"

    parser = argparse.ArgumentParser(
        description="Generate an OpenAI assistant with RAG on a directory"
    )

    parser.add_argument("dir")
    parser.add_argument("--name", default="My assistant")
    parser.add_argument("--instructions", default="")

    args = parser.parse_args()

    # Check that dir is a correct path
    if not os.path.isdir(args.dir):
        raise NotADirectoryError(f"{args.dir} is not a directory")

    file_paths = get_file_paths(args.dir, ACCEPTED_EXTENSIONS, MAX_FILES, MAX_FILE_SIZE)

    logging.info(f"Found {len(file_paths)} files. Uploading to OpenAI...\n")

    openai_file_ids = upload_files(file_paths)

    assistant_id = create_assistant(args.name, args.instructions, openai_file_ids)

    logging.warning(f"Assistant created with ID {assistant_id}")
    logging.info(f"Assistant URL: {build_assistant_url(assistant_id)}")


if __name__ == "__main__":
    main()
