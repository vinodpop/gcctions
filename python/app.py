from enum import EnumMeta
from sqlite3.dbapi2 import sqlite_version
from flask import Flask, json, request, jsonify
from werkzeug.wrappers import response
import sqlite3
app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("users.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM users")
        users = [
            dict(id=row[0], fullname=row[1], empid=row[2])
            for row in cursor.fetchall()
        ]
        if users is not None:
            return jsonify(users)
        else:
            return jsonify({"msg": "There is nothing to show"}), 200
    if request.method =='POST':
        new_fullname = request.form['fullname']
        new_empid = request.form['empid']
        sql_query = """ INSERT INTO users (fullname, empid) VALUES(?, ?)"""

        cursor = conn.execute(sql_query, (new_fullname, new_empid))
        conn.commit()
        return f"Your new changes has been made with id: {cursor.lastrowid}", 201

        # new_obj = {
        #     'id': iD,
        #     'fullname': new_fullname,
        #     'empid': new_empid
        # }
        # user_list.append(new_obj)
        # return jsonify(user_list), 201

    # else:
    #     return jsonify({"msg": "Use the correct request method: GET/POST is allowed"}), 400

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_user(id):
    conn = db_connection()
    cursor = conn.cursor()
    users = None
    if request.method == 'GET':
        cursor.execute("SELECT * FROM users WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            users = r
        if users is not None:
            return jsonify(users), 200
        else:
            return "Somethind is wrong/You are searching for the users doesnt exist", 404
    # if request.method == 'GET':
    #     conn = db_connection()
    #     cursor = conn.cursor()
    #     for user in user_list:
    #         if user['id'] == id:
    #             return jsonify(user)
    #         pass
    if request.method == 'PUT':
        sql_query = """ UPDATE users SET fullname=?,empid=? WHERE id=? """
        fullname = request.form['fullname']
        empid = request.form['empid']
        updated_list = {
                'id': id,
                'fullname': fullname,
                'empid': empid
                 }
        conn.execute(sql_query, (fullname, empid, id))
        conn.commit
        return jsonify(updated_list)
    if request.method == 'DELETE':
        sql_query = """ DELETE FROM users WHERE id=? """
        conn.execute(sql_query, (id, ))
        conn.commit()
        return "Thats great! we have successfulle removed the ID: {}".format(id), 200

        # for index, user in enumerate(user_list):
        #     if user['id'] == id:
        #         user_list.pop(index)
        #         return jsonify(user_list)          

if __name__ == '__main__':
    app.run(debug=True)



