import gzip
import json
import os

# --- CONFIGURACIÓN ---
archivo_entrada = r"C:\Ruta\A\Tu\latest-all.json.gz"
archivo_salida = r"C:\Ruta\A\Tu\personas_wikidata.nt"


def procesar_wikidata():
    print("Iniciando procesamiento... Esto tardará varias HORAS dependiendo de tu procesador.")

    count = 0
    encontrados = 0

    with gzip.open(archivo_entrada, 'rt', encoding='utf-8') as f_in, open(archivo_salida, 'w', encoding='utf-8') as f_out:

        # Saltamos el primer carácter '[' que abre el JSON de Wikidata
        f_in.read(1)

        for line in f_in:
            line = line.strip()
            if line.endswith(','): line = line[:-1]  # Quitamos la coma al final de la línea
            if not line: continue

            try:
                entidad = json.loads(line)
            except:
                continue

            # 1. FILTRO: ¿Es un humano? (P31 -> Q5)
            claims = entidad.get('claims', {})
            es_humano = False
            if 'P31' in claims:
                for statement in claims['P31']:
                    if statement.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id') == 'Q5':
                        es_humano = True
                        break

            if es_humano:
                encontrados += 1
                id_sujeto = entidad['id']
                label = entidad.get('labels', {}).get('es', {}).get('value',entidad.get('labels', {}).get('en', {}).get('value', 'Sin nombre'))

                # Escribimos en formato N-Triples básico para GraphDB
                # <ID> <Nombre> "Nombre"
                f_out.write(
                    f'<http://www.wikidata.org/entity/{id_sujeto}> <http://www.w3.org/2000/01/rdf-schema#label> "{label}" .\n')

                # 2. EXTRAER ATRIBUTOS (Ejemplo: Ocupación P106)
                if 'P106' in claims:
                    for s in claims['P106']:
                        val = s.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id')
                        if val:
                            f_out.write(
                                f'<http://www.wikidata.org/entity/{id_sujeto}> <http://www.wikidata.org/prop/P106> <http://www.wikidata.org/entity/{val}> .\n')

            count += 1
            if count % 10000 == 0:
                print(f"Procesadas {count} entidades... {encontrados} personas encontradas.", end='\r')

    print(f"\n¡Listo! Se guardaron {encontrados} personas en {archivo_salida}")


if __name__ == "__main__":
    procesar_wikidata()