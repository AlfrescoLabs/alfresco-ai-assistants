"""\
This script aggregates the content of Markdown files from the 'latest' subdirectories
of all directories in the root directory. It then writes the aggregated content to
new Markdown files in a 'target' directory.
Used to aggregate the contents of the docs-alfresco GitHub repository.
"""

import os
import glob

# Set the root directory
root_dir = '.'

# Iterate over all directories in the root directory
for dir_name in os.listdir(root_dir):
    if dir_name.startswith('_') or dir_name.startswith('.'):
        continue
    
    dir_path = os.path.join(root_dir, dir_name)
    
    # Check if it's a directory
    if os.path.isdir(dir_path):
        docs_content = ''
        # Check if it has a 'latest' subdirectory
        latest_dir_path = os.path.join(dir_path, 'latest')
        if os.path.isdir(latest_dir_path):
            # Use glob to find all Markdown files in the 'latest' directory
            md_files = glob.glob(f'{latest_dir_path}/**/*.md', recursive=True)
            
            # Aggregate the Markdown files
            for md_file in md_files:
                with open(md_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    docs_content += content

            # Write the aggregated content to a new file
            if not os.path.exists('target'):
                os.makedirs('target')
            with open(os.path.join('target', f'{dir_name}.md'), 'w', encoding='utf-8') as file:
                file.write(docs_content)

