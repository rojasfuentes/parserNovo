#from loadFiles import file_path , master_path, nota
import re
import pandas as pd

# TEST : Nota
nota = 100
## TEST: df_parser
file_path = r'C:\Users\JFROJAS\Desktop\PARSER\Novo\Archivos\03 Order_Detail_Report_Mexico_original - MEDISITK.xlsx'
df = pd.read_excel(file_path)
df = df.iloc[:, [2, 13, 14, 16]]
df.columns = ['Id'] + list(df.columns[1:])


# Master de clientes
master_path = r'C:\Users\JFROJAS\Desktop\PARSER\Novo\Archivos\Maestro de Clientes (1).xlsx'
df_master = pd.read_excel(master_path, header=6)
df_master = df_master.iloc[:, [1]]


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

df_final.to_excel('test.xlsx', index=False)

print(df_final.head())
#print(df_master.keys())
