import os
import re
import os.path

SUFFIX_RE = re.compile(r"\-\d+$")

for file_name in os.listdir("."):
    base, ext = os.path.splitext(file_name)
    fixed_base = SUFFIX_RE.sub("", base, 1).replace("x265", "x264")
    fixed_file_name = fixed_base + ext
    print(fixed_file_name)
    os.rename(file_name, fixed_file_name)
