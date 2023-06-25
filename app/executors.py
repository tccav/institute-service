from mayim import PostgresExecutor, query
from models.institute import Institute
from typing import List

class instituteExecutor(PostgresExecutor):

    @query("SELECT id, name FROM faculties")
    async def get_institutes(self) -> List[Institute]:
        ...