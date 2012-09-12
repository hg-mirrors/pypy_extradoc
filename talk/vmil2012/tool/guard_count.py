import json
import csv
MISSING=1e-30
with file("logs/guard_summary.json") as f:
    data = json.load(f)
with file("logs/resume_summary.csv") as f:
    reader = csv.DictReader(f, delimiter=',')
    csv_data = dict([(l['bench'], l) for l in reader])


rows = []
max_guardcount = 0
for bench, d in data.iteritems():
    failures = sorted(d['results'].values())
    total_failures = float(sum(failures))
    normed_failures = [f/total_failures for f in failures]
    guardcount = int(csv_data[bench]['number of guards'])
    normed_failures.reverse()
    normed_failures += [MISSING] * (guardcount - len(failures))
    # marker to see where it ends
    normed_failures += [1]
    rows.append(normed_failures)
    max_guardcount = max(guardcount, max_guardcount)

nbenchs = len(rows)



with file("logs/guard_failures.csv", "w") as out:
    writer = csv.writer(out)
    res = []
    for k in data.keys():
        res += [k,k]
    writer.writerow(res)

    for i in range(max_guardcount):
        res = []
        for row in rows:
            if i < len(row):
                res.append(i/float(len(row)))
                res.append(row[i])
            else:
                row += [MISSING,MISSING]
        writer.writerow(res)
