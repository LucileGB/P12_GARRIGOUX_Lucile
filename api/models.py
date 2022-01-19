from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import CIEmailField
from django.core.validators import MinValueValidator

class Client(models.Model):
    email = CIEmailField(
        "email address",
        unique=True,
        max_length=100,
        help_text="Required. 100 characters or fewer.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField("first name", max_length=25)
    last_name = models.CharField("last name", max_length=25)
    # TODO: func - check entered phone number
    phone_number = models.CharField("phone nomber", max_length=20)
    mobile_number = models.CharField("phone nomber", max_length=20)
    company_name = models.CharField("company name", max_length=25)

    date_created = models.DateTimeField("date joined", default=timezone.now)
    date_updated = models.DateTimeField("date updated", default=timezone.now)
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)

    USERNAME_FIELD = "email"

    # TODO: add sales_contact?
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "company_name", ]

    @classmethod
    def create(cls, email, first_name, last_name, phone_number, mobile_number,
                company_name):
        client = cls(email=email, first_name=first_name, last_name=last_name,
                    phone_number=phone_number, mobile_number=mobile_number,
                    company_name=company_name)

        return client

    def __str__(self):
        return f"{self.company_name}: {self.first_name} {self.last_name}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                    related_name="sales_contact",
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL,)
    # QUESTION: comment gérer en cas de suppression ?
    client = models.ForeignKey(to=Client,
                            on_delete=models.SET_NULL,
                            blank=True, null=True)
    date_created = models.DateTimeField("date joined", default=timezone.now)
    # TODO: func - update updated
    date_updated = models.DateTimeField("date joined", default=timezone.now)
    status = models.BooleanField(default=True)
    amount = models.FloatField(
        validators=[MinValueValidator(0.0),]
        )
    payment_due = models.DateField()

    @classmethod
    def create(cls, sales_contact, client, status, amount, payment_due):
        contract = cls(sales_contact=sales_contact, client=client, status=status,
                    amount=amount, payment_due=payment_due)

        return contract

    def __str__(self):
        return self.id

class Event(models.Model):
    client = models.ForeignKey(to=Client,
                            on_delete=models.SET_NULL,
                            blank=True, null=True)
    date_created = models.DateTimeField("date joined", default=timezone.now)
    # TODO: func - update updated
    date_updated = models.DateTimeField("date joined", default=timezone.now)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                        related_name="support_contact",
                                        on_delete=models.SET_NULL,
                                        blank=True, null=True)
    status = models.BooleanField(default=True)
    attendees = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0),]
        )
    event_date = models.DateField()
    notes = models.TextField(max_length=1000)

    @classmethod
    def create(cls, client, support_contact, status, attendees, event_date, notes):
        event = cls(client=client, support_contact=support_contact, status=status,
                        attendees=attendees, event_date=event_date, notes=notes)

        return event

    def __str__(self):
        return self.id
