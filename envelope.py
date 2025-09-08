class Envelope:
    def __init__(self, value: int, next_envelope=None):
        self._value = value
        self._next = next_envelope
        self._kept = False
    
  def get_value():
    return self._value()

  def keep():
    self._kept =True
    return self._value()

  def toss_and_get_next():
    return self._next()
  
    
