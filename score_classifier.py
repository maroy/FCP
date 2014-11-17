import sys

perfect_path = 'perfectSubmission.csv' if len(sys.argv) == 1 else sys.argv[1]

with open('out.csv', 'rb') as out:
    out_lines = [line.strip().split(',') for line in out.readlines()]

perfection = {}
with open(perfect_path, 'rb') as perfect:
    items = [line.strip().split(',') for line in perfect.readlines()]
    for item in items:
        perfection[item[0]] = item[1]

out_lines_len = len(out_lines)
correct = 0
for i in range(0, out_lines_len):
    if out_lines[i][1] == perfection[out_lines[i][0]]:
        correct += 1

print correct, "of", out_lines_len
print float(correct) / float(out_lines_len-1)