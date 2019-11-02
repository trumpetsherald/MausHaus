from django.db import models


class Mouse(models.Model):
    mouse_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    codename = models.CharField(max_length=128, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    deceased_on = models.DateField(blank=True, null=True)
    picture = models.FileField(blank=True, null=True)
    is_favorite = models.BooleanField(blank=True, null=True)


class Trait(models.Model):
    trait_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_dominant = models.BooleanField(blank=True, null=True)


class MouseTrait(models.Model):
    mouse_id = models.ManyToManyField(Mouse)
    trait_id = models.ManyToManyField(Trait)


class Mating(models.Model):
    mating_id = models.IntegerField(primary_key=True)
    doe = models.ForeignKey(Mouse, on_delete=models.CASCADE, related_name='+')
    buck = models.ForeignKey(Mouse, on_delete=models.CASCADE, related_name='+')
    cohabitation_start = models.DateField(blank=True, null=True)
    cohabitation_end = models.DateField(blank=True, null=True)
    copulation_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    successful = models.BooleanField(blank=True, null=True)


class Offspring(models.Model):
    mouse_id = models.ForeignKey(
        Mouse, on_delete=models.CASCADE,
    )
    mating_id = models.ForeignKey(
        Mating, on_delete=models.CASCADE,
    )

