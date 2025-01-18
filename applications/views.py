from django.shortcuts import render, redirect
from django.urls import reverse
import sqlite3
error = False
def connect():
    connection = sqlite3.connect('./db.sqlite3', check_same_thread=False)
    cursor = connection.cursor()
    return connection, cursor
def applications_user(request):
    global error
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM applications')
    applications = [list(i) for i in cursor.fetchall()]
    filtered_inventory = [i for i in inventory if i[2]=="Есть"]
    current_filters = []
    if request.method=="POST":
        current_filters.append(request.POST.get("name", "")) 
        current_filters.append(request.POST.get("condition", ""))
        for i in current_filters:
            if i=="Всё":
                continue
            filtered_inventory = [j for j in filtered_inventory if i in j]
    data = {"names": list(set([i[1] for i in inventory])),
            "possible_conditions": ["Всё","Новый","Используемый","Сломанный","В ремонте"],
            "inventory": filtered_inventory,
            "filters": current_filters,
            "my_applications": [[i[0], [j[1] for j in inventory if j[0]==i[1]][0], [j[4] for j in inventory if j[0]==i[1]][0], i[3]] for i in applications if i[2]==request.user.id],
            "error": error}
    error = False
    return render(request, "applications.html", context=data)
def applications_admin(request):
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Inventory')
    inventory = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM auth_user')
    users = [list(i) for i in cursor.fetchall()]
    cursor.execute('SELECT * FROM applications')
    applications = [list(i) for i in cursor.fetchall()]
    cursor.close()
    if request.method=="POST":
        for i in applications:
            connection, cursor = connect()
            content = request.POST.get(f"application{i[0]}", "")
            if content=="ignore":
                continue
            elif content=="decline":
                pass
            elif content=="confirm":
                cursor.execute("""UPDATE Inventory SET belonging = ?, condition = ? WHERE id = ?""", ([j[4] for j in users if j[0]==i[2]][0], "Используемый", i[1],))
                connection.commit()
                cursor.close()
            connection, cursor = connect()
            cursor.execute("""DELETE FROM applications WHERE id=?""", (i[0],))
            connection.commit()
            cursor.close()
    connection, cursor = connect()        
    cursor.execute('SELECT * FROM applications')
    applications = [list(i) for i in cursor.fetchall()]
    cursor.close()
    data = {"applications_data": [[i[0], [j[4] for j in users if j[0]==i[2]][0], [j[1] for j in inventory if j[0]==i[1]][0], [j[4] for j in inventory if j[0]==i[1]][0]] for i in applications]}
    return render(request, "applications_admin.html", context=data)
def application_create(request, instr_id):
    global error
    connection, cursor = connect()
    cursor.execute('SELECT * FROM applications')
    applications = cursor.fetchall()
    index = 1
    try:
        index = applications[-1][0]+1
    except:
        pass
    if len([j for j in applications if j[1]==instr_id and j[2]==request.user.id and j[3]=="На рассмотрении"])==0:
        cursor.execute('INSERT INTO applications (id, instrument_id, user_id, status) VALUES (?, ?, ?, ?)', (index, instr_id, request.user.id, "На рассмотрении"))
        connection.commit()
    else:
        error = True
    return redirect(reverse('applications_user'))
# Create your views here.
