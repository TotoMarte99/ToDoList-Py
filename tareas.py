from tkinter import *
from tkinter import messagebox
import sqlite3

root = Tk()
root.title('To Do List - TM')
root.geometry('500x500')

coon = sqlite3.connect('todo.db')

c = coon.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed TEXT NOT NULL
    )
""")



coon.commit()

#funcion que elimina las tareas de la base de datos donde el id coincida con el id seleccionado
def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id,))
        coon.commit()
        renderizadoToDo()
    return _remove
    

def completadoo(id):
    def _completado():
        todo = c.execute("SELECT * from todo WHERE id = ?", (id,)).fetchone()
        completed = todo[3] == "1" 
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (str(int(not completed)), id))        
        coon.commit()
        renderizadoToDo()

    return _completado


#1-funcion que renderiza tareas, selecciona todas las que esten ingresadas en la base de datos, cambia los estados de cada tarea luego de asignarle un check
#2-y en donde se le asgina el check a cada item
def renderizadoToDo():

    for widget in frame.winfo_children():
     widget.destroy()
    
    rows = c.execute("SELECT * FROM todo").fetchall()
  
    for i in range(0, len(rows)):
       id = rows[i][0]
       completados = rows[i][3] == "1"
       descripccion = rows[i][2]
       color = '#555555' if completados else '#555554'  
       task = Checkbutton(
            frame,
            text= descripccion,
            width=42,
            fg=color,
            anchor='w',
            command=completadoo(id)
        )
       task.grid(row=i, column=0, sticky='w')
       btn2 = Button(frame,text='Eliminar', command=remove(id))
       btn2.grid(row=i,column=1)
       if completados:
           task.select()


       

#funcion en donde se agregan a la base de datos todas las tareas que se ingresen en el todo
def addToDo():
    todo = e.get()
    if todo:
        c.execute("""

        INSERT INTO todo (description, completed) VALUES (?,?)

        """, (todo,False))
        coon.commit()
        e.delete(0,END)
        renderizadoToDo()
    else:
        messagebox.showinfo("Atención", "No puedes agregar una tarea vacia")
        pass



#------ESTILOS--------#

# Configurar redimensionamiento
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)

# Etiqueta y campo de entrada
l = Label(root, text='Tarea:')
l.grid(row=0, column=0, sticky=W, padx=5, pady=5)

e = Entry(root)
e.grid(row=0, column=1, sticky=W+E, padx=5, pady=5)

# Botón para agregar tareas
btn = Button(root, text='Agregar', command=addToDo)
btn.grid(row=0, column=2, sticky=E, padx=5, pady=5)

# Frame para contener las tareas
frame = LabelFrame(root, text='Mis tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky=N+S+E+W, padx=5, pady=5)

# Hacer que el frame se expanda
frame.columnconfigure(0, weight=1)



root.bind('<Return>',lambda x: addToDo())
renderizadoToDo()
root.mainloop()