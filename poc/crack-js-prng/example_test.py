import random_crack_api as rc
from data import numberlist
import re
import ast
import json
import itertools

N = 1000000000
i = 10
start = 0

bodies = []

with open('response.txt','r') as f:
  stream = False
  body = False
  body_info = {}
  stream_id = -1
  stream_pattern = r"#- *Stream ID: (\d+) *-#"
  for line in f:
    m = re.search(stream_pattern,line.strip())
    if m:
      stream = True
      stream_id = int(m.group(1))
    else:
      if stream:
        if line.strip() == "-Body-":
          body = True
        else:
          if body:
            body_info = json.loads(ast.literal_eval(line.strip()))
            bodies.append((body_info["seq"],body_info["correctNumber"]))
            stream = False
          body = False

#bodies.sort()

print(bodies)

print(sorted(bodies))

for perm in itertools.permutations(bodies):


  input_data = []

  for i in range(1,7):
    input_data.append(perm[i][1] - 1)

  next_value = perm[7][1] - 1

  #print(input_data)

  P = rc.Predictor()

  P.feed_scaled_floors(input_data,N)
  #P.feed_raw_doubles(input_data)
  if (P.check_sat()):
    print("SAT")
    print(P.predict_next_scaled_floor(N))
    #print(P.predict_next_double())
    print(f"True value: {next_value}")
    print(input_data)
    print(next_value)
    print(perm)
    exit(0)
  else:
    continue