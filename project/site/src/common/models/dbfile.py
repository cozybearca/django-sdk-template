import hashlib

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models as m


class DBFile(m.Model):
    """
    An internal data storage node used by DBFileField. DBFile and DBFileField are
    designed to be bijective. DBFile is read-only. Its content once set cannot be
    changed. Further, files are treated as values: when changing the value assigned to a
    DBFileField, you assign a new DBUploadedFile instance to the field, instead of
    modifying the content of its DBFile object. This is designed to simplify handling
    user upload. Since two DBFileField always have different associated DBFile
    instances, reassigning a file on one model instance never affects other instances.
    """

    name = m.CharField(max_length=100, unique=True, db_index=True)  # see Storage
    content = m.BinaryField()
    md5 = m.CharField(max_length=32, db_index=True)
    size = m.PositiveIntegerField(default=0)
    suggested_name = m.CharField(max_length=100, blank=True, default="")
    # accessed_time = m.DateTimeField(auto_now=True)
    # created_time = m.DateTimeField(auto_now_add=True)
    # modified_time = m.DateTimeField(auto_now=True)

    content_type = m.ForeignKey(ContentType, on_delete=m.CASCADE, null=True)
    object_id = m.PositiveIntegerField(null=True, db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        index_together = ["object_id", "content_type"]

    def write(self, content):
        if len(self.content):
            raise IOError("DBFile is read-only.")
        self.content = content
        self.size = len(content)
        self.save()
        self.__update_md5()

    def __update_md5(self):
        algo = hashlib.md5()
        algo.update(self.content)
        self.md5 = algo.hexdigest()
        self.save()

    # def dump_to_media(self):
    #     dest = settings.MEDIA_DIR / self.name
    #     dest.parent.mkdir(parents=True, exist_ok=True)
    #     dest.write_bytes(self.content)
    #     return dest
