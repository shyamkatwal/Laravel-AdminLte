from django.db import models


class MyModel(models.Model):
    user_id = models.IntegerField()
    #name = models.CharField(max_length=255)

    class Meta:
        db_table = "finfadm.urm_upr_coreserver"  # Use the actual table name in Oracle
