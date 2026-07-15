from models import Application
class ApplicationService:
    def __init__(self, app_repo):
        self.app_repo = app_repo

    def complete_application(self, app_id):
        app = self.app_repo.readApplication(app_id)
        if app is None:
            raise ValueError(f"Заявка {app_id} не найдена")
        app.set_new_status()
        self.app_repo.updateApplication(app)

        print(f"Заявка {app_id} переведена в статус: {app.status}")
        return app

    def assign_executor(self, app_id, executor):
        app = self.app_repo.readApplication(app_id)
        if app is None:
            raise ValueError(f"Заявка {app_id} не найдена")

        app.set_executor(executor)

        self.app_repo.updateApplication(app)

        print(f"Исполнитель назначен на заявку {app_id}")
        return app