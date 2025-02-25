from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import Config

def connect_db():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, client_encoding='utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def execute_procedure(proc_name, params=None):
    session = connect_db()
    try:
        if params:
            result = session.execute(text(f"SELECT {proc_name}({params})"))
        else:
            result = session.execute(text(f"SELECT {proc_name}()"))
        session.commit()
        return result
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        return None
    finally:
        session.close()

def execute_func(func_name, params=None):
    session = connect_db()
    try:
        if params:
            result = session.execute(text(f"CALL {func_name}({params})"))
        else:
            result = session.execute(text(f"CALL {func_name}()"))
        session.commit()
        return result
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        return None
    finally:
        session.close()

def execute(func_name, params=None):
    session = connect_db()
    try:
        if params:
            result = session.execute(text(f"select * from {func_name}({params})"))
        else:
            result = session.execute(text(f"select * from {func_name}()"))
        session.commit()
        return result
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        return None
    finally:
        session.close()

def get_table_from_raw(cursor, columns=None):
    result = []
    for i in cursor:
        # print(list(i)[0].replace(")", "").replace("(", "").split(","))
        result.append(list(i)[0].replace(")", "").replace("(", "").replace('"', '').split(","))
    return [dict(zip(columns, row)) for row in result]