import sqlite3


def store_to_db(db_name, data):
    """do something once we have downloaded a page

    :parser: the parser object
    :data: @todo
    :success: @todo
    :failed: @todo
    :returns: @todo

    """
    build = []
    for job in data:
        build.append((job['url'], job['title'], job['description'],
                      job['name'], job['keyword'], job['job_id']))
    sql = """insert into jobs (url, title, description, name, keyword,
             job_id) values(?, ?, ?, ?, ?, ?)"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.executemany(sql, build)
    conn.commit()
    conn.close()


def create_db(db_name):
    """create database
    :returns: @todo

    """
    conn = sqlite3.connect(db_name)
    sql = '''CREATE TABLE jobs (url text, title text, description text,
             name text, keyword text, job_id real unique)'''
    try:
        conn.execute(sql)
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()
