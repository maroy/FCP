from sample import Sample


class SampleSet:

    def __init__(self, is_training, is_raw):
        self.is_training = is_training
        self.is_raw = is_raw
        self.samples = []

    def add(self, file_line):
        sample = Sample(self.is_training, self.is_raw, file_line)
        self.samples.append(sample)

    def __getitem__(self, i):
        return self.samples[i]

    def read(self, file_path):
        with open(file_path, 'rb') as f:
            if not self.is_raw:
                f.readline()
            for l in f:
                self.add(l.strip())

    def __len__(self):
        return len(self.samples)