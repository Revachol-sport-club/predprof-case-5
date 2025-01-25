from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import sqlite3
from datetime import date
def connect():
    connection = sqlite3.connect('./db.sqlite3', check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor
def inventory_editing(request):
    error = False
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM auth_user')
    users_usernames = ["Ничьё"] + [i[4] for i in [list(i) for i in cursor.fetchall()]]
    cursor.close()
    try:
        index = inventory[-1][0] + 1
    except:
        index = 1
    if request.method=="POST":
        connection, cursor = connect()
        if request.POST.get("name", "")!="":
            for i in range(int(request.POST.get("quantity", ""))):
                condition = "Используемый" if request.POST.get("belonging", "") != "Ничьё" and request.POST.get("condition", "") == "Новый" else request.POST.get("condition", "")
                cursor.execute('INSERT INTO Inventory (id, name, availability, condition, belonging) VALUES (?, ?, ?, ?, ?)', (index+i, request.POST.get("name",""), request.POST.get("availability",""), condition, request.POST.get("belonging",""),))
                connection.commit()
            cursor.close()
        else:
            error = True
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.close()
    data = {"inventory": inventory,
            "possible_users": users_usernames,
            "possible_conditions": ["Новый","Используемый","Сломанный","В ремонте"],
            "error": error,
            }
    return render(request, "inventory_editing.html", context=data)
def inventory_purchase(request):
    connection, cursor = connect()
    cursor.execute('SELECT * FROM purchase_list')
    purchase_list = [list(i) for i in cursor.fetchall()]
    cursor.close()
    if request.method=="POST":
        try:
            index = purchase_list[-1][0]+1
        except:
            index=1
        connection, cursor = connect()
        cursor.execute('INSERT INTO purchase_list (id, name, company_name, quantity, price, status) VALUES (?, ?, ?, ?, ?, ?)', (index, request.POST.get("name",""), request.POST.get("company_name",""), request.POST.get("quantity",""), request.POST.get("price",""), "Отправлено"))
        connection.commit()
        cursor.close()
    connection, cursor = connect()
    cursor.execute('SELECT * FROM purchase_list')
    purchase_list = [list(i) for i in cursor.fetchall()]
    cursor.close()
    data = {"purchase_list": purchase_list[::-1],
            
    }
    return render(request, "inventory_purchase.html", context=data)
def inventory_report(request):
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM auth_user')
    users = [list(i) for i in cursor.fetchall()]
    cursor.close()
    data = {"information": [len(inventory), len([i for i in inventory if i[3]=="Новый"]), len([i for i in inventory if i[3]=="Используемый"]), len([i for i in inventory if i[3]=="Сломанный"]), len([i for i in inventory if i[3]=="В ремонте"])],
            "inventory": inventory,
            "instrument_names": [[i, len([j for j in inventory if j[1]==i])] for i in set([k[1] for k in inventory])],
            "users_instruments": [[i[4], [j[1] for j in inventory if j[-1]==i[4]]] for i in users],
    }
    return render(request, "inventory_report.html", context=data)
def inventory_edit_instrument(request, id=1):
    error = False
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM auth_user')
    users_usernames = ["Ничьё"] + [i[4] for i in [list(i) for i in cursor.fetchall()]]
    instrument = [i for i in inventory if i[0]==id][0]
    cursor.close()
    if request.method=="POST":
        connection, cursor = connect()
        condition = "Новый" if request.POST.get("belonging", "") == "Ничьё" and request.POST.get("condition", "") == "Используемый" else "Используемый" if request.POST.get("belonging", "") != "Ничьё" and (request.POST.get("condition", "") in ["Новый", "Используемый"]) else request.POST.get("condition", "")
        if request.POST.get("name","") == "":
            error = True
        else:
            cursor.execute('UPDATE Inventory SET name = ?, availability = ?, condition = ?, belonging = ? WHERE id = ?', (request.POST.get("name",""), request.POST.get("availability",""), condition, request.POST.get("belonging",""), id))
            connection.commit()
            cursor.close()
            return redirect("inventory_editing")
    data={"instrument": instrument,
          "possible_users": users_usernames,
          "possible_conditions": ["Новый","Используемый","Сломанный","В ремонте"],
          "error": error,
          }
    return render(request, "inventory_edit_instrument.html", context=data)