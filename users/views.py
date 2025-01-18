from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import sqlite3
def connect():
    connection = sqlite3.connect('./db.sqlite3', check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor
def users(request):
    connection, cursor = connect()
    cursor.execute('SELECT * FROM auth_user')
    users = [list(i) for i in cursor.fetchall()]
    cursor.close()
    data = {
        "users": users
    }
    return render(request, "users.html", context=data)
    
def user_change_state(request, id=0):
    connection, cursor = connect()
    cursor.execute('SELECT * FROM auth_user')
    users = [list(i) for i in cursor.fetchall()]
    cursor.close()
    connection, cursor = connect()
    if request.user.id == id:
        pass
    else:
        cursor.execute('UPDATE auth_user SET is_superuser = ? WHERE id = ?', (int(not([i for i in users if i[0]==id][0][3])), id))
        connection.commit()
        cursor.close()
    return redirect(reverse('users'))
    