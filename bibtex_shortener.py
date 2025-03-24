#!/usr/bin/python3

"""
Shorten a bibtex file.
- Replace "online" entries by only their URL
- Remove optional fields (pages, address)
- Remove notes for entries other than `misc`
- Replace author lists of more than 3 authors with \"et al.\"
"""

import os
from pathlib import Path
import argparse
from copy import deepcopy
import bibtexparser


### GLOBAL VARIABLES ###
script_name = os.path.basename(__file__)
script_path = Path(os.path.abspath(__file__))
removable_fields = ["pages", "address"]


### MAIN ###
if __name__ == "__main__":

    ## ARGUMENT PARSING ##
    parser = argparse.ArgumentParser(
        description="Shorten a bibtex file.",
        prog=script_name
    )
    # Positional argument: path to the input bibtex file
    parser.add_argument("input", help="Path to the input bibtex file")
    # Parse arguments
    args = parser.parse_args()

    # Output file
    output_path = args.input.replace(".bib", "_short.bib")


    ### BIBTEX FILE LOGIC ###


    # Load bibtex file
    bib_db = None
    with open(args.input, "r") as bibfile:
        bib_db = bibtexparser.load(bibfile)


    # Process entries
    entries_new = []
    for entry in bib_db.entries:

        entry_new = deepcopy(entry)
        entry_type = entry_new.get("ENTRYTYPE", "misc")

        # Remove unnecessary fields
        for field in removable_fields:
            if field in entry_new:
                del entry_new[field]

        # Remove unnecessary notes for entries other than `misc`
        if entry_type != "misc" and "note" in entry_new:
            del entry_new["note"]

        # Replace "online" entries by only their URL
        if entry_type == "online":
            url = entry_new.get("url", None)
            if url is not None:
                entry_new = {"note": url}

        # Shorten author list
        authors = entry_new.get("author", "")
        n_authors = authors.count(",")
        if n_authors > 2:
            i = authors.find(" and")
            new_authors = authors[:i] if i != -1 else authors
            split = new_authors.split(", ")
            split[0] = f"{split[0]} \\textit{{et al.}}"
            new_authors = f"{split[0]}, {split[1]}"
            entry_new["author"] = new_authors
        
        # Append new entry
        entries_new.append(entry_new)
    

    # Write output bibtex file
    bib_db.entries = entries_new
    with open(output_path, "w") as output:
        bibtexparser.dump(bib_db, output)
