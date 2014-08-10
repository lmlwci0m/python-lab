__author__ = 'roberto'


class FreqAnalysis(object):

    def __init__(self, data="data/syfreq.txt"):

        with open(data) as f:
            entries = f.readlines()

        freqs = {}
        for entry in entries:
            vals = entry.strip().split(" ")
            key, value = vals[0], vals[1]
            freqs[key] = float(value)

        self.sylls = freqs