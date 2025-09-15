import stat_math

class ExampleStrategy:
    """
    An example strategy for demonstration purposes.
    This strategy simply selects the first envelope.
    """

    def __init__(self, envelopes):
        self.envelopes = envelopes

    def display(self):
        return "Example Strategy: Always pick the first envelope."

    def play(self):
        if self.envelopes:
            chosen = self.envelopes[0]
            print(f"ExampleStrategy selected envelope with value: {chosen.get_value()}")
        else:
            print("No envelopes to choose from.")

class Automatic_strategy:
    """
    chooses a random envelope.
    """

    def __init__(self, envelopes):
        self.envelopes = envelopes

    def display(self):
        return "Automatic Strategy: Pick a random envelope."

    def play(self):
        if self.envelopes:
            i= random.randint(0, len(self.envelopes)-1)
            chosen = self.envelopes[i]
            print(f"AutomaticStrategy selected envelope with value: {chosen.get_value()}")
        else:
            print("No envelopes to choose from.")


class BestStrategy:
    """
    Take if x > mu + sd*var_{r-1}
    """

    def __init__(self, envelopes):
        self.envelopes = envelopes
        self.COLLECT_PERCENT = 0.05
    
    def display(self):
        return "BestStrategy: Take if x > mu + sd*var_{r-1}"
    
    def play(self):
        data = []
        # Collect the first <collect_percent> of envelopes as data
        current_envelope_index = 0
        for i in range(int(len(self.envelopes) * self.COLLECT_PERCENT)):
            data.append(self.envelopes[i].get_value())
            current_envelope_index = i
        while current_envelope_index < len(self.envelopes):
            current_envelope = self.envelopes[current_envelope_index]
            mu = stat_math.get_average(data)
            sd = stat_math.get_sd(data)
            var_r_1 = stat_math.get_varience(data)
            if current_envelope.get_value() > mu + sd*var_r_1:
                return current_envelope
            data.append(current_envelope.get_value())
            current_envelope_index += 1
