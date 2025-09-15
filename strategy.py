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


class Automatic_basestrategy:
    """
    chooses a random envelope.
    """

    def __init__(self, envelopes):
        self.envelopes = envelopes

    def display(self):
        return "Automatic Base Strategy: Pick a random envelope."

    def play(self):
        if self.envelopes:
            i= random.randint(0, len(self.envelopes)-1)
            chosen = self.envelopes[i]
            print(f"AutomaticBaseStrategy selected envelope with value: {chosen.get_value()}")
        else:
            print("No envelopes to choose from.")


class N_max_strategy:
    """
    chooses the 4th max-value envelope.
    """

    def __init__(self, envelopes):
        self.envelopes = envelopes

    def display(self):
        return "N max strategy: Pick the 4th maximum value envelope."

    def play(self):
        if self.envelopes:
            i=0
            j=1
            max=self.envelopes[0].get_value()
            while (i <= 4):
                if self.envelopes[j].get_value()>=max:
                    max=self.envelopes[j].get_value()
                    i++
                    j++
                else
                    j++
                
            chosen = self.envelopes[j]
            print(f"NMaxStrategy selected envelope with value: {chosen.get_value()}")
        else:
            print("No envelopes to choose from.")



class More_then_N_percent_group_strategy:
    """
    chooses the first envelope with higher value than 125 (12.5% of max value).
    """

    def __init__(self, envelopes):
        self.envelopes = envelopes

    def display(self):
        return "More than N percent group strategy: Pick the first envelope with higher value than 125 (12.5% of max value)."

    def play(self):
        if self.envelopes:
            i=0
            while (true):
                if self.envelopes[i].get_value()>=125:
                    chosen = self.envelopes[i]
                    print(f"NMaxStrategy selected envelope with value: {chosen.get_value()}")
                    return
                else
                    i++
        else:
            print("No envelopes to choose from.")
            return



class Best_Solution:
    """
    Optimal threshold strategy for the finite-envelope problem when envelope values
    are i.i.d. Uniform(A, B). If A,B are unknown, it uses only information seen so far:
    (optionally) skip an exploration prefix to estimate A,B, then apply the optimal
    dynamic-programming thresholds to the remainder.

    Interface mirrors the example:
      - __init__(envelopes, known_min=None, known_max=None, explore=0)
      - display()
      - play()

    Assumptions:
      - Each envelope supports .get_value()
      - Risk-neutral objective
      - Decisions are sequential and irreversible
    """

    def __init__(self, envelopes, known_min=None, known_max=None, explore=0):
        self.envelopes = envelopes or []
        self.known_min = known_min
        self.known_max = known_max
        self.explore = max(0, int(explore))  # number of envelopes to *observe and pass* to estimate A,B

    # ---------- core DP machinery ----------
    @staticmethod
    def _continuation_values(kmax):
        """
        v_0 = 0; v_k = E[max(U, v_{k-1})] with U ~ Unif[0,1] = (1 + v_{k-1}^2)/2.
        Returns list v[0..kmax].
        """
        v = [0.0] * (kmax + 1)
        for k in range(1, kmax + 1):
            v[k] = 0.5 * (1.0 + v[k - 1] ** 2)
        return v

    @staticmethod
    def _threshold_from_range(A, B, cont_value):
        # Accept now iff x >= A + (B-A) * cont_value
        return A + (B - A) * cont_value

    def display(self):
        return ("Best Solution: Optimal stopping via dynamic-programming thresholds "
                "for i.i.d. Uniform(A,B). If A,B unknown, estimate from seen values "
                "after an exploration prefix, then apply thresholds to the remainder.")

    def play(self):
        if not self.envelopes:
            print("No envelopes to choose from.")
            return None

        N = len(self.envelopes)
        # Precompute continuation values up to N
        v = self._continuation_values(N)

        # Range handling: if known_min/max provided, use them from the start.
        # Otherwise, estimate online from values we've *already seen* (never from future).
        have_known_range = (self.known_min is not None) and (self.known_max is not None)

        seen_min = float("inf")
        seen_max = float("-inf")

        chosen_idx = None
        chosen_val = None

        for t, env in enumerate(self.envelopes):
            x = env.get_value()

            # Update online range estimates with observed value
            seen_min = min(seen_min, x)
            seen_max = max(seen_max, x)

            k_remaining = N - t  # includes current
            # Continuation value to compare against is v_{k-1} on the standardized [0,1] scale
            cont_value_std = v[k_remaining - 1]

            # Determine which A,B to use at this step
            if have_known_range:
                A, B = float(self.known_min), float(self.known_max)
            else:
                # Enforce exploration prefix if requested
                if t < self.explore:
                    # Must pass; cannot select during exploration
                    continue
                # Use the best *feasible* estimate from data seen so far
                A, B = seen_min, seen_max
                # Degenerate or unsafe estimates: if B == A, no scale to compare yet; continue unless last envelope
                if not (B > A):
                    # If this is the last envelope, we must take it
                    if k_remaining == 1:
                        chosen_idx = t
                        chosen_val = x
                    continue

            threshold = self._threshold_from_range(A, B, cont_value_std)

            # Stop if current value meets/exceeds the dynamic threshold
            if x >= threshold:
                chosen_idx = t
                chosen_val = x
                break

            # If this is the last envelope and we haven't stopped, we must take it
            if k_remaining == 1:
                chosen_idx = t
                chosen_val = x

        if chosen_idx is not None:
            chosen_env = self.envelopes[chosen_idx]
            print(f"Best_Solution selected envelope #{chosen_idx + 1} with value: {chosen_val}")
            return chosen_env
        else:
            # Should not occur, but guard anyway
            print("No selection made (unexpected).")
            return None
