from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import mysql.connector


config = {
    'user': 'Jack_admin',
    'password': '1234',
    'host': '127.0.0.1',
    'database': 'schema1',
    'port': 3306
}
cnx = mysql.connector.connect(**config)


class Table():
    _filt = ''

    def __init__(self):
        self1 = self

    def query(self1, filt, entry_pos='one'):
        cursor = cnx.cursor()
        self1 = self
        cursor.execute(
            f"select * from {self._tble} where {self._filt} {filt}")
        col_name = cursor.column_names
        entry_obj = cursor.fetchall()
        if not entry_obj:
            entry = ''
        elif entry_pos == 'one':
            entry = entry_obj[0]
        else:
            entry = []

            for i in range(len(entry_obj[0])):
                ent_inner = []
                for ent in entry_obj:
                    ent_inner.append(ent[i])
                entry.append(ent_inner)

        value_dic = dict(zip(col_name, entry))
        for k, v in value_dic.items():
            setattr(self, k, v)
        cursor.close()
        return self1

    def add(self):
        cursor = cnx.cursor()
        var_list = [attr for attr in dir(
            self) if not callable(getattr(self, attr)) and not attr.startswith('_') and not attr in self._exc_list]
        val_list = [getattr(self, var) for var in var_list]
        var_inp = str(var_list)[1:-1].replace("'", "")
        print(var_inp)
        print(str(val_list))
        cursor.execute(
            f"INSERT INTO {self._tble} ({var_inp}) VALUES ({str(val_list)[1:-1]})")
        cnx.commit()
        cursor.close()

    def delete(self, filt):
        cursor = cnx.cursor()
        cursor.execute(f"DELETE FROM {self._tble} WHERE {filt}")
        cnx.commit()
        cursor.close()


class User(Table, UserMixin):
    _tble = 'user'
    _exc_list = ['user_id']

    def __init__(self, name='', email='', password=''):
        self.email = email
        self.name = name
        self.password = password


class Note(Table, UserMixin):
    _tble = 'notes'
    _exc_list = ['notes_id', 'date']

    def __init__(self, data='', user_id=''):
        self.data = data
        self.user_id = user_id


class Join(Table):
    def __init__(self, table1, table2, join_f1, join_f2=''):
        _table_list = [table1._tble, table2._tble]
        self._tble = var_inp = str(_table_list)[1:-1].replace("'", "")
        if join_f2 == '':
            join_f2 = join_f1
        self._filt = f"{table1._tble}.{join_f1} = {table2._tble}.{join_f2} and"


"""
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
"""


# class dbase():
#     for column in columns:
#         col_state = f"column"
#     TABLES['employees'] = (
#         "CREATE TABLE `employees` ("
#         "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
#         "  `birth_date` date NOT NULL,"
#         "  `first_name` varchar(14) NOT NULL,"
#         "  `last_name` varchar(16) NOT NULL,"
#         "  `gender` enum('M','F') NOT NULL,"
#         "  `hire_date` date NOT NULL,"
#         "  PRIMARY KEY (`emp_no`)"
#         ") ENGINE=InnoDB")
#     TABLES['User'] = (
#         "CREATE TABLE '{}' ("
#     )


#     new_user = User(email=email, first_name=first_name, password=generate_password_hash(
#                 password1, method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()


#                 new_note = Note(data=note, user_id=current_user.id)
#             db.session.add(new_note)
#             db.session.commit()


# CREATE TABLE `schema1`.`user` (
#   `user_id` INT NOT NULL AUTO_INCREMENT,
#   `email` VARCHAR(45) NOT NULL,
#   `password` VARCHAR(45) NOT NULL,
#   `name` VARCHAR(45) NOT NULL,
#   PRIMARY KEY (`user_id`),
#   UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);
