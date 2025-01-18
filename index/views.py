from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
def connect():
    connection = sqlite3.connect('./db.sqlite3', check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor
def index(request):
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = cursor.fetchall()
    cursor.close()
    data = {"inventory": inventory}
    return render(request, "index.html", context=data)

# Create your views here.
