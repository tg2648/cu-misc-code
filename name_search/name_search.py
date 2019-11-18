"""
"""

# Standard library imports
# import os

# Third party imports
# from dotenv import load_dotenv


with open('name-search/paths.csv', encoding='utf-8') as f_paths:
    paths = [line.rstrip() for line in f_paths]

with open('name-search/names.csv', encoding='utf-8') as f_names:
    next(f_names, None)  # Skip the header
    names = [line.rstrip() for line in f_names]

headers = ','.join(['Person_ID', 'Name', 'Path Match on Full Name Count', 'Path Match on Last Name Count', 'All Drafts', 'All Full Name Matches', 'All Last Name Matches', '\n'])

with open('name-search/output.csv', 'w', encoding='utf-8') as f_out:
    f_out.writelines(headers)
    for name in names:
        person_id, full_name = name.split(',')
        name_components = full_name.split(' ')
        first_name, last_name = name_components[0], name_components[1]

        options = [
            f"{last_name},{first_name}",
            f"{last_name}, {first_name}",
            f"{last_name} {first_name}",
        ]
        matches_full_name = []
        matches_last_name = []

        for path in paths:
            loc = path.find(last_name)
            if (loc != -1) and (path not in matches_last_name):
                matches_last_name.append(path)

            for option in options:
                loc = path.find(option)
                if (loc != -1) and (path not in matches_full_name):
                    matches_full_name.append(path)

        # Check if all matches are drafts
        logical = [match.find('draft') != -1 for match in matches_full_name]
        if len(logical) > 0:
            all_draft = all(logical)
        else:
            all_draft = False

        output = [
            person_id,
            full_name,
            str(len(matches_full_name)),
            str(len(matches_last_name)),
            str(all_draft),
            f"\"{str(matches_full_name)}\"",
            f"\"{str(matches_last_name)}\"",
            '\n'
        ]

        f_out.writelines(','.join(output))
