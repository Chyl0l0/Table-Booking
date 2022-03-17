from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Room(models.Model):
    rows = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    columns = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    tables_number = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_from = models.DateField()
    date_to = models.DateField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " rows=" + str(self.rows) + " columns=" + str(self.columns)


class Table(models.Model):

    # TABLE_STATUS = (('available', 'available'),
    #                 ('reserved', 'reserved'),
    #                 ('unavailable', 'unavailable'))
    #status = models.CharField(max_length=20, choices=TABLE_STATUS, default='unavailable')

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    seats_number = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(25)])
    x_pos = models.PositiveIntegerField(default=0)
    y_pos = models.PositiveIntegerField(default=0)


    def __str__(self):
        return str(self.seats_number)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.OneToOneField(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    timeTo = models.TimeField()
    duration = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.table)



