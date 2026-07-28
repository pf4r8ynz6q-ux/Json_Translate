# JSON Language Translator

A Python script designed to automatically translate text within deeply nested JSON structures. It is specifically tailored to find and translate values associated with `label` and `html` keys, making it ideal for localizing UI configurations, structured content, or web components. By default, it translates from English to a target language, but it can be configured to translate from any language to any language.

## Features

*   **Deep Recursion**: Traverses through complex, deeply nested dictionaries and lists within your JSON file.
*   **Targeted Translation**: Only translates strings found under the keys `label` and `html`.
*   **HTML Preservation**: Safely translates text inside `html` fields without breaking or translating the HTML tags.
*   **Smart Skipping**: Ignores purely numeric, symbolic, or punctuation-only strings to save time and API requests.
*   **Progress Tracking**: Displays a real-time progress bar counting the exact number of translated items.
*   **Auto-Installation**: Automatically installs the required `deep-translator` package if it's missing from your environment.

## Prerequisites

*   Python 3.x

## Usage

Run the script from the command line, providing the target language and input file.

```bash
python json_lang_translate.py --lang <target_language> --input <input_file> [--in_lang <source_language>] [--output <output_file>]
```

### Arguments

*   `--lang` / `--l` *(Required)*: The target language code (e.g., `de` for German, `fr` for French, `es` for Spanish).
*   `--input` / `--in` *(Required)*: The path to your input JSON file. The `.json` extension is optional and will be appended if missing. The assumed input language is English.
*   `--in_lang` / `-in_l` *(Optional)*: The source language code. Defaults to `en` unless specified. Allows for translation both to and from other Languages.
*   `--output` / `--out` *(Optional)*: The path for the translated output file. If omitted, the script automatically generates a name based on the input file and target language (e.g., `data.json` translated to French becomes `data_fr.json`).

### Examples

**1. Basic Usage (Auto-generated output file)**
Translate `data.json` to Spanish (`es`). This will automatically create `data_es.json` in the same directory.
```bash
python json_lang_translate.py --lang es --input data.json
```

**2. Specify an Output File**
Translate `config.json` to German (`de`) and save it to a specific path.
```bash
python json_lang_translate.py --lang de --input config.json --output ./locales/config_german.json
```

## Dependencies
*   `deep-translator` (installed automatically upon first run if not found).
