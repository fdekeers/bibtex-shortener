#!/usr/bin/python3

"""
Shorten a bibtex file by replacing author lists of more than 3 authors with \"et al.\"
"""

import os
from pathlib import Path
import argparse
import bibtexparser


### GLOBAL VARIABLES ###
script_name = os.path.basename(__file__)
script_path = Path(os.path.abspath(__file__))
removable_fields = ["pages", "address"]


### MAIN ###
if __name__ == "__main__":

    ## ARGUMENT PARSING ##
    parser = argparse.ArgumentParser(
        description="Shorten a bibtex file by replacing author lists of more than 3 authors with \"et al.\"",
        prog=script_name
    )
    # Positional argument: path to the input bibtex file
    parser.add_argument("input", help="Path to the input bibtex file")
    # Parse arguments
    args = parser.parse_args()

    # Output file
    output_path = args.input.replace(".bib", "_short.bib")


    ## BIBTEX FILE LOGIC ##
    with open(args.input, "r") as bibfile:
        bib_db = bibtexparser.load(bibfile)

        for entry in bib_db.entries:

            # Remove unnecessary fields
            for field in removable_fields:
                if field in entry:
                    del entry[field]

            # Remove unnecessary notes for entries other than `misc`
            entry_type = entry.get("ENTRYTYPE", "misc")
            if entry_type != "misc" and "note" in entry:
                del entry["note"]

            # Shorten author list
            authors = entry.get("author", "")
            n_authors = authors.count(",")
            if n_authors > 2:
                i = authors.find(" and")
                new_authors = authors[:i] if i != -1 else authors
                spl = new_authors.split(", ")
                spl[0] = f"{spl[0]} \\textit{{et al.}}"
                new_authors = f"{spl[0]}, {spl[1]}"
                entry["author"] = new_authors
        
        # Write output bibtex file
        with open(output_path, "w") as output:
            bibtexparser.dump(bib_db, output)
