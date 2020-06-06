from django.db import models


# area====>深圳市
# area.parant===>广东省
# area.parent_id===>广东省的id
# area.area_set====>area.subs


class Area(models.Model):
    name = models.CharField(max_length=20)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subs')

    class Meta:
        db_table = 'tb_areas'

    def __str__(self):
        return self.name
