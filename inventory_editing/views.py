from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, FileResponse
import sqlite3
import os
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
    users_usernames = ["Свободно"] + [i[4] for i in [list(i) for i in cursor.fetchall()]]
    cursor.close()
    try:
        index = inventory[-1][0] + 1
    except:
        index = 1
    if request.method=="POST":
        connection, cursor = connect()
        if request.POST.get("name", "")!="":
            for i in range(int(request.POST.get("quantity", ""))):
                condition = "Используемый" if request.POST.get("belonging", "") != "Свободно" and request.POST.get("condition", "") == "Новый" else request.POST.get("condition", "")
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
    if request.method == "POST":
        report = open("report "+str(date.today()) + ".txt", "w+")
        report_text = f"Всего инструментов: {data['information'][0]}\n"
        for i in data["instrument_names"]:
            report_text += f"   {i[0]}: {i[1]}\n"
        report_text += f"Используемых инструментов: {data['information'][2]}\n"
        for i in data["users_instruments"]:
            report_text += f"   Используется пользователем {i[0]} ({len(i[1])}): "
            for j in i[1]:
                report_text += f"{j}, \n"
            if len(i[1])==0:
                report_text+="-\n"
        report_text += f"Новых инструментов: {data['information'][1]}\n"
        report_text += f"Сломанных инструментов: {data['information'][3]}\n"
        report_text += f"Инструментов в ремонте: {data['information'][4]}\n"
        report_text += f"Дата генерации отчёта: {date.today()}"
        report.write(report_text)
        report.close()
        return FileResponse(open("./report "+str(date.today())+".txt","rb"),as_attachment=True)
    try:
        os.remove("./report "+str(date.today())+".txt")
    except:
        pass
    return render(request, "inventory_report.html", context=data)
def inventory_edit_instrument(request, id=1):
    error = False
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM auth_user')
    users_usernames = ["Свободно"] + [i[4] for i in [list(i) for i in cursor.fetchall()]]
    instrument = [i for i in inventory if i[0]==id][0]
    cursor.close()
    if request.method=="POST":
        connection, cursor = connect()
        condition = "Новый" if request.POST.get("belonging", "") == "Свободно" and request.POST.get("condition", "") == "Используемый" else "Используемый" if request.POST.get("belonging", "") != "Свободно" and (request.POST.get("condition", "") in ["Новый", "Используемый"]) else request.POST.get("condition", "")
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

def inventory_delete_instrument(request, id=1):
    connection, cursor = connect()
    cursor.execute('DELETE FROM Inventory WHERE id = ?', (id, ))
    cursor.execute('DELETE FROM applications WHERE instrument_id = ?', (id, ))
    connection.commit()
    cursor.close()
    return redirect("inventory_editing")
