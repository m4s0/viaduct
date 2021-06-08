from src.database import Database


class Fixtures(Database):
    def clean_database(self):
        self.execute_query("SET FOREIGN_KEY_CHECKS=0")
        self.execute_query("TRUNCATE TABLE user")
        self.execute_query("TRUNCATE TABLE api_key")
        self.execute_query("TRUNCATE TABLE api_key_usage")
        self.execute_query("SET FOREIGN_KEY_CHECKS=1")

    def there_is_an_user_with_an_api_key_and_n_usage_at(self, username, api_key_value, n, at):
        self.create_user(username)
        user = self.find_user(username)
        self.create_api_key(user['id'], api_key_value)
        api_key = self.find_api_key(api_key_value)
        for x in range(0, n):
            self.create_api_key_usage(api_key['id'], at)

    def create_user(self, username):
        query = """
                INSERT INTO user
                (username)
                VALUES (%s)
                """

        values = (username,)

        self.execute_query(query, values)

    def find_user(self, username):
        query = """
                SELECT * FROM user
                WHERE username = %(username)s
                """

        values = {'username': username}

        return self.execute_query(query, values)

    def create_api_key(self, user_id, api_key_value):
        query = """
                INSERT INTO api_key
                (user_id, value)
                VALUES (%s, %s)
                """

        values = (user_id, api_key_value)

        self.execute_query(query, values)

    def find_api_key(self, api_key_value):
        query = """
                SELECT * FROM api_key
                WHERE value = %(api_key)s
                """

        values = {'api_key': api_key_value}

        return self.execute_query(query, values)

    def create_api_key_usage(self, api_key_id, used_at):
        query = """
                INSERT INTO api_key_usage
                (api_key_id, used_at)
                VALUES (%s, %s)
                """

        values = (api_key_id, used_at)

        self.execute_query(query, values)
