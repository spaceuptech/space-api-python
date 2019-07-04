from space_api.utils import generate_find
from space_api import AND, COND, OR

condition = AND(COND('a', '>=', 1), COND('a', '<=', 10))
print(generate_find(condition))
