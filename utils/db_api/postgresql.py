import asyncio
from typing import Union

import asyncpg
from asyncpg import Pool, Connection

from data import config


class Database:
    def __init__(self):
        # пул соединений
        self.pool: Union[Pool, None] = None  # Юнион говорит, что мы можем принять либо Pool либо None

    async def create_pool(self):  # создание пула соединений для бота
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,  # после выполнения запроса собрать ВСЕ данные
                      fetchrow: bool = False,  # достать только 1 строчку (не будет вложеным)
                      fetchval: bool = False,  # достать только 1 значение
                      execute: bool = False  # ничего не доставать, только выполнить
                      ):

        # асинхронный менеджер контекста
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id, full_name, username=None,):
        sql = "INSERT INTO Users (username, full_name, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, username, full_name, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
        # if "telegram_id" in kwargs:
        #     sql += " telegram_id=$1"

    async def count_users(self):
        sql = "SELECT COUNT (*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        sql = "DELETE FROM Users WHERE TRUE"
        await self.execute(sql, execute=True)

    async def drop_table(self):
        sql = "DROP TABLE Users;"
        await self.execute(sql, execute=True)

if __name__ == '__main__':
    db = Database()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.create_pool())
    print(loop.run_until_complete(db.drop_table()))
    # print(loop.run_until_complete(db.select_all_users()))
    # print(loop.run_until_complete(db.add_user(user_id=1, full_name="rus", telegram_id=321)))


