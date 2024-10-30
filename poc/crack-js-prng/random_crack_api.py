import z3
import struct
import math

# NOTE: random cache size is 64 and it is read out LIFO. Therefore, output random numbers aren't all contiguous, with a cache refill every 64 numbers
# If you have a range of generated numbers of length k, then you have a k/64 probability of the predictor failing
  
def xorshift(s0: int, s1: int):
# XORshift128+ algorithm
  se_s1 = s0
  se_s0 = s1
  s0 = se_s0
  se_s1 ^= (se_s1 << 23) % (1 << 64)
  se_s1 ^= ((se_s1 % (1 << 64)) >> 17) # Logical shift instead of Arthmetric shift
  se_s1 ^= se_s0
  se_s1 ^= ((se_s0 % (1 << 64)) >> 26)
  s1 = se_s1

  return s0, s1

class Predictor:
  def __init__(self):
    self._input_type = ""
    self._state_0, self._state_1 = z3.BitVecs("_state_0 _state_1", 64)
    self._solver = z3.Solver()
    self._states = {}
  
  def _advance_xorshift(self):
  # internal representation of xorshift state
    se_s1 = self._state_0
    se_s0 = self._state_1
    self._state_0 = se_s0
    se_s1 ^= se_s1 << 23
    se_s1 ^= z3.LShR(se_s1, 17)
    se_s1 ^= se_s0
    se_s1 ^= z3.LShR(se_s0, 26)
    self._state_1 = se_s1

  def feed_mantissas(self, mantissas: list[int]):
  # feed mantissa values (52-bit unsigneds) to z3 solver
    for mantissa in mantissas[::-1]:
      self._advance_xorshift()
      self._solver.add(int(mantissa) == z3.LShR(self._state_0, 12))

  def feed_raw_doubles(self, doubles: list[float]):
  # feed Math.random() double outputs to z3 solver
    mantissas = []
    for doub in doubles:
      float_64 = struct.pack("d", doub + 1)

      u_long_long_64 = struct.unpack("<Q", float_64)[0]

      mantissa = u_long_long_64 & ((1 << 52) - 1)

      mantissas.append(mantissa)
    self.feed_mantissas(mantissas)

  def feed_mantissa_bounds(self, bounds: list[tuple[int,int]]):
  # feed (lower,upper) bound pairs on the mantissa to z3 solver. all bounds are unsigned 52-bit integers
    for bound in bounds[::-1]:
      self._advance_xorshift()
      mantissa_low, mantissa_high = bound
      self._solver.add(z3.LShR(self._state_0,12) >= mantissa_low)
      self._solver.add(z3.LShR(self._state_0,12) <= mantissa_high)

  def feed_scaled_floors(self, nums: list[int], N: int):
  # feed numbers (ints) of the form Math.floor(Math.random()*N) to the solver
    bounds = []
    for num in nums:
      low_bound = (num) / N
      high_bound = (num + 1) / N

      float_64_low = struct.pack("d", low_bound + 1)
      float_64_high = struct.pack("d", high_bound + 1)

      u_long_long_64_low = struct.unpack("<Q", float_64_low)[0]
      u_long_long_64_high = struct.unpack("<Q", float_64_high)[0]

      mantissa_low = (u_long_long_64_low & ((1 << 52) - 1)) - 1
      mantissa_high = (u_long_long_64_high & ((1 << 52) - 1)) + 1

      bounds.append((mantissa_low,mantissa_high))
    self.feed_mantissa_bounds(bounds)

  def check_sat(self) -> bool:
  # determine if model is satisfiable
    return self._solver.check() == z3.sat
  
  def _model(self):
  # internal method to solve the internal model
    model = self._solver.model()
    self._states = {}
    for state in model.decls():
      self._states[state.__str__()] = model[state]

  def predict_next_mantissa(self) -> int:
  # predict the next mantissa outputted by Math.random()
    self._model()

    state0 = self._states["_state_0"].as_long()
    return (state0 >> 12)    

  def predict_next_double(self) -> float:
  # predict the next double outputted by Math.random()
    mantissa = self.predict_next_mantissa()

    u_long_long_64 = mantissa | 0x3FF0000000000000

    float_64 = struct.pack("<Q", u_long_long_64)
    next_double = struct.unpack("d", float_64)[0]

    next_double -= 1

    return next_double

  def predict_next_scaled_floor(self, N: int) -> int:
  # predict the next member of the sequence Math.floor(Math.random() * N)
    next_double = self.predict_next_double()

    return math.floor(next_double * N)
  
  def get_states(self):
  # return computed initial states if SAT
    return (self._states["_state_0"], self._states["_state_1"])