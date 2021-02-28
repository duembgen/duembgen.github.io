#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_bib_file.py: Convert raw bibtex file to yml format and md pages. 
"""

import os
import yaml

import bibtexparser as bb


def get_link(entry):
    if 'url' in entry.keys():
        return entry['url']
    elif 'doi' in entry.keys():
        return f"https://doi.org/{entry['doi']}"
    else:
        print('Warning: no link in', entry['ID'])
        return ''


def get_journal(entry):
    if entry.get('ENTRYTYPE') == 'article':
        return entry.get('journal')
    elif entry.get('ENTRYTYPE') == 'inproceedings':
        return entry.get('booktitle')
    else:
        print('Warning: unknown entry type in', entry)
        return ''


def clean(list_of_string):
    replace = [
        ['\\"{u}}', 'ü'],
        ['{', ''],
        ['}', ''],
    ]
    if not isinstance(list_of_string, list):
        list_of_string = [list_of_string]

    clean_list = []
    for a in list_of_string:
        for r in replace:
            a = a.replace(*r)
        clean_list.append(a)
    return clean_list


def check_for_overwrite(fname):
    answer = ""
    if os.path.exists(fname): 
        while answer not in ["y", "n"]: 
            answer = input(f"{fname} exists, overwrite? (y/[n])") or "n"
    if answer == "n":
        return False
    return True


if __name__ == "__main__":
    import sys 

    in_name_bib = "_data/mendeley-export.bib"
    out_name_data = "_data/mendeley-export.yml"
    out_folder_pages = "_publications"

    with open(in_name_bib, 'r') as f:
        bib_db = bb.load(f)

    general_dict = {
        'layout': 'publication',
        'ref-code': '',
        'ref-link': '',
        'ref-video': ''
    }

    categories = {'inproceedings': 'Conference', 'article': 'Journal'}

    all_dicts = []
    for entry in bib_db.entries:
        author_tuples = [a.split(', ') for a in entry['author'].split(' and ')]
        author_names = [f"{a[1].strip()[0]}. {a[0]}" for a in author_tuples]
        author_names = clean(author_names)

        dict_to_write = {}
        dict_to_write['ref-authors'] = author_names
        dict_to_write['title'] = clean(entry['title'])[0]
        dict_to_write['ref-year'] = int(entry['year'])
        dict_to_write['ref-journal'] = get_journal(entry)
        dict_to_write['ref-link'] = get_link(entry)
        dict_to_write['categories'] = categories.get(entry['ENTRYTYPE'],
                                                     'Other')

        all_dicts.append(dict_to_write)

        fname = os.path.join(out_folder_pages, entry['ID'] + '.md')

        if not check_for_overwrite(fname):
            continue

        with open(fname, 'w') as f:
            f.write('---\n')
            f.write('layout: publication\n')
            f.write(yaml.dump(dict_to_write))
            f.write('---\n\n\n')
            f.write(entry.get('abstract', ''))
            f.write('\n')
        print('wrote', fname)


    if not check_for_overwrite(out_name_data):
        sys.exit(0) # successful termination

    with open(out_name_data, 'w') as f:
        f.write(yaml.dump(all_dicts))
    print('wrote', out_name_data)
