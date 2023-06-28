from loadFiles import order_path, master_path, nota
import pandas as pd
import PySimpleGUI as sg

# TEST: Nota
# nota = 100
## TEST: df_parser
# order_path = r'C:\Users\JFROJAS\Desktop\PARSER\Novo\Archivos\03 Order_Detail_Report_Mexico_original - MEDISITK.xlsx'
df = pd.read_excel(order_path)
df = df.iloc[:, [2, 13, 14, 16]]
df.columns = ['Id'] + list(df.columns[1:])

# Master de clientes
# master_path = r'C:\Users\JFROJAS\Desktop\PARSER\Novo\Archivos\Maestro de Clientes (1).xlsx'
df_master = pd.read_excel(master_path, header=6)
df_master = df_master.iloc[:, [1, 9, 8, 12]]

#print(df_master)

previous_id = ''
increment = 0

def add_nota(row):
    global previous_id
    global increment
    global nota

    current_id = row['Id']
    if current_id != previous_id:
        increment += 1
        previous_id = current_id

    return 'NN-' + str(nota + increment)

df['Id Pedido'] = df.apply(add_nota, axis=1)
df['Linea'] = range(1, len(df) + 1)
df['Lote'] = None
df['Caducidad'] = None
df['Estatus de Inventario'] = None
df['Bill To'] = df['ONE KEY ID']
df['Ship To'] = df['ONE KEY ID']
df = df.rename(columns={'Sample Product Code': 'Codigo Producto'})

df_final = df.iloc[:, [4, 5, 1, 6, 7, 2, 9, 10]]

# Buscar clientes en el maestro y agregar columnas correspondientes
clientes_faltantes = []

for cliente in df['Bill To']:
    if cliente not in df_master['Cliente'].values:
        clientes_faltantes.append(cliente)
    else:
        cliente_info = df_master[df_master['Cliente'] == cliente].iloc[0]
        tipo_proceso = cliente_info['Tipo de proceso']
        estado = cliente_info['Estado']
        localidad = cliente_info['Ciudad']
        df_final.loc[df_final['Bill To'] == cliente, 'Tipo de proceso'] = tipo_proceso
        df_final.loc[df_final['Bill To'] == cliente, 'Estado'] = estado
        df_final.loc[df_final['Bill To'] == cliente, 'Ciudad'] = localidad

# GUI
if clientes_faltantes:
    # Los convertimos a un dataframe y los guardamos en un archivo de excel
    clientes_faltantes_df = pd.DataFrame(clientes_faltantes, columns=['Cliente'])
    clientes_faltantes_df.to_excel('Clientes Faltantes.xlsx', index=False)
    sg.Popup(f"Se han encontrado {len(clientes_faltantes)} clientes faltantes. Revisa el archivo 'Clientes Faltantes.xlsx'.")
else:
    sg.Popup("Todos los clientes están registrados en el sistema.")

df_final.to_excel('test.xlsx', index=False)

#print(df_final.head())
#print(df_master.head())
