"""JSON Translation script for deeply nested structures."""
import argparse
import json
import re
import subprocess
import sys

# 1. Install deep-translator if not present
try:
    from deep_translator import GoogleTranslator
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "deep-translator"])
    from deep_translator import GoogleTranslator

def translate_text(text, translator):
    """Translates plain text, ignoring purely numeric/symbolic text."""
    if not text or not isinstance(text, str) or not text.strip():
        return text
    try:
        # Avoid translating pure numbers, punctuation or IDs
        if re.match(r'^[0-9\s.,:\-_()]+$', text):
            return text
        return translator.translate(text)
    except Exception:  # pylint: disable=broad-exception-caught
        return text

def translate_html(html_str, translator):
    """Translates HTML text content while preserving the HTML tags."""
    if not html_str or not isinstance(html_str, str):
        return html_str

    parts = re.split(r'(<[^>]+>)', html_str)
    new_parts = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            new_parts.append(part)
        elif part.strip():
            leading = part[:len(part) - len(part.lstrip())]
            trailing = part[len(part.rstrip()):]
            translated = translate_text(part.strip(), translator)
            new_parts.append(f"{leading}{translated}{trailing}")
        else:
            new_parts.append(part)
    return "".join(new_parts)

class TranslationJob:
    """Class to track translation progress and recurse through JSON."""
    def __init__(self, data, translator):
        self.current_translation = 0
        self.translator = translator
        self.total_translations = self.count_translations(data)

    def count_translations(self, node):
        """Recursively count how many text elements need to be translated."""
        count = 0
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ('label', 'html') and isinstance(v, str):
                    count += 1
                else:
                    count += self.count_translations(v)
        elif isinstance(node, list):
            for item in node:
                count += self.count_translations(item)
        return count

    def _update_progress(self):
        """Internal method to update the counter and display progress."""
        self.current_translation += 1
        if self.total_translations > 0:
            percent = (self.current_translation / self.total_translations) * 100
            msg = f"\rProgress: {self.current_translation}/{self.total_translations}"
            print(f"{msg} ({percent:.1f}%)", end="", flush=True)

    def recurse_json(self, node):
        """Recursively traverse and translate dicts and lists."""
        if isinstance(node, dict):
            new_dict = {}
            for k, v in node.items():
                if k == 'label' and isinstance(v, str):
                    new_dict[k] = translate_text(v, self.translator)
                    self._update_progress()
                elif k == 'html' and isinstance(v, str):
                    new_dict[k] = translate_html(v, self.translator)
                    self._update_progress()
                else:
                    new_dict[k] = self.recurse_json(v)
            return new_dict

        if isinstance(node, list):
            return [self.recurse_json(item) for item in node]

        return node

def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Translate deeply nested JSON files.")
    parser.add_argument('--lang', '--l', type=str,
                        help="Target language code (e.g., 'de', 'fr')")
    parser.add_argument('--input', '--in', type=str, default=None,
                        help="Input JSON file path - .json file extension is optional")
    parser.add_argument('--output', '--out', type=str, default=None, help="Output JSON file path - optional, will default to input_lang.json if not provided")
    args = parser.parse_args()

    if not args.lang or not args.input:
        print("Error: Missing mandatory arguments. Please provide both --lang and --input.\n")
        parser.print_help()
        sys.exit(1)

    input_path = args.input
    if input_path and not input_path.lower().endswith('.json'):
        input_path += '.json'

    output_path = args.output
    if output_path and not output_path.lower().endswith('.json'):
        output_path += '.json'

    if not output_path and input_path:
        # Automatically generate output path based on the target language if not specified
        output_path = input_path[:-5] + f"_{args.lang}.json"

    # 2. Read the actual uploaded file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' was not found.")
        sys.exit(1)

    translator = GoogleTranslator(source='en', target=args.lang.lower())

    # Pre-calculate the total number of translation tasks
    job = TranslationJob(data, translator)
    print(f"Found {job.total_translations} items to translate to '{args.lang}'.")

    # 3. Translate
    translated_data = job.recurse_json(data)
    print()  # Add a newline after the progress bar finishes

    # 4. Save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print("SUCCESS: Full translation completed and saved to", output_path)

if __name__ == '__main__':
    main()
