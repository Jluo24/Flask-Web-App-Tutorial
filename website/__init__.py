from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import mysql.connector


db = SQLAlchemy()
DB_NAME = "database.db"
config = {
    'user': 'Jack_admin',
    'password': '1234',
    'host': '127.0.0.1',
    'database': 'schema1',
    'port': 3306
}
cnx = mysql.connector.connect(**config)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
#    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

#    cursor.execute(f"Show tables like 'user'")
#    print(cursor.fetchone(), "hi")

    create_table_user()
    create_table_notes()

#    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query(f'user_id = {int(id)}')

    # def load_user(id):
    #     return User.query.get(int(id))

    return app


def dbase_check(table):
    cursor = cnx.cursor()
    cursor.execute(f"Show tables like '{table}'")
    return cursor.fetchone()
    cursor.close()


def create_table_user():
    cursor = cnx.cursor()
    if not dbase_check('user'):
        cursor.execute("""CREATE TABLE `schema1`.`user` (
`user_id` INT NOT NULL AUTO_INCREMENT,
`email` VARCHAR(45) NOT NULL,
`password` VARCHAR(45) NOT NULL,
`name` VARCHAR(45) NOT NULL,
PRIMARY KEY (`user_id`),
UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);
"""
                       )
        print('Created table user!')
    cursor.close()


def create_table_notes():
    cursor = cnx.cursor()
    if not dbase_check('notes'):
        cursor.execute("""
CREATE TABLE `schema1`.`notes` (
`notes_id` INT NOT NULL AUTO_INCREMENT,
`data` MEDIUMTEXT NOT NULL,
`date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
`user_id` INT NOT NULL,
PRIMARY KEY (`notes_id`),
UNIQUE INDEX `idnotes_UNIQUE` (`notes_id` ASC) VISIBLE);
"""
                       )
        print('Created table notes!')
    cursor.close()

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
