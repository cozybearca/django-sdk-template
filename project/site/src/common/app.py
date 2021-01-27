from django.apps import AppConfig


class CommonApp(AppConfig):
    name = "src.common"

    def ready(self):
        """
        Although you can access model classes as described above, avoid interacting with
        the database in your ready() implementation. This includes model methods that
        execute queries (save(), delete(), manager methods etc.), and also raw SQL
        queries via django.db.connection. Your ready() method will run during startup of
        every management command. For example, even though the test database
        configuration is separate from the production settings, manage.py test would
        still execute some queries against your production database!
        """
        pass
