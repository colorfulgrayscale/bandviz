from collections import deque

LIMIT = 10000000

q = deque()
for i in xrange(LIMIT):
  q.appendleft(i)
while len(q):
  q.pop()