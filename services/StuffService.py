class StuffService:
    """
    Сервис для работы с сотрудниками.
    Содержит бизнес-сценарии, связанные с сотрудниками.
    """

    def __init__(self, stuff_repo, app_repo):
        self.stuff_repo = stuff_repo
        self.app_repo = app_repo

    def deleteStuffWithCheck(self, pasport):

        stuff = self.stuff_repo.readStuff(pasport)
        if stuff is None:
            raise ValueError(f"Сотрудник с паспортом {pasport} не найден")

        apps = self.app_repo.filterByExecutor(stuff)

        in_progress = [app for app in apps if app.status == 2]

        if in_progress:
            raise ValueError(
                f"Нельзя удалить сотрудника {stuff.surname} {stuff.name}: "
                f"у него {len(in_progress)} активных заявок!"
            )

        self.stuff_repo.deleteStuff(pasport)
        print(f"Сотрудник {stuff.surname} {stuff.name} удален")
        return True


