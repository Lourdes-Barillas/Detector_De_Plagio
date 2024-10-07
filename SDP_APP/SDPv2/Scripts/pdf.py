from PyPDF2 import PdfReader
import openai

openai.api_key = "sk-mZws2FCsSRjhRMZmFM9arJIufLBWCQkioPJLpiApFyT3BlbkFJOgytS8yAIXw6QCihCSIMhnjXHr3EFiTEA2woyz2LsA"


#Extraer la pregunta de investigación
def extract_question(pdf_path):
    reader = PdfReader(pdf_path)
    pregunta_clave = "1.7.1 Pregunta general"
    
    # Convertir el título a minúsculas para comparación case insensitive
    pregunta_clave_lower = pregunta_clave.lower()

    # Variable para almacenar el texto extraído
    extracted_text = ""
    found_pregunta = False

    # Iterar página por página
    for page in reader.pages:
        page_text = page.extract_text()
        paragraphs = page_text.split('\n')

        for paragraph in paragraphs:
            #Buscar la palabra clave (pregunta)
            if pregunta_clave_lower in paragraph.lower():
                found_pregunta = True  # Señal de que la "pregunta" fue encontrada
                
                continue  # Pasar al siguiente párrafo para capturarlo
                
            # Si se ha encontrado la palabra clave, empezar a acumular texto
            if found_pregunta:
                # Si encontramos un párrafo vacío o un título en mayúsculas, es probable que sea el fin del texto relacionado
                if paragraph.strip() == "" or paragraph.isupper():
                    found_pregunta = False
                    break
                if '.' in paragraph:
                    extracted_text += paragraph.strip() + " "
                    break
                   
                # Acumular el texto si no parece ser un título
                extracted_text += paragraph + "\n"

    return extracted_text if extracted_text else "Pregunta no encontrada o no hay contenido relevante."

def obtener_pregunta(pdf_path):
    #pdf_path = "c:/SitioWeb/SDP_PG2/SDP_APP/media/Documentos_prueba/Sistema_Web_detector_de_plagios_de_tesis/entrega2.pdf"
    parrafo = extract_question(pdf_path)
    if parrafo is not None and parrafo != "":
        # proceso de integración de openai
        # Realizar la solicitud de chat completion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Asegúrate de que "gpt-4o-mini" es el modelo correcto o utiliza "gpt-4"
            messages=[
                {"role": "user", "content": "Indicame la pregunta en el siguiente párrafo. Debes encontrar la lógica del párrafo para ver la pregunta, pero solo quiero la pregunta y nada más. Ni siquiera la quiero con asteriscos para markdown. Solo la pregunta por favor: "+parrafo}
            ],
            temperature=0.7
        )
        # Imprimir la respuesta
        print(response.choices[0].message['content'])
        return (response.choices[0].message['content'])
    else:
        return "Pregunta no identificada. Para visualizar la pregunta, puede editar las características del objeto Tesis."

#Extraer la texto para resumen
def extract_objetivo(pdf_path):
    reader = PdfReader(pdf_path)
    pregunta_clave = "1.4.1 Objetivo General"
    
    # Convertir el título a minúsculas para comparación case insensitive
    pregunta_clave_lower = pregunta_clave.lower()

    # Variable para almacenar el texto extraído
    extracted_text = ""
    found_pregunta = False

    # Iterar página por página
    for page in reader.pages:
        page_text = page.extract_text()
        paragraphs = page_text.split('\n')

        for paragraph in paragraphs:
            #Buscar la palabra clave (pregunta)
            if pregunta_clave_lower in paragraph.lower():
                found_pregunta = True  # Señal de que la "pregunta" fue encontrada
                
                continue  # Pasar al siguiente párrafo para capturarlo
                
            # Si se ha encontrado la palabra clave, empezar a acumular texto
            if found_pregunta:
                # Si encontramos un párrafo vacío o un título en mayúsculas, es probable que sea el fin del texto relacionado
                if paragraph.strip() == "" or paragraph.isupper():
                    found_pregunta = False
                    break
                if '.' in paragraph:
                    extracted_text += paragraph.strip() + " "
                    break
                   
                # Acumular el texto si no parece ser un título
                extracted_text += paragraph + "\n"

    return extracted_text if extracted_text else "Pregunta no encontrada o no hay contenido relevante."

#Extraer la objetivo
def extract_texto_resumen(pdf_path):
    reader = PdfReader(pdf_path)
    pregunta_clave = "1.2	Planteamiento del Problema"
    
    # Convertir el título a minúsculas para comparación case insensitive
    pregunta_clave_lower = pregunta_clave.lower()

    # Variable para almacenar el texto extraído
    extracted_text = ""
    found_pregunta = False

    # Iterar página por página
    for page in reader.pages:
        page_text = page.extract_text()
        paragraphs = page_text.split('\n')

        for paragraph in paragraphs:
            #Buscar la palabra clave (pregunta)
            if pregunta_clave_lower in paragraph.lower():
                found_pregunta = True  # Señal de que la "pregunta" fue encontrada
                
                continue  # Pasar al siguiente párrafo para capturarlo
                
            # Si se ha encontrado la palabra clave, empezar a acumular texto
            if found_pregunta:
                # Si encontramos un párrafo vacío o un título en mayúsculas, es probable que sea el fin del texto relacionado
                if paragraph.strip() == "" or paragraph.isupper():
                    found_pregunta = False
                    break
                if '.' in paragraph:
                    extracted_text += paragraph.strip() + " "
                    break
                   
                # Acumular el texto si no parece ser un título
                extracted_text += paragraph + "\n"

    return extracted_text if extracted_text else "Pregunta no encontrada o no hay contenido relevante."



def obtener_objetivo(pdf_path):
    #pdf_path = "c:/SitioWeb/SDP_PG2/SDP_APP/media/Documentos_prueba/Sistema_Web_detector_de_plagios_de_tesis/entrega2.pdf"
    parrafo = extract_objetivo(pdf_path)
    if parrafo is not None and parrafo != "":
        # proceso de integración de openai
        # Realizar la solicitud de chat completion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Asegúrate de que "gpt-4o-mini" es el modelo correcto o utiliza "gpt-4"
            messages=[
                {"role": "user", "content": "Indicame el objetivo en el siguiente párrafo. Debes encontrar la lógica del párrafo para ver el objetivo, pero solo quiero el objetivo general y nada más. Ni siquiera la quiero con asteriscos para markdown. Solo el mero objetivo por favor: "+parrafo}
            ],
            temperature=0.7
        )
        # Imprimir la respuesta
        print(response.choices[0].message['content'])
        return (response.choices[0].message['content'])
    else:
        return "Objetivo no identificado. Para visualizar el objetivo, puede editar las características del objeto Tesis."

#Crear un resumen
def crearResumen(pdf_path):
    #pdf_path = "c:/SitioWeb/SDP_PG2/SDP_APP/media/Documentos_prueba/Sistema_Web_detector_de_plagios_de_tesis/entrega2.pdf"
    pregunta = extract_question(pdf_path)
    objetivo = extract_objetivo(pdf_path)
    problema = extract_texto_resumen(pdf_path)
    if pregunta is not None and pregunta != "" and objetivo is not None and objetivo != "" and problema is not None and problema != "":
        # proceso de integración de openai
        # Realizar la solicitud de chat completion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  #"gpt-4o-mini" es el modelo correcto o utiliza "gpt-4"
            messages=[
                {"role": "user", "content": "Crea un resumen del objetivo y pregunta. Debes encontrar la lógica del párrafo para ver la pregunta y el objetivo, pero solo quiero el resumen y nada más. Ni siquiera la quiero con asteriscos para markdown. Solo el objetivo por favor. Esta es la pregunta: " + pregunta + " y este es el objetivo: " + objetivo + "adicionalmente, este es el problema de investigación: " + problema}
            ],
            temperature=0.7
        )
        # Imprimir la respuesta
        print(response.choices[0].message['content'])
        return (response.choices[0].message['content'])
    else:
        return "Objetivo o pregunta no identificados. Para visualizar el resumen, puede editar las características del objeto Tesis."

def generarSinStopWords(pdf_path):
    #pdf_path = "c:/SitioWeb/SDP_PG2/SDP_APP/media/Documentos_prueba/Sistema_Web_detector_de_plagios_de_tesis/entrega2.pdf"
    parrafo = crearResumen(pdf_path)
    if parrafo is not None and parrafo != "":
        # proceso de integración de openai
        # Realizar la solicitud de chat completion
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Asegúrate de que "gpt-4o-mini" es el modelo correcto o utiliza "gpt-4"
            messages=[
                {"role": "user", "content": "necesito que a este texto le quites todas las tildes y las stop words en español, adicionalmente dame las palabras más importantes, debido a que para encontrar similitud de tesis quiero tener las palabras que marcan más relevancia, pero muestrame única y solamente las palabras que te pido separadas por espacios. NO QUIERO MAS QUE LAS PALABRAS: "+parrafo}
            ],
            temperature=0.7
        )
        # Imprimir la respuesta
        print(response.choices[0].message['content'])
        return (response.choices[0].message['content'])
    else:
        return "Objetivo no identificado. Para visualizar el objetivo, puede editar las características del objeto Tesis."


