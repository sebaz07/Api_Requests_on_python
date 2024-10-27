from Api_Groups.apis_group3 import api_list as api_group3
from Api_Groups.apis_group2 import api_list as api_group2
from Api_Groups.apis_group1 import api_list as api_group1
from prometheus_client import start_http_server, Summary, Gauge, Counter
import requests
import time
import certifi
import urllib3
from requests.exceptions import Timeout, RequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Importar las listas de APIs desde los archivos

# Configuración de métricas de Prometheus
REQUEST_TIME = Summary('api_request_duration_seconds',
                       'Time spent processing API requests')
REQUEST_STATUS = Gauge('api_request_status',
                       'Status of the API request', ['api'])
RESPONSE_TIME_BY_ENDPOINT = Gauge(
    'api_response_time_by_endpoint_seconds', 'Average response time of each API endpoint', ['api'])
# Contador para total de consumos
TOTAL_API_CALLS = Counter('total_api_calls', 'Total number of API calls made')

# Diccionario para manejar los grupos de APIs
api_groups = {
    "group1": api_group1,
    "group2": api_group2,
    "group3": api_group3
}

# Función para validar las APIs de cada grupo


@REQUEST_TIME.time()
def validate_apis(api_group_name, api_list):
    for api in api_list:
        start_time = time.time()
        try:
            response = requests.get(api, verify=False, timeout=120)
            end_time = time.time()
            response_time = end_time - start_time
            status_code = response.status_code
            REQUEST_STATUS.labels(api=api).set(status_code)
            RESPONSE_TIME_BY_ENDPOINT.labels(api=api).set(response_time)

            # Incrementar el contador total de llamadas
            TOTAL_API_CALLS.inc()

            # Validar todos los códigos de estado
            if 200 <= status_code < 300:
                print(f"{api_group_name} - API: {api} - Status: Success ({
                      status_code}) - Response Time: {response_time:.2f} seconds")
            elif 300 <= status_code < 400:
                print(f"{api_group_name} - API: {api} - Status: Redirection ({
                      status_code}) - Response Time: {response_time:.2f} seconds")
            elif 400 <= status_code < 500:
                print(f"{api_group_name} - API: {api} - Status: Client Error ({
                      status_code}) - Response Time: {response_time:.2f} seconds")
            elif 500 <= status_code < 600:
                print(f"{api_group_name} - API: {api} - Status: Server Error ({
                      status_code}) - Response Time: {response_time:.2f} seconds")
            else:
                print(f"{api_group_name} - API: {api} - Status: Unknown ({
                      status_code}) - Response Time: {response_time:.2f} seconds")

        except requests.exceptions.RequestException as e:
            end_time = time.time()
            REQUEST_STATUS.labels(api=api).set(-1)  # -1 para indicar fallo
            print(f"{api_group_name} - API: {api} - Status: Failed - Error: {str(e)
                                                                             } - Response Time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    # Exponer métricas en el puerto 8000
    start_http_server(8000)
    while True:
        for group_name, apis in api_groups.items():
            validate_apis(group_name, apis)
        time.sleep(10)  # Ejecutar cada 10 segundos
