import os
import logging
import argparse

logging.basicConfig(level=logging.INFO)

def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logging.warning(f"File {filename} not found.")
        return ""

def embed_content(html_content, tag, content):
    if tag == 'style':
        return html_content.replace('</head>', f'<style>{content}</style></head>')
    elif tag == 'script':
        return html_content.replace('</body>', f'<script>{content}</script></body>')
    return html_content

def main():
    parser = argparse.ArgumentParser(description="Embed CSS and JS into HTML.")
    parser.add_argument('--output', '-o', default='combined.html', help='Output filename')
    args = parser.parse_args()

    html_files = [f for f in os.listdir() if f.endswith('.html')]
    css_files = [f for f in os.listdir() if f.endswith('.css')]
    js_files = [f for f in os.listdir() if f.endswith('.js')]

    if not html_files:
        logging.error("No HTML file found. Exiting.")
        return

    html_content = "".join([read_file(f) for f in html_files])
    css_content = "".join([read_file(f) for f in css_files])
    js_content = "".join([read_file(f) for f in js_files])

    if css_content:
        html_content = embed_content(html_content, 'style', css_content)
    else:
        logging.info("No CSS content to embed.")

    if js_content:
        html_content = embed_content(html_content, 'script', js_content)
    else:
        logging.info("No JS content to embed.")

    with open(args.output, 'w') as f:
        f.write(html_content)

    logging.info(f"Combined content written to {args.output}")

if __name__ == '__main__':
    main()
