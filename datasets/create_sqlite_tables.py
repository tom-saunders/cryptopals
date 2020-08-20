#!/usr/bin/env python

import sqlite3
import csv
import argparse
import re

def setup():
    argparser = argparse.ArgumentParser(
            description = 'Utility to create sqlite3 database from input datasets.')
    argparser.add_argument(
            '-o',
            '--output-path',
            type = str,
            required = False,
            default = 'ngrams.sqlite')
    argparser.add_argument(
            '-i',
            '--input-name',
            dest = 'input_names',
            action = 'append',
            type = str,
            required = True)
    argparser.add_argument(
            '-b',
            '--base-path',
            type = str,
            default = './',
            required = False)
    argparser.add_argument(
            '-s',
            '--header-suffix',
            type = str,
            default = '-grams.hdr',
            required = False)
    argparser.add_argument(
            '-d',
            '--data-suffix',
            type = str,
            default = '-grams.tsv',
            required = False)

    args = argparser.parse_args()

    return args

def create_table(*, db, table_name, base_path, header_suffix):
    header_path = f'{base_path}/{table_name}{header_suffix}'
    with open(header_path, 'r') as header_file:
        reader = csv.reader(
                header_file,
                delimiter = '\t')
        header = next(reader)
    # yes, this isn't the right way to do this but it's a util
    # for use here and now. I'm happy the table names aren't
    # going to inject anything, and if they did then so what?
    col_decls = []
    primary_key = []
    for field in header:
        if re.match(r'^[a-z_]+$', field):
            col_decls.append(f"{field} BLOB")
            primary_key.append(f'{field}')
        else:
            col_decls.append(f'"{field}" INTEGER')

    all_decls = ', '.join(col_decls)
    drop_sql = f'drop table if exists {table_name}'
    if primary_key:
        primary_keys = ', '.join(primary_key)
        primary_key_sql = f', primary key({primary_keys})'
    else:
        primary_key_sql = ''
    create_sql = f'create table {table_name} ({all_decls}{primary_key_sql})'
    db.execute(drop_sql)
    db.execute(create_sql)
    db.commit()

    return len(header)

def populate_table(*, db, table_name, num_columns, base_path, data_suffix):
    data_path = f'{base_path}/{table_name}{data_suffix}'
    with open(data_path, 'r') as data_file:
        reader = csv.reader(
                data_file,
                delimiter = '\t')
        cursor = db.cursor()
        for data in reader:
            subst = ', '.join(['?' for x in range(0, num_columns)])
            insert_sql = f'insert into {table_name} values ({subst})'
            cursor.execute(insert_sql, tuple(data))

        db.commit()

def load_db(*, db_path):
    db = sqlite3.connect(db_path)
    return db

def main():
    args = setup()
    with sqlite3.connect(args.output_path) as db:
        for input_name in args.input_names:
            num_columns = create_table(
                    db = db,
                    table_name = input_name,
                    base_path = args.base_path,
                    header_suffix = args.header_suffix)
            populate_table(
                    db = db,
                    table_name = input_name,
                    num_columns = num_columns,
                    base_path = args.base_path,
                    data_suffix = args.data_suffix)

if __name__ == '__main__':
    main()
