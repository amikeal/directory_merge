#!/usr/bin/env python
# encoding: utf-8
"""
merge.py

Created by Adam Mikeal on 2011-11-10.
Copyright (c) 2011 Adam Mikeal. All rights reserved.
"""

import sys, os, getopt, hashlib, pprint
from datetime import date, datetime


help_message = '''
A simple script to merge two directories, eliminating duplicate
files, and renaming files with the same name but different content.

Usage: python merge.py [options]

Options:
  -h, --help    Show this help file
  -k, --keep    The directory to keep
  -c, --clean   The directory to clean
  -v            Run verbosely

Example:
  merge.py --keep a --clean b

After execution, 'a' will contain at least all its original files, 
plus any files from 'b' which did not appear in 'a' beforehand.
'b' will be empty, all its files having been moved or deleted.
'''


KEEP_LIST = {}
VERBOSE = False


def log(msg):
    logit = '[%s] %s' % (datetime.now(), msg)
    print logit.encode('utf8')
    #self.LOG_FH.write(logit + "\n")


def md5_hash(filename, block_size=8192):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(block_size), ''): 
            md5.update(chunk)
    hsh = md5.hexdigest()
    if VERBOSE:
        log("Calculated MD5 hash for %s: %s" % (filename, hsh) )
    return hsh


def merge_dirs(_keep, _clean):
    _keep = os.path.realpath(_keep)
    _clean = os.path.realpath(_clean)
    log("Merging files from %s into %s! \n" % (_clean, _keep) )
    
    log("Building list of files in %s... " % _keep )
    for fname in os.listdir(_keep):
        if fname[0] != '.':
            KEEP_LIST[md5_hash(os.path.join(_keep, fname))] = fname
    log(" -- Identified %i files in %s\n" % (len(KEEP_LIST), _keep) )
    
    log("Comparing files in %s... \n" % _clean )
    count = 0
    dels = 0
    moves = 0
    for fname in os.listdir(_clean):
        if fname[0] == '.':
            continue
        count += 1
        the_file = os.path.join(_clean, fname)
        hsh = md5_hash(the_file)
        if hsh in KEEP_LIST:
            log("DELETING %s -- found in KEEP_LIST (%s)" % (fname, hsh) )
            os.remove(the_file)
            dels += 1
        else:
            log("MOVING %s -- not found in KEEP_LIST (%s)" % (fname, hsh) )
            new_path = os.path.join(_keep, fname)
            if os.path.exists(new_path):
                (name, ext) = os.path.splitext(fname)
                new_path = os.path.join(_keep, name+'_1'+ext)
                if VERBOSE:
                    log("Filename collision for '%s'; generated new path '%s'" % (fname, new_path) )
            os.rename(the_file, new_path)
            KEEP_LIST[hsh] = new_path
            moves += 1
    
    print ''
    log("Identified %i files in %s" % (count, _clean) )
    log(" -- %i DELETED" % dels)
    log(" -- %i MOVED" % moves)
    print ''
    if dels + moves != count:
        log("!!!WARNING!!! \n\n\t\tCounts do not match!")




class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    _KEEP_DIR = None
    _CLEAN_DIR = None
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hkc:v", ["help", "keep=", "clean="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                VERBOSE = True
            if option in ("-h", "--help"):
                print help_message
                sys.exit(0)
            if option == "--keep":
                _KEEP_DIR = value
            if option == "--clean":
                _CLEAN_DIR = value
        
        if os.path.isdir(_KEEP_DIR) == False:
            raise Usage("You must specify a valid directory to keep!")
        if os.path.isdir(_CLEAN_DIR) == False:
            raise Usage("You must specify a valid directory to clean!")
        
        merge_dirs(_KEEP_DIR, _CLEAN_DIR)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
