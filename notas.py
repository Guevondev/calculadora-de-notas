import csv
# Obtiene un int n de notas a partir de input por consola
# Se asegura de que lo entregado sea un número natural sin detener el programa
def obtener_n_notas() -> int:
    while True:
        n = input('Ingrese el número de notas: ')
        if n.isnumeric() and n != '0':
            return int(n)
        print('Por favor, ingrese un número natural válido')


def obtener_notas(n_notas):
    print("ingrese sus notas: (nota pendiente ingresar 0)")
    notas = []
    for i in range(1, n_notas+1):
        nota = 0.5
        while (nota != 0 and not (nota >= 1 and nota <= 7)):
            nota = float(input("nota " + str(i) + ": "))
            notas.append(nota)
    print()
    return notas

def obtener_peso_notas(n_notas):
    opt = ""
    pesos = []

    while not (opt in ["Y", "y", "N", "n"]):
        opt = input("promedio simple? (Y/N) ")

    if opt in ["Y", "y"]:
        val_peso = 100/n_notas
        pesos = [val_peso for x in range(n_notas)]

    if opt in ["N", "n"]:
        val_check = 0
        print("ingrese el valor de cada nota: (porcentaje entre 0 y 100)")
        for i in range(1, n_notas+1):
            val_peso = 0
            while not (val_peso > 0 and val_peso <= 100):
                val_peso = int(input("valor nota " + str(i) + ": "))
            val_check += val_peso
            pesos.append(val_peso)
        if val_check != 100:
            print("Advertencia: el peso de las notas no suma 100")
            print("Suma de pesos: ", val_check)
    print()
    return pesos

def calcular_nota(n_notas, notas, pesos):
    promedio = 0
    for i in range(n_notas):
        if notas[i] == 0:
            # asumir notas pendientes como 1
            promedio += pesos[i]*0.01
        else:
            promedio += notas[i]*pesos[i]*0.01
    return promedio

def crear_excel(n_notas, notas, pesos, promedio):
    with open('calculadora de notas.csv', 'w', newline='') as csvfile:
        csv_notas = csv.writer(csvfile, dialect='excel')
        
        # Calcular notas asumiendo las pendientes en 1
        csv_notas.writerow(["Notas","Peso (%)","Valor", "" ,"Promedio"])
        if notas[0] == 0:
            csv_notas.writerow([1, str(pesos[0]).replace(".", ","),"=A2*B2*0,01", "" ,"=SUMA(C2:C" + str(n_notas + 1) +")"])
        else:
            csv_notas.writerow([str(notas[0]).replace(".", ","), str(pesos[0]).replace(".", ","),"=A2*B2*0,01", "" ,"=SUM(C2:C" + str(n_notas + 1) +")"])

        for i in range(1, n_notas):
            if notas[i] == 0:
                csv_notas.writerow([1, str(pesos[i]).replace(".", ","),"=A{i}*B{i}*0,01".format(i= i+2), "" ,""])
            else:
                csv_notas.writerow([str(notas[i]).replace(".", ","), str(pesos[i]).replace(".", ","),"=A{i}*B{i}*0,01".format(i= i+2), "" ,""])

        # Calcular con notas minimas para el 4
    
        # Revisar si hay notas pendientes
        notas_pendientes = []
        for i in range(n_notas):
            if notas[i] == 0:
                notas_pendientes.append(notas[i])
        if len(notas_pendientes) == 0:
            print("no hay notas pendientes")
            return
    
        notas = notas_minimas(n_notas, notas, pesos, promedio)
        notas = [round(n, 2) for n in notas]
        csv_notas.writerow(["","","","" ,""])
        csv_notas.writerow(["Notas minimas","Peso (%)","Valor", "" ,"Promedio"])
        csv_notas.writerow([str(notas[0]).replace(".", ","), str(pesos[0]).replace(".", ","),"=A{0}*B{0}*0,01".format(4+n_notas), "" ,"=SUM(C{0}:C{1})".format(4+n_notas, 4+ 2*n_notas)])

        for i in range(1, n_notas):
            csv_notas.writerow([str(notas[i]).replace(".", ","), str(pesos[i]).replace(".", ","),"=A{i}*B{i}*0,01".format(i= i+4+n_notas), "" ,""])
    return

def notas_minimas(n_notas, notas, pesos, promedio):
    orden_index_pesos = []
    pesos_copy = [p for p in pesos]
    for i in range(n_notas):
        peso_max = pesos_copy[0]
        index_max = 0
        for p in range(n_notas):
            if pesos_copy[p] > peso_max:
                peso_max = pesos_copy[p]
                index_max = p
        # ignorar si no es una nota pendiente
        if notas[index_max] == 0:
            orden_index_pesos.append(index_max)
        pesos_copy[index_max] = -1
    
    for i in range(n_notas):
        if notas[i] == 0:
            notas[i] = 1

    while promedio < 4:
        for i in orden_index_pesos:
            notas[i] += 0.1
            promedio = calcular_nota(n_notas, notas, pesos)
            if promedio >= 4:
                return notas
    return notas

def main():
    n_notas = obtener_n_notas()
    notas = obtener_notas(n_notas)
    pesos = obtener_peso_notas(n_notas)
    promedio = calcular_nota(n_notas, notas, pesos)
    print("asumiendo tus notas pendientes en 1, tu promedio es ", round(promedio, 2))

    opt = ""
    while not (opt in ["Y", "y", "N", "n"]):
        if promedio >= 4:
            opt = input("crear excel? (Y/N) ")
        else:
            opt = input("crear excel y calcular nota minima? (Y/N) ")

    if opt in ["Y", "y"]:
        crear_excel(n_notas, notas, pesos, promedio)
        print("archivo csv creado, ábrelo con excel o spreadsheets")

if __name__ == "__main__":
    main()