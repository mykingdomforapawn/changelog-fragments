import os
import datetime
import argparse

# Configuration.
FRAGMENT_DIR = ".changelog/unreleased"
CHANGELOG_FILE = "CHANGELOG.md"

# Map file extensions to Section Headers.
TYPE_MAPPING = {
    "feature": "### Features",
    "bugfix": "### Bug Fixes",
    "breaking": "### Breaking Changes",
    "docs": "### Documentation",
    "chore": "### Chores",
}

def get_fragments():
    fragments = {}
    if not os.path.exists(FRAGMENT_DIR):
        return fragments

    for filename in os.listdir(FRAGMENT_DIR):
        if filename.startswith('.'): continue

        # Parse filename: name.type.md.
        parts = filename.split('.')
        if len(parts) < 3 or parts[-1] != 'md':
            print(f"Skipping malformed file: {filename}")
            continue

        category = parts[-2]
        content = open(os.path.join(FRAGMENT_DIR, filename)).read().strip()

        if category not in fragments:
            fragments[category] = []
        fragments[category].append(content)

    return fragments

def generate_release_text(version, fragments):
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    lines = [f"## {version} ({date_str})", ""]

    # Sort categories to ensure consistent order.
    for category, header in TYPE_MAPPING.items():
        if category in fragments:
            lines.append(header)
            for item in fragments[category]:
                lines.append(f"- {item}")
            lines.append("")

    return "\n".join(lines)

def update_changelog(new_content):
    current_content = ""
    if os.path.exists(CHANGELOG_FILE):
        current_content = open(CHANGELOG_FILE).read()

    # Prepend new content.
    with open(CHANGELOG_FILE, 'w') as f:
        f.write(new_content + "\n" + current_content)

def cleanup_fragments():
    for filename in os.listdir(FRAGMENT_DIR):
        if filename.endswith(".md"):
            os.remove(os.path.join(FRAGMENT_DIR, filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="The version number (e.g., v1.0.0).")
    args = parser.parse_args()

    fragments = get_fragments()
    if not fragments:
        print("No fragments found. Skipping release generation.")
        exit(0)

    new_section = generate_release_text(args.version, fragments)
    print(f"Generating release notes for {args.version}...")

    update_changelog(new_section)
    cleanup_fragments()

    # Save the release body to a temp file for GitHub Actions to read.
    with open("release_body.txt", "w") as f:
        f.write(new_section)
