import requests
import time
from colorama import Fore, Back, Style, init
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import Timeout, HTTPError, RequestException

# Importar listas de APIs desde los archivos
from Api_Groups.apis_group1 import api_list as api_group1
from Api_Groups.apis_group2 import api_list as api_group2
from Api_Groups.apis_group3 import api_list as api_group3

# Suprimir advertencias de solicitudes inseguras
urllib3.disable_warnings(InsecureRequestWarning)

# Inicializa Colorama
init(autoreset=True)

print(Back.GREEN + 'INICIO DEL CONSUMO DE APIs')

# Diccionario que agrupa los grupos de APIs importados
api_groups = {
    "Group 1": api_group1,
    "Group 2": api_group2,
    "Group 3": api_group3
}

# Función para validar las APIs de cada grupo


def validate_apis(api_group_name, api_list):
    results = []
    for api in api_list:
        start_time = time.time()  # Tiempo de inicio
        try:
            # Hacer la solicitud con un tiempo máximo de espera
            # Timeout de 10 segundos
            response = requests.get(api, verify=False, timeout=10)
            end_time = time.time()  # Tiempo de fin
            response_time = end_time - start_time  # Tiempo de respuesta
            status_code = response.status_code

            # Manejo detallado de códigos HTTP
            if 200 <= status_code < 300:
                result = {
                    "API": api,
                    "Status": status_code,
                    "Result": "Success",
                    "Response Time (s)": response_time
                }
            elif 400 <= status_code < 500:
                result = {
                    "API": api,
                    "Status": status_code,
                    "Result": "Client Error",
                    "Response Time (s)": response_time
                }
            elif 500 <= status_code < 600:
                result = {
                    "API": api,
                    "Status": status_code,
                    "Result": "Server Error",
                    "Response Time (s)": response_time
                }
            else:
                result = {
                    "API": api,
                    "Status": status_code,
                    "Result": "Unexpected Status",
                    "Response Time (s)": response_time
                }

        except Timeout:
            end_time = time.time()  # Tiempo de fin
            response_time = end_time - start_time  # Tiempo de respuesta
            result = {
                "API": api,
                "Status": "N/A",
                "Result": "Timeout",
                "Error": "The request timed out",
                "Response Time (s)": response_time
            }
        except HTTPError as http_err:
            end_time = time.time()
            response_time = end_time - start_time
            result = {
                "API": api,
                "Status": "N/A",
                "Result": "HTTP Error",
                "Error": str(http_err),
                "Response Time (s)": response_time
            }
        except RequestException as req_err:
            end_time = time.time()
            response_time = end_time - start_time
            result = {
                "API": api,
                "Status": "N/A",
                "Result": "Failed",
                "Error": str(req_err),
                "Response Time (s)": response_time
            }

        results.append(result)

    print_results(api_group_name, results)

# Imprimir los resultados organizadamente


def print_results(api_group_name, results):
    print(f"\nValidation Results for {api_group_name}:\n")
    for result in results:
        print(Fore.GREEN + f"API: {result['API']}")
        print(Style.BRIGHT + f"  Status Code: {result['Status']}")
        if result['Result'] == "Success":
            print(Fore.CYAN + f"  Result: {result['Result']}")
        elif result['Result'] == "Client Error":
            print(Back.YELLOW + Fore.BLACK + f"  Result: {result['Result']}")
        elif result['Result'] == "Server Error":
            print(Back.RED + Fore.WHITE + f"  Result: {result['Result']}")
        else:
            print(Back.RED + Fore.WHITE + f"  Result: {result['Result']}")
        print(Fore.YELLOW +
              f"  Response Time(s): {result['Response Time (s)']:.4f}")
        if 'Error' in result:
            print(Back.RED + Fore.WHITE + f"  Error: {result['Error']}")
        print(Style.RESET_ALL + "-" * 40)


# Validar APIs de todos los grupos y mostrar resultados
if __name__ == "__main__":
    for group_name, api_list in api_groups.items():
        validate_apis(group_name, api_list)

print(Back.GREEN + 'FIN DEL CONSUMO DE APIs')
