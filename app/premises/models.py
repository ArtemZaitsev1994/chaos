from django.db import models

from uuid import uuid4

from core.models import (TimestampedModel, UUIDModel)


class PremisesTimestampedModel(TimestampedModel):

    class Meta:
        abstract = True
        app_label = 'premises'


class PremisesUUIDModel(UUIDModel):

    class Meta:
        abstract = True
        app_label = 'premises'


class PremisesAddress(PremisesTimestampedModel):

    country_name = models.CharField(max_length=30, default="")
    country_code = models.CharField(max_length=10, default="")
    post_code = models.PositiveIntegerField()
    city_name = models.CharField(max_length=30)
    street = models.CharField(max_length=128, default="")
    house_number = models.PositiveIntegerField()

    def __str__(self):
        return '{} {}, {} {}, {}'.format(self.street, self.house_number, self.post_code,
                                         self.city_name, self.country_code)


class PremisesDiscountDuration(PremisesTimestampedModel):

    RENT_DURATION = (
        (0, 'Week'),
        (1, 'One month'),
        (2, 'One and half month')
    )
    rent_duration = models.PositiveSmallIntegerField(default=0, choices=RENT_DURATION)

    discount_size = models.PositiveIntegerField()

    def __str__(self):
        return '{}: {}'.format(self.rent_duration, self.discount_size)


class PremisesSeason(PremisesTimestampedModel):

    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return '{} - {}'.format(self.date_start, self.date_end)


class PremisesSeasonDiscount(PremisesTimestampedModel):

    season = models.ForeignKey(PremisesSeason, on_delete=models.CASCADE)
    discount_size = models.PositiveIntegerField()

    def __str__(self):
        return '{}: {}'.format(self.season, self.discount_size)


class PremisesSeasonMarkup(PremisesTimestampedModel):

    season = models.ForeignKey(PremisesSeason, on_delete=models.CASCADE)
    markup_size = models.PositiveIntegerField()

    def __str__(self):
        return '{}: {}'.format(self.season, self.markup_size)


class PremisesDiscountsMarkup(PremisesTimestampedModel):

    discount_rental_period = models.ManyToManyField(PremisesDiscountDuration,
                                                    related_name="discount_for_rental_duration")
    season_discount_size = models.ManyToManyField(PremisesSeasonDiscount,
                                                  related_name="season_discount_size")
    season_markup_size = models.ManyToManyField(PremisesSeasonMarkup,
                                                related_name="season_markup_size")

    def __str__(self):
        return '{}, {}, {}'.format(self.discount_rental_period, self.season_discount_size, self.season_markup_size)


class PremisesRestrictionThing(PremisesUUIDModel):

    thing_name = models.CharField(default="", max_length=32)

    def __str__(self):
        return self.thing_name


class PremisesStorageSpace(PremisesUUIDModel):

    STORAGE_TYPES = (
        (0, 'Shelf'),
        (1, 'Rack'),
        (2, 'Box')
    )

    storage_type = models.PositiveSmallIntegerField(default=0, choices=STORAGE_TYPES)
    available_rent_duration = models.PositiveIntegerField()

    rent_price = models.PositiveIntegerField()
    discounts_and_markups = models.ForeignKey(PremisesDiscountsMarkup, on_delete=models.SET_NULL,
                                              blank=True, null=True, related_name="discounts_and_markups")

    def __str__(self):
        return '{}: {}'.format(self.storage_type, self.available_rent_duration)


class PremisesClimaticConditions(PremisesUUIDModel):

    heating = models.FloatField()
    humidity = models.FloatField()
    condensation = models.BooleanField(default=False)

    def __str__(self):
        return 'Heating: {}, humidity: {}, condensation: {}'.format(self.heating, self.humidity, self.condensation)


class PremisesAccess(PremisesUUIDModel):

    separate_entrance = models.BooleanField(default=False)
    security = models.BooleanField(default=False)

    stairs = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    without_lifting = models.BooleanField(default=False)

    def __str__(self):
        return 'Separate entrance: {}, security: {}, stairs: {}, elevator: {}, without lifting: {}'.format(
            self.separate_entrance, self.security, self.stairs, self.elevator, self.without_lifting
        )


class PremisesExtraOptions(PremisesUUIDModel):

    ceiling_height = models.FloatField()
    climatic_conditions = models.ManyToManyField(PremisesClimaticConditions, related_name="climatic_conditions")
    animals_presence = models.BooleanField(default=False)
    gas_and_smoke_detector = models.BooleanField(default=True)
    premises_access = models.ForeignKey(PremisesAccess, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return 'Ceiling: {}, climatic: {}, animals: {}, gas-smoke detector: {}'.format(
            self.ceiling_height, self.climatic_conditions, self.animals_presence, self.gas_and_smoke_detector
        )


class PremisesOwner(PremisesTimestampedModel):

    owner_profile_uuid = models.UUIDField()

    def __str__(self):
        return self.owner_profile_uuid


class PremisesReview(PremisesUUIDModel):

    premises_review_uuid = models.UUIDField()

    def __str__(self):
        return self.premises_review_uuid


class PremisesImage(PremisesUUIDModel):

    #photo = models.ImageField(upload_to="premises_images")

    def __str__(self):
        """"""
        #return self.photo


class PremisesVideo(PremisesUUIDModel):

    video = models.FileField(upload_to="premises_video_files")

    def __str__(self):
        return self.video


class PremisesMedia(PremisesUUIDModel):

    photos = models.ManyToManyField(PremisesImage, related_name="premises_photos")
    videos = models.ManyToManyField(PremisesVideo, related_name="premises_videos")


class PremisesPromises(PremisesUUIDModel):

    tax_policy = models.TextField()
    cancellation_policy = models.TextField()


class Premises(PremisesTimestampedModel):

    BOOKING_TYPE = (
        (0, 'Instant booking'),
        (1, 'Upon request')
    )

    size = models.PositiveIntegerField()
    address = models.ForeignKey(PremisesAddress, on_delete=models.SET_NULL,
                                blank=True, null=True, related_name="premises_address")

    limitation_things = models.ManyToManyField(PremisesRestrictionThing,
                                               related_name="limitation_by_type_of_things")

    rent_only_whole_premises = models.BooleanField(default=False)

    booking_type = models.PositiveSmallIntegerField(default=0, choices=BOOKING_TYPE)
    storage_spaces = models.ManyToManyField(PremisesStorageSpace,
                                            related_name="types_of_storage_spaces")

    owner = models.ForeignKey(PremisesOwner, on_delete=models.SET_NULL, blank=True, null=True)

    is_confirmed = models.BooleanField(default=False)

    reviews = models.ManyToManyField(PremisesReview)

    media = models.ForeignKey(PremisesMedia, on_delete=models.SET_NULL, blank=True, null=True)

    policies = models.ForeignKey(PremisesPromises, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.owner
