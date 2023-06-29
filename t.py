t = """
Median employee tenure ‧
 6.3 years
"""

import re

match = re.search(r".*(\d+\.\d+).*", t)
print(match.group(1))
