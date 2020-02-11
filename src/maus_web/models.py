from django.db import models
from enum import Enum


class Gender(Enum):
    M = "Male"
    F = "Female"
    I = "Indeterminate"


class BinCage(models.Model):
    class Meta:
        verbose_name_plural = "Bins or Cages"
        ordering = ['name']

    bin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    rack = models.TextField(blank=True, null=True)
    elevation = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    last_cleaned = models.DateField(blank=True, null=True)

    def __str__(self):
        resident_list = "("
        resident_mice = Mouse.objects.filter(bin_location=self.bin_id)
        if len(resident_mice) > 0:
            for i, mouse in enumerate(resident_mice):
                resident_list += mouse.name
                if i < len(resident_mice) - 1:
                    resident_list += ", "
            resident_list += ")"
        else:
            resident_list = "(Empty Bin)"

        return "%s %s" % (self.name, resident_list)


class Mouse(models.Model):
    class Meta:
        verbose_name_plural = "Mice"
        ordering = ['dob', 'name']

    mouse_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    codename = models.CharField(max_length=128, blank=True, null=True)
    gender = models.CharField(
        max_length=16,
        choices=[(tag.name, tag.value) for tag in Gender],
        blank=True,
        null=True
    )
    dob = models.DateField(blank=True, null=True)
    bin_location = models.ForeignKey(
        BinCage, on_delete=models.CASCADE,
        blank=True, null=True
    )
    deceased_on = models.DateField(blank=True, null=True)
    picture = models.FileField(blank=True, null=True)
    is_favorite = models.BooleanField(blank=True, null=True)

    def __str__(self):
        if self.gender:
            return self.name + " (" + self.gender + ")"
        else:
            return self.name


class Trait(models.Model):
    class Meta:
        ordering = ['name']

    trait_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    locus = models.CharField(max_length=3, blank=True, null=True)
    chromosome = models.IntegerField(blank=True, null=True)
    gene = models.CharField(max_length=8, blank=True, null=True)
    is_dominant = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.name + " - " + self.description


class MouseTrait(models.Model):
    class Meta:
        verbose_name_plural = "Trait on a mouse"

    mouse_id = models.ForeignKey(
        Mouse, on_delete=models.CASCADE,
    )
    trait_id = models.ForeignKey(
        Trait, on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.mouse_id.name + " has " + self.trait_id.name


class Mating(models.Model):
    class Meta:
        ordering = ['-cohabitation_start', 'buck', 'doe']

    mating_id = models.AutoField(primary_key=True)
    doe = models.ForeignKey(
        Mouse,
        on_delete=models.CASCADE,
        related_name='+',
        limit_choices_to={'gender': 'F'},
    )
    buck = models.ForeignKey(
        Mouse,
        on_delete=models.CASCADE,
        related_name='+',
        limit_choices_to={'gender': 'M'},
    )
    cohabitation_start = models.DateField(blank=True, null=True)
    cohabitation_end = models.DateField(blank=True, null=True)
    copulation_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    number_pups_born = models.IntegerField(blank=True, null=True)
    successful = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.buck.name + " and " + self.doe.name + \
               " on " + str(self.cohabitation_start)


class Offspring(models.Model):
    class Meta:
        verbose_name_plural = "Offspring"

    mouse_id = models.ForeignKey(
        Mouse, on_delete=models.CASCADE,
    )
    mating_id = models.ForeignKey(
        Mating, on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.mouse_id.name + " of " + self.mating_id.buck.name + \
            " and " + self.mating_id.doe.name
