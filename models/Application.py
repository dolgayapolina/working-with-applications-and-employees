class Application:
    def __init__(self, id, date, term, author, executor, description, status=1):
        self.id = id
        self.date = date
        self.term = term
        self.author = author
        self.executor = executor
        self.description = description
        self.status = status

    def set_new_status(self):
        if self.status == 1:  # Новая заявка
            if self.executor is None:
                raise ValueError("Нельзя перевести в работу без исполнителя!")
            self.status = 2
        elif self.status == 2:
            self.status = 3
        elif self.status == 3:
            raise ValueError("Заявка уже выполнена")

    def set_executor(self, executor):
        if self.status == 3:
            raise ValueError("Заявка уже выполнена и её исполнителя нельзя поменять")
        self.executor = executor

    def is_overdue(self, current_date):
        return current_date > self.date + self.term
