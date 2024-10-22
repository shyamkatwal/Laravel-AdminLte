from django.db import models

class AddressBook(models.Model):
    # Adjust field types according to your table structure
    fld_fname = models.CharField(max_length=100)
    fld_email = models.EmailField()
    fld_mobile = models.CharField(max_length=10)
    fld_lname = models.CharField(max_length=100)

    class Meta:
        db_table = 'tbl_addressbook'  # Specify the existing table name