import math


class Sample:

    soil_type_info = [
        "0000",
        "2702",
        "2703",
        "2704",
        "2705",
        "2706",
        "2717",
        "3501",
        "3502",
        "4201",
        "4703",
        "4704",
        "4744",
        "4758",
        "5101",
        "5151",
        "6101",
        "6102",
        "6731",
        "7101",
        "7102",
        "7103",
        "7201",
        "7202",
        "7700",
        "7701",
        "7702",
        "7709",
        "7710",
        "7745",
        "7746",
        "7755",
        "7756",
        "7757",
        "7790",
        "8703",
        "8707",
        "8708",
        "8771",
        "8772",
        "8776"
    ]

    def __init__(self, is_training, is_raw, file_line):
        self.is_training = is_training

        strings = file_line.split(',')
        ints = iter([int(item.strip()) for item in strings])

        self.Id = ints.next() if not is_raw else 0
        self.Elevation = ints.next()
        aspect = float(ints.next())
        aspect_x = math.cos(math.pi * aspect / 180.0)
        aspect_y = math.sin(math.pi * aspect / 180.0)
        self.Aspect = aspect
        self.AspectX = aspect_x
        self.AspectY = aspect_y
        self.AspectNorm = math.sqrt(math.pow(1-aspect_x,2) + math.pow(0-aspect_y,2))
        self.Slope = ints.next()
        self.Horizontal_Distance_To_Hydrology = ints.next()
        v_dist_to_water = ints.next()
        self.Vertical_Distance_To_Hydrology = v_dist_to_water
        self.AboveNearestSurfaceWater = 1 if v_dist_to_water < 0 else 0
        self.ABS_Vertical_Distance_To_Hydrology = abs(v_dist_to_water)
        self.Horizontal_Distance_To_Roadways = ints.next()
        self.Hillshade_9am = ints.next()
        self.Hillshade_Noon = ints.next()
        self.Hillshade_3pm = ints.next()
        self.Hillshade_Total = self.Hillshade_9am + self.Hillshade_Noon + self.Hillshade_3pm
        self.Hillshade_Mean = (self.Hillshade_9am + self.Hillshade_Noon + self.Hillshade_3pm) / 3.0
        self.Horizontal_Distance_To_Fire_Points = ints.next()

        for i in range(1, 5):
            x = ints.next()
            if x == 1:
                self.Wilderness_Area = i

        for i in range(1, 41):
            x = ints.next()
            if x == 1:
                self.Soil_Type = i

        self.ClimaticZone = int(Sample.soil_type_info[self.Soil_Type][0])
        self.GeologicZone = int(Sample.soil_type_info[self.Soil_Type][1])

        self.Cover_Type = ints.next() if self.is_training else 0