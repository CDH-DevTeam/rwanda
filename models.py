from tabnanny import verbose
from django.contrib.gis.db import models
import diana.abstract.models as abstract
from django.utils.translation import gettext_lazy as _

class Informant(abstract.AbstractBaseModel):

    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('X', _('Other')),
        ('-',_('Unknown'))
    ] 

    custom_id = models.CharField(max_length=256, unique=True, blank=True, null=True, verbose_name=_("custom ID"), help_text=_("An ID of the informant provided by the researcher."))
    age = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("age"), help_text=_("The approximate age of the informant."))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name=_("gender"), help_text=_("Gender of the informant, if known."))
    note = models.TextField(null=True, blank=True, verbose_name=_("note"), help_text=_("Researcher's note on informant."))

    def __str__(self) -> str:
        return self.custom_id
    
class Period(abstract.AbstractTagModel):

    start_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("start year"), help_text=_("An approximate start year, if applicable."))
    end_year = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_("end year"), help_text=_("An approximate end year, if applicable."))

class Language(abstract.AbstractBaseModel):

    name = models.CharField(max_length=512, blank=True, null=True, verbose_name=_("name"))
    abbreviation = models.CharField(max_length=8, blank=True, null=True, verbose_name=_("abbreviation"))

    class Meta:
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def __str__(self) -> str:
        return self.name



# Create your models here.
class Name(abstract.AbstractBaseModel):

    languages = models.ManyToManyField(Language, blank=True, verbose_name=_("rwanda.language"), related_name="names")
    text = models.CharField(max_length=2028, blank=True, null=True, verbose_name=_("general.text"))
    period = models.ForeignKey(Period, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_("period"), help_text=_("An approximate periodization of the name."))
    informants = models.ManyToManyField(Informant, blank=True, related_name="names", verbose_name=_("informants"), help_text=_("List of informants attesting to the name."))
    note = models.TextField(null=True, blank=True, verbose_name=_("note"), help_text=_("Researcher's note on the name."))

    class Meta:
        verbose_name = _("name")
        verbose_name_plural = _("names")

    def __str__(self) -> str:

        ls = ", ".join([f"({l.abbreviation})" for l in self.languages.all()]).rstrip()

        return f"{self.text} {ls}"

class PlaceOfInterest(abstract.AbstractBaseModel):

    names     = models.ManyToManyField(Name, verbose_name=_("rwanda.name"), blank=True, related_name="%(class)s")
    geometry = models.GeometryField(verbose_name=_("geometry"), blank=True, null=True)
    comment  = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:

        ns = ", ".join([f"{n.text}" for n in self.names.all()]).rstrip()

        return f"{ns}"


class Street(PlaceOfInterest):

    pass

    class Meta:
        verbose_name = _("rwanda.street")
        verbose_name_plural = _("rwanda.street.plural")

class Building(PlaceOfInterest):

    is_iconic = models.BooleanField(default=False)
    is_existing = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("rwanda.building")
        verbose_name_plural = _("rwanda.building.plural")

class Author(abstract.AbstractBaseModel):

    name = models.CharField(max_length=2028, verbose_name=_("general.name"))

    def __str__(self) -> str:
        return self.name

class Image(abstract.AbstractTIFFImageModel):

    street   = models.ForeignKey(Street, on_delete=models.CASCADE, related_name="images")
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="images")
    description = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField(Author, blank=True, related_name="images")
    informants = models.ManyToManyField(Informant, blank=True, related_name="images", verbose_name=_("informants"), help_text=_("List of informants attesting to the name."))



class Text(abstract.AbstractBaseModel):

    title = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_("general.title"))
    text = models.TextField(null=True, blank=True, verbose_name=_("general.text"))
    authors = models.ManyToManyField(Author, blank=True, related_name="texts")
    informants = models.ManyToManyField(Informant, blank=True, related_name="texts", verbose_name=_("informants"), help_text=_("List of informants attesting to the name."))

