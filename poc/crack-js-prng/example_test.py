import random_crack_api as rc
from data import numberlist

N = 10000
i = 20
start = 0
input_data = numberlist[start:start+i]
next_value = numberlist[start+i]

print(input_data)

P = rc.Predictor()

P.feed_scaled_floors(input_data,N)
#P.feed_raw_doubles(input_data)
if (P.check_sat()):
  print("SAT")
  print(P.predict_next_scaled_floor(N))
  #print(P.predict_next_double())
  print(f"True value: {next_value}")
else:
  print("UNSAT")