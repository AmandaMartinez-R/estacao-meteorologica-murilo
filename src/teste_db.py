from database import *

init_db()

print("Inserindo...")
id1 = inserir_leitura(25.5, 60)
id2 = inserir_leitura(26.2, 65)

print("\nListando:")
for l in listar_leituras():
    print(dict(l))