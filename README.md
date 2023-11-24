# 🤖 OpenAI instant assistant

## Description

Generate an OpenAI assistant with Retrieval Augmented Generation on your directories!

## Installation

```bash
pip install git+https://github.com/davidgonmar/openai_instant_assistant@main
```

## Usage

First, you must set your OpenAI API key as an environment variable.

```bash
# Windows
set OPENAI_API_KEY=<your-api-key>
# Linux / Mac
export OPENAI_API_KEY=<your-api-key>
```

You can use the command 'create-assistant' to generate an assistant on a directory.
It will upload all files with supported types to OpenAI in said directory, and create the assistant in your OpenAI account.

```bash
create-assistant <directory> [--name <name>] [--instructions <instructions>]
```

- **directory**: Directory where to get the files from.
- **name**: Name of the assistant. Default: 'My assistant'.
- **instructions**: Instructions to generate the assistant. Default: ''.

## File limitations

OpenAI only supports certain file types. Moreover, files cannot exceed 512MB and there is a maximum of 20 files per assistant. Non-supported files or files that exceed the size limit will be ignored. The supported file types are:

- **.c**
- **.cpp**
- **.docx**
- **.html**
- **.java**
- **.json**
- **.md**
- **.pdf**
- **.php**
- **.pptx**
- **.py**
- **.rb**
- **.tex**
- **.txt**

## Development

Poetry is used to manage dependencies and virtual environments. Linting and formatting is done with Ruff and Black.

```bash
# Install dependencies
poetry install

# Run linter and formatter
poetry run ruff check .
poetry run black .

# Run tests
poetry run pytest
```

## 📝 License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.
