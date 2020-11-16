class PostgresRouter:
    default_app_labels = {'django_celery_beat'}

    auth_app_labels = {'auth', 'contenttypes', 'admin', 'session', 'authentication'}

    premises_app_labels = {'premises'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.default_app_labels:
            return 'default'
        elif model._meta.app_label in self.auth_app_labels:
            return 'auth_db'
        elif model._meta.app_label in self.premises_app_labels:
            return 'premises_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.default_app_labels:
            return 'default'
        elif model._meta.app_label in self.auth_app_labels:
            return 'auth_db'
        elif model._meta.app_label in self.premises_app_labels:
            return 'premises_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.default_app_labels
            and obj2._meta.app_label in self.default_app_labels
        ):
            return True
        elif (
            obj1._meta.app_label in self.auth_app_labels
            and obj2._meta.app_label in self.auth_app_labels
        ):
            return True
        elif (
            obj1._meta.app_label in self.premises_app_labels
            and obj2._meta.app_label in self.premises_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.default_app_labels:
            return db == 'default'
        elif app_label in self.auth_app_labels:
            return db == 'auth_db'
        elif app_label in self.premises_app_labels:
            return db == 'premises_db'
        return None
