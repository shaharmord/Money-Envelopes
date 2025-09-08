from envelope import Envelope
from strategy import BaseStrategy, Automatic_BaseStrategy, N_max_strategy, More_then_N_percent_group_strategy

def cls(): print ("\n" * 20)

envelopes = []
for i in range(100):
    envelopes.append(Envelope())
strategies = []
strategies.append(BaseStrategy(envelopes))                              # user select manually envelopes
strategies.append(Automatic_BaseStrategy(envelopes))                    # random selection of envelop
strategies.append(N_max_strategy(envelopes))                            # return envelope after N max values (defualt N=3)
strategies.append(More_then_N_percent_group_strategy(envelopes, 0.25))  # return envelope with more money that in the highest of N% group

n=-1
while n!=4:
    cls()
    for i in range(len(strategies)):
        print(i, strategies[i].display())
    n = input(f'enter your choice [0-{len(strategies)}] (len(strategies) to end):')
    if n.isdigit():
        n=int(n)
        if n==2:
            N = input(f'enter N max values: ')
            strategies[n].N=int(N)
        elif n==3:
            p = input(f'enter 0-1 number for group size (defualt=0.25)')
            strategies[n].percent=p
        if n!=4:    
            strategies[n].play()
        x=input('press any key to continue')
    else:
        pass
