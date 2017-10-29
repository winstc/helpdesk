from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    class Meta:
        permissions = (("can_view_all", "View all tickets"), ("can_open", "Open a new ticket"),
                       ("can_edit_tickets", "Has full control of tickets"))

    COMPLETE = 'C'
    WAITING = "W"
    IN_PROGRESS = "I"

    STATUS_CHOICES = (
        (COMPLETE, "Complete"),
        (IN_PROGRESS, "In Progress"),
        (WAITING, "Waiting")
    )

    user = models.OneToOneField(User, default=1)
    description = models.TextField()
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default="W")
    priority = models.IntegerField(default=1)
    submissionDate = models.DateTimeField('date submitted')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ipAddress = models.GenericIPAddressField()

    def __str__(self):
        return str(self.user.username + " - " + str(self.submissionDate.date()))


class Question(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    questionTitle = models.CharField(max_length=100)
    questionText = models.TextField()
    questionHelpText = models.TextField()
    questionType = models.CharField(max_length=15)


class File(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.file.name


