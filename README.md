PEP257fier
==========

A script to fix pep257 issues automatically.

It fixes D200, D202, D203, D204, D209 and some parts of D400.
Copy fixer257.py into the folder you want to fix, run this command:
   pep257 *.py -s --ignore=D100,D102,D101,D205,D103 > allout.txt 2>&1
and then run the file:
   python fixer257.py
Check what the script has done (by git diff) before anything.
