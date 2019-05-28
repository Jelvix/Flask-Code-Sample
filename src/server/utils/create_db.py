import sys
import getopt
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import argparse


def create_empty_db(db_name, username, password=""):
    print(db_name, username, password)
    con = psycopg2.connect(user="postgres", host='127.0.0.1',
                           password=password)

    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = con.cursor()
    cur.execute("CREATE DATABASE %s  ;" % db_name)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', '-d', help="database name", type=str)
    parser.add_argument('--username', '-u', help="username for database", type=str, default="")
    parser.add_argument('--password', '-p', help="password for database", type=str, default="")
    args = parser.parse_args()
    create_empty_db(args.database, args.username, args.password)
    # try:
    #     opts, args = getopt.getopt(argv, "hd:u:p:", ["ifile=", "ofile="])
    # except getopt.GetoptError:
    #     print('test.py -i <inputfile> -o <outputfile>')
    #     sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
