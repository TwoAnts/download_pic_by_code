#!/usr/bin/env python3

import sys
import re

CODE_PATTERN = re.compile(r'\D')

if __name__ == '__main__':
    code_set = set()

    with open(sys.argv[1], "r", encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            line = CODE_PATTERN.sub("", line)
            if len(line) < 8 or len(line) > 12:
                continue
            code_set.add(line)
    
    with open(sys.argv[2], "w", encoding='UTF-8') as of:
        of.writelines((code + '\n' for code in code_set))