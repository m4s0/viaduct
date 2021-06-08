from datetime import datetime

from src.database import Database


class ApiKey(Database):
    async def find_api_key(self, api_key):
        query = """
                SELECT * FROM api_key
                WHERE value = %(value)s
                """
        values = {
            'value': api_key,
        }

        return Database.execute_query(self, query, values)

    async def count_api_key_usage(self, used_at, api_key_id):
        query = """
                SELECT count(used_at)
                FROM api_key_usage
                WHERE api_key_id = %(api_key_id)s
                AND used_at = %(used_at)s
                GROUP BY api_key_id, used_at
                ORDER BY used_at DESC
                LIMIT 1
                """

        values = {
            'api_key_id': api_key_id,
            'used_at': used_at
        }

        result = Database.execute_query(self, query, values)
        return result['count(used_at)'] if result is not None else 0

    async def update_api_key_usage(self, api_key_id):
        query = """
                INSERT INTO api_key_usage
                (used_at, api_key_id)
                VALUES (%(used_at)s, %(api_key_id)s);
                """

        values = {
            'used_at': datetime.now(),
            'api_key_id': api_key_id,
        }

        Database.execute_query(self, query, values)
