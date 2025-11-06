import sqlalchemy


class BaseTools:

    def __init__(self):
        self.engine = sqlalchemy.create_engine("sqlite:///todo_list.db")
        self.metadata = sqlalchemy.MetaData()

    def create_table(self, date):
        sqlalchemy.Table(date, self.metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("task", sqlalchemy.Text),
                         sqlalchemy.Column("completed", sqlalchemy.Integer, default=False)
                         )
        self.metadata.create_all(self.engine)

    def add_task(self, date, task, completed=0):
        new_task = (sqlalchemy.Table(date, self.metadata, autoload_with=self.engine)
                    .insert()
                    .values([{"task": task, "completed": completed}]))

        with self.engine.begin() as conn:
            conn.execute(new_task)

        task_list = sqlalchemy.Table(date, self.metadata, autoload_with=self.engine)

        with self.engine.connect() as conn:
            return len(conn.execute(task_list.select()).fetchall())

    def complete_task(self, date, task_id, completed=1):
        task_table = sqlalchemy.Table(date, self.metadata, autoload_with=self.engine)
        update_task = task_table.update().where(task_table.c.id == task_id).values(completed=completed)

        with self.engine.begin() as conn:
            conn.execute(update_task)

    def delete_task(self, date, task_id):
        task_table = sqlalchemy.Table(date, self.metadata, autoload_with=self.engine)
        delete_task = task_table.delete().where(task_table.c.id == task_id)

        with self.engine.begin() as conn:
            conn.execute(delete_task)

    def edit_task(self, date, task_id, new_text):
        task_table = sqlalchemy.Table(date, self.metadata, autoload_with=self.engine)
        update_task = task_table.update().where(task_table.c.id == task_id).values(task=new_text)

        with self.engine.begin() as conn:
            conn.execute(update_task)

    def get_tasks(self, date):

        try:
            task_list = sqlalchemy.Table(date, self.metadata, autoload_with=self.engine)

            with self.engine.connect() as conn:
                tasks = conn.execute(task_list.select()).fetchall()

        except sqlalchemy.exc.NoSuchTableError:
            self.create_table(date)
            tasks = []

        return tasks
