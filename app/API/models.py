from django.db import models


class RoadName(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Date(models.Model):
    year = models.IntegerField()

    def __str__(self):
        return str(self.year)


class Category(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class StartJunction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)


class EndJunction(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)


class BasicCountMethod(models.Model):
    method = models.CharField(max_length=10)

    def __str__(self):
        return self.method


class DetailedCountMethod(models.Model):
    method = models.CharField(max_length=60)

    def __str__(self):
        return self.method


class Direction(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


models.CASCADE


class RoadInfo(models.Model):
    road = models.ForeignKey(RoadName, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    junc_start = models.ForeignKey(
        StartJunction,
        on_delete=models.CASCADE,
        related_name="start_junction_road_name",
        null=True,
        blank=True,
    )
    junc_end = models.ForeignKey(
        EndJunction,
        on_delete=models.CASCADE,
        related_name="end_junction_road_name",
        null=True,
        blank=True,
    )

    len_mi = models.FloatField(null=True, blank=True)
    len_km = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.road)


class Location(models.Model):
    count_point_ref = models.IntegerField()
    easting = models.IntegerField()
    latitude = models.FloatField()
    northing = models.IntegerField()
    longitude = models.FloatField()

    def __str__(self):
        return "ref: {} ({}, {})".format(
            self.count_point_ref, self.latitude, self.longitude
        )


class CountMethod(models.Model):
    basic_count_method = models.ForeignKey(
        BasicCountMethod, on_delete=models.CASCADE
    )
    detailed_count_method = models.ForeignKey(
        DetailedCountMethod, on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}: {}".format(
            str(self.basic_count_method).upper(), self.detailed_count_method
        )


class Record(models.Model):
    road = models.ForeignKey(RoadInfo, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    count_method = models.ForeignKey(CountMethod, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.date.year, self.road)


class Count(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE)
    all_hgvs = models.IntegerField()
    all_motor_vehicles = models.IntegerField()
    pedal_cycles = models.IntegerField()
    two_wheeled_motor_vehicles = models.IntegerField()
    cars_and_taxis = models.IntegerField()
    buses_and_coaches = models.IntegerField()
    lgvs = models.IntegerField()
    hgvs_2_rigid_axle = models.IntegerField()
    hgvs_3_rigid_axle = models.IntegerField()
    hgvs_4_or_more_rigid_axle = models.IntegerField()
    hgvs_3_or_4_articulated_axle = models.IntegerField()
    hgvs_5_articulated_axle = models.IntegerField()
    hgvs_6_articulated_axle = models.IntegerField()
