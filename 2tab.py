import re
import sys
import Orange
from sample_set import SampleSet

int_strs = [str(i) for i in range(0,41)]
columns = [
    ("Id",                                  "d",                        "meta"),
    ("Elevation",                           "c",                        ""),
    ("Aspect",                              "c",                        "ignore"),
    ("AspectX",                             "c",                        "ignore"),
    ("AspectY",                             "c",                        "ignore"),
    ("AspectNorm",                          "c",                        "ignore"),
    ("Slope",                               "c",                        "ignore"),
    ("Horizontal_Distance_To_Hydrology",    "c",                        ""),
    ("Vertical_Distance_To_Hydrology",      "c",                        ""),
    ("AboveNearestSurfaceWater",            " ".join(int_strs[0:2]),    "ignore"),
    ("ABS_Vertical_Distance_To_Hydrology",  "c",                        "ignore"),
    ("Horizontal_Distance_To_Roadways",     "c",                        ""),
    ("Hillshade_9am",                       "c",                        ""),
    ("Hillshade_Noon",                      "c",                        ""),
    ("Hillshade_3pm",                       "c",                        ""),
    ("Hillshade_Total",                     "c",                        "ignore"),
    ("Hillshade_Mean",                      "c",                        "ignore"),
    ("Horizontal_Distance_To_Fire_Points",  "c",                        ""),
    ("Wilderness_Area",                     " ".join(int_strs[1:5]),    ""),
    ("Soil_Type",                           " ".join(int_strs[1:41]),   "ignore"),
    ("ClimaticZone",                        " ".join(int_strs[1:9]),    ""),
    ("GeologicZone",                        " ".join(int_strs[1:8]),    ""),
    ("Cover_Type",                          " ".join(int_strs[1:8]),    "class")
]

def to_tab(is_training, is_raw, in_path, add_cover_type):

    out_path = re.sub("csv$|data$", "tab", in_path)

    sample_set = SampleSet(is_training, is_raw)
    sample_set.read(in_path)

    perfection = {}

    if add_cover_type:
        with open('perfectSubmission.csv', 'rb') as perfect:
            items = [line.strip().split(',') for line in perfect.readlines()]
            for item in items:
                perfection[item[0]] = item[1]

        for sample in sample_set:
            sample.Cover_Type = perfection[str(sample.Id)]

    with open(out_path, 'w') as f:
        for i in range(0,3):
            f.write("\t".join([col[i] for col in columns]) + "\n")

        for sample in sample_set:
            values = []
            for col in columns:
                values.append(getattr(sample, col[0]))

            f.write("\t".join([str(v) for v in values]) + "\n")


def main():
    is_training = sys.argv[1].upper() == "TRUE"
    is_raw = sys.argv[2].upper() == "TRUE"
    in_path = sys.argv[3]

    add_cover_type = len(sys.argv) > 4 and sys.argv[4].upper() == "TRUE"

    to_tab(is_training, is_raw, in_path, add_cover_type)


if __name__ == "__main__":
    main()