from q import app

if __name__ == "__main__":

    sql_create_questions0 = ''' CREATE TABLE IF NOT EXISTS db0 (
                                    id integer PRIMARY KEY,
                                    username text NOT NULL,
                                    gender text NOT NULL,
                                    age integer NOT NULL,
                                    language text NOT NULL,
                                    city text NOT NULL,
                                    education integer NOT NULL,
                                    specialization integer NOT NULL
                                    );
                            '''

    sql_create_questions1 = ''' CREATE TABLE IF NOT EXISTS db1 (
                                    id integer REFERENCES db0(id) ON DELETE CASCADE ON UPDATE NO ACTION,
                                    city text NOT NULL,
                                    river text NOT NULL,
                                    countryside text NOT NULL,
                                    village text NOT NULL,
                                    lake text NOT NULL,
                                    island text NOT NULL,
                                    state text NOT NULL,
                                    mountain text NOT NULL,
                                    sierra text NOT NULL,
                                    peninsula text NOT NULL,
                                    square text NOT NULL,
                                    strait text NOT NULL
                                    );
                            '''

    sql_create_questions2 = ''' CREATE TABLE IF NOT EXISTS db2 (
                                    id integer REFERENCES db0(id) ON DELETE CASCADE ON UPDATE NO ACTION,
                                    city text NOT NULL,
                                    river text NOT NULL,
                                    countryside text NOT NULL,
                                    village text NOT NULL,
                                    lake text NOT NULL,
                                    island text NOT NULL,
                                    state text NOT NULL,
                                    mountain text NOT NULL,
                                    sierra text NOT NULL,
                                    peninsula text NOT NULL,
                                    square text NOT NULL,
                                    strait text NOT NULL
                                    );
                            '''

    sql_create_search = ''' CREATE TABLE IF NOT EXISTS db3 (
                                    phrase text NOT NULL,
                                    gender text NOT NULL,
                                    lage integer NOT NULL,
                                    rage integer NOT NULL,
                                    education integer NOT NULL,
                                    specialization integer NOT NULL
                                    );
                            '''
    
    conn = create_connection(DATABASE)
    if conn is not None:
        create_table(conn, sql_create_questions0)
        create_table(conn, sql_create_questions1)
        create_table(conn, sql_create_questions2)
        create_table(conn, sql_create_search)
        conn.commit()
    else:
        print('Can\'t create the database connection')
    app.run(host='0.0.0.0')