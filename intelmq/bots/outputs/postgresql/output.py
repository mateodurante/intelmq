# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import psycopg2
from intelmq.lib.bot import Bot


class PostgreSQLBot(Bot):

    def init(self):
        self.logger.debug("Connecting to PostgreSQL")
        self.con = psycopg2.connect(database=self.parameters.database,
                                    user=self.parameters.user,
                                    password=self.parameters.password,
                                    host=self.parameters.host,
                                    port=self.parameters.port,
                                    )
        self.cur = self.con.cursor()
        self.logger.info("Connected to PostgreSQL")

    def process(self):
        event = self.receive_message()

        keys = ", ".join(event.keys())
        values = event.values()
        fvalues = len(values) * "%s, "
        query = "INSERT INTO events (" + keys + \
            ") VALUES (" + fvalues[:-2] + ")"

        self.cur.execute(query, values)
        self.con.commit()

        self.acknowledge_message()


if __name__ == "__main__":
    bot = PostgreSQLBot(sys.argv[1])
    bot.start()
