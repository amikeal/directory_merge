merge.py
===============

A simple script to merge two directories, eliminating duplicate
files, and renaming files with the same name but different content.

Usage
-----

```python merge.py [options]```

Options
-------
```
  -h, --help    Show this help file
  -k, --keep    The directory to keep
  -c, --clean   The directory to clean
  -v            Run verbosely
```

Example
-------
```merge.py --keep a --clean b```

After execution, `a` will contain at least all its original files, 
plus any files from `b` which did not appear in `a` beforehand.
`b` will be empty, all its files having been moved or deleted.
