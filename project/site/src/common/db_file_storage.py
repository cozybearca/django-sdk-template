import logging
import random
import string

from django.core.files import File as DjangoFile
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from ipromise import overrides
from src.common.models import DBFile

LOG = logging.getLogger(__name__)


class DBContentFile(ContentFile):
    def __init__(self, dbfile, mode):
        self.dbfile = dbfile
        self.mode = mode
        super().__init__(dbfile.content, dbfile.name)

    @overrides(ContentFile)
    def close(self):
        if "w" in self.mode or "a" in self.mode:
            self.seek(0)
            self.dbfile.write(self.read())
        super().close()


@deconstructible
class DatabaseFileStorage(Storage):
    @overrides(Storage)
    def delete(self, name, missing_ok=False):
        LOG.debug(f"Delete {name}")
        if not self.exists(name) and not missing_ok:
            raise FileNotFoundError(name)
        DBFile.objects.get(name=name).delete()

    @overrides(Storage)
    def exists(self, name):
        return DBFile.objects.filter(name=name).exists()

    # @overrides(Storage)
    # def path(self, name):
    #     fullpath = settings.MEDIA_DIR / name
    #     if not fullpath.exists():
    #         fullpath.parent.mkdir(parents=True, exist_ok=True)
    #         model = DBFile.objects.get(name=name)
    #         LOG.debug(f"writing file {fullpath}")
    #         fullpath.write_bytes(model.content)
    #     return fullpath

    def generate_unique_filename(self):
        name = None
        while not name or self.exists(name):
            name = "".join([random.choice(string.ascii_lowercase) for _ in range(16)])
        return name

    @overrides(Storage)
    def url(self, name):
        if not self.exists(name):
            raise FileNotFoundError(name)
        return f"/media/{name}"

    def size(self, name):
        if not self.exists(name):
            raise FileNotFoundError(name)
        return DBFile.objects.get(name=name).size

    def open(self, name, mode="rb"):
        if "r" in mode:
            dbfile = DBFile.objects.select_for_update().filter(name=name).first()
            if not dbfile:
                raise FileNotFoundError(name)
        elif "w" in mode or "a" in mode:
            dbfile, _ = DBFile.objects.select_for_update().get_or_create(name=name)
        else:
            raise NotImplementedError(f"Invalid mode: {mode}")
        contentfile = DBContentFile(dbfile, mode=mode)
        contentfile.open(mode)
        return contentfile

    def save(self, name, content, max_length=None, suggested_name=""):
        LOG.debug(f"Save {name}")

        if type(content) is bytes:
            content = ContentFile(content, name=name)

        if not hasattr(content, "chunks"):
            content = DjangoFile(content, name)

        if name is None:
            name = content.name

        if not suggested_name:
            suggested_name = getattr(content, "suggested_name", "")

        available_name = self.get_available_name(name, max_length=max_length)
        if available_name != name:
            LOG.debug(f"..renamed to {available_name}")

        dbfile, _ = DBFile.objects.select_for_update().update_or_create(
            name=available_name,
            defaults=dict(suggested_name=suggested_name),
        )

        with content.open("rb") as file:
            dbfile.write(file.read())

        return available_name

    def suggested_name(self, name):
        if not self.exists(name):
            raise FileNotFoundError(name)
        dbfile = DBFile.objects.get(name=name)
        return dbfile.suggested_name
