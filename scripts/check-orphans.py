#!/usr/bin/env python3
import csv, glob, os

# Get all available slugs from content files
slugs = {os.path.basename(p).replace('.md','') for p in glob.glob('seo-portfolio/src/content/blog/**/*.md', recursive=True)}

print(f'Available slugs: {len(slugs)}')
print('Slugs:', sorted(slugs))

# Check link_map.csv for missing targets
missing = []
with open('link_map.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Check if target_slug exists in available slugs
        target = row.get('target_slug', '').strip()
        if target and target not in slugs:
            missing.append(target)

print(f'\nMissing targets: {len(missing)}')
if missing:
    print('Missing slugs:', missing)
else:
    print('✅ No orphan links found!')

# Also check for any links in the content that might be broken
print('\nChecking for broken internal links in content...')
broken_links = []
for md_file in glob.glob('seo-portfolio/src/content/blog/**/*.md', recursive=True):
    with open(md_file, 'r') as f:
        content = f.read()
        # Look for markdown links
        import re
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for link_text, link_url in links:
            if link_url.startswith('/blog/'):
                slug = link_url.replace('/blog/', '').strip()
                if slug not in slugs:
                    broken_links.append(f'{os.path.basename(md_file)}: {link_text} -> {link_url}')

if broken_links:
    print(f'Found {len(broken_links)} broken internal links:')
    for link in broken_links:
        print(f'  - {link}')
else:
    print('✅ No broken internal links found!')
