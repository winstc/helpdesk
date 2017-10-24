from django.db import models

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

    userName = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, default="No Description")
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default="W")
    priority = models.IntegerField(default=5)
    submissionDate = models.DateTimeField('date submitted')

    def __str__(self):
        return str(self.userName)