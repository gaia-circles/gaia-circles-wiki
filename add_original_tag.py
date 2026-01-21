#!/usr/bin/env python3
"""
Script to add #PageFromTheOriginal tag to all markdown files.
"""

import os
import sys

def process_file(filepath, test_mode=False):
    """Process a single markdown file to add the tag."""

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if already tagged
    content = ''.join(lines)
    if '#PageFromTheOriginal' in content:
        if test_mode:
            print(f"SKIP (already tagged): {filepath}")
        return False

    # Find the first header line (starts with "# ")
    header_index = None
    for i, line in enumerate(lines):
        if line.startswith('# '):
            header_index = i
            break

    # Prepare the insertion
    tag_lines = [
        '\n',
        ' #PageFromTheOriginal\n',
        '\n',
        'This is a [[Page From The Original]].\n',
        '\n'
    ]

    # Insert after header or at the beginning
    if header_index is not None:
        # Insert after the header
        insert_position = header_index + 1
        new_lines = lines[:insert_position] + tag_lines + lines[insert_position:]
    else:
        # No header found, insert at the beginning
        new_lines = tag_lines + lines

    if test_mode:
        print(f"\n{'='*60}")
        print(f"FILE: {filepath}")
        print(f"{'='*60}")
        print("\nBEFORE:")
        print(''.join(lines[:10]))  # Show first 10 lines
        print("\nAFTER:")
        print(''.join(new_lines[:15]))  # Show first 15 lines
        print(f"{'='*60}\n")
        return True
    else:
        # Write the modified content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True

def main():
    test_mode = len(sys.argv) > 1 and sys.argv[1] == '--test'
    limit = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])

    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk('.'):
        # Skip .obsidian directory
        if '.obsidian' in root:
            continue

        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                md_files.append(filepath)

    if test_mode:
        # Test on first 3 files
        print(f"TEST MODE: Processing first 3 files out of {len(md_files)} total\n")
        for filepath in md_files[:3]:
            process_file(filepath, test_mode=True)
    else:
        # Process files (all or limited)
        files_to_process = md_files[:limit] if limit else md_files
        processed = 0
        skipped = 0

        for filepath in files_to_process:
            if process_file(filepath, test_mode=False):
                processed += 1
                print(f"Processed: {filepath}")
            else:
                skipped += 1

        print(f"\nProcessed: {processed} files")
        print(f"Skipped: {skipped} files (already tagged)")
        print(f"Total: {len(md_files)} files")

if __name__ == '__main__':
    main()
