from django.db import models
from django.db import migrations, models 
import django.db.models.deletion
# Create your models here


class Specialty(models.Model) :
    Specialty = models.CharField(max_length=100, default="", primary_key=True)

    def __str__(self) :
        return(self.Specialty)
    
    class Meta:
        db_table = "pd_specialty"
class Credential(models.Model) :
    Credential = models.CharField(max_length=20, default="", primary_key=True)

    def __str__(self) :
        return(self.Credential)
    class Meta:
        db_table = "pd_credential"

class State(models.Model) :
    state = models.CharField(max_length=30)
    stateabbrev = models.CharField(max_length=2, primary_key=True)
    population = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)

    def __str__(self) :
        return(self.stateabbrev)
    class Meta:
        db_table = "pd_statedata"

class Drugs(models.Model) :
    drugid = models.IntegerField(default=0)
    drugname = models.CharField(max_length=50, primary_key=True)
    isopioid = models.BooleanField(default=False)
    average = models.IntegerField(default=0)

    def __str__(self) :
        return(self.drugname)
    class Meta:
        db_table = "pd_drugs"

class Prescriber(models.Model) : 
    NPI = models.IntegerField(default=0, primary_key=True)
    Fname = models.CharField(max_length=25)
    Lname = models.CharField(max_length=25)
    Gender = models.CharField(max_length=1)
    StateAbbreviation = models.ForeignKey(State, default="", max_length=2, on_delete=models.DO_NOTHING, db_column="StateAbbreviation")
    Credential = models.CharField(max_length=25)
    Specialty = models.CharField(max_length=50)
    IsOpioidPrescriber = models.CharField(max_length=5)
    TotalPrescriptions = models.IntegerField(default=0)

    def __str__(self) :
        return(self.prescriber_name)

    @property
    def prescriber_name(self) :
        return '%s %s' % (self.Fname, self.Lname)

    def save(self) :
        super(Prescriber, self).save()
    class Meta:
        db_table = "pd_prescriber"

class Triple(models.Model) :
    id = models.IntegerField(default=0, primary_key=True)
    prescriberid = models.ForeignKey(Prescriber, default=0, on_delete=models.DO_NOTHING, db_column="prescriberid")
    drugname = models.ForeignKey(Drugs, default="", on_delete=models.DO_NOTHING, db_column="drugname")
    qty = models.IntegerField(default=0)
    
    def __str__(self) :
        return(self.prescriber_data)

    @property
    def prescriber_data(self) :
        return '%s %s' % (self.prescriberid, self.drugname)
    class Meta:
        db_table = "pd_triple"