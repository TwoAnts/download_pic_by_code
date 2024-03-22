#!/usr/bin/env python3

import sys
import re

CODE_PATTERN = re.compile(r'\D')

if __name__ == '__main__':
    code_set = set()
    with open(sys.argv[1], "r", encoding='UTF-8') as f:
        lineno = 0
        for line in f:
            lineno += 1
            line = line.strip()
            line = CODE_PATTERN.sub("", line)
            if len(line) < 8 or len(line) > 12:
                print("ignore %d %s" %(lineno, line))
                continue
            if line in code_set:
                print("%d %s already exists" %(lineno, line))
                continue
            print("%d %s" %(lineno, line))
            code_set.add(line)
    
    with open(sys.argv[2], "w", encoding='UTF-8') as of:
        of.writelines((code + '\n' for code in code_set))