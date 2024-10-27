# <img src= "https://brandslogos.com/wp-content/uploads/images/large/python-logo.png" alt ="descripcion de la imagen" width= "40"> VALIDACIÓN DE APIS CON PYTHON
## Ejecucion Manual del proyecto

### 1. Creacion de entorno para proyecto python
En la carpeta donde inicie el proyecto ejecuto:
````
python -m venv Entorno
````
Luego se debe ejecutar el Entorno mediante ``Activate``

### 2. Instalacion de dependencias
Se ejecuta el comando para instalar todas las dependencias necesarias en el proyecto

````
pip install requests prometheus_client colorama
````

### 3. Ejecutar proyecto
Se inicia con el comando: 
````
python ApiConsumo.py
````

### <img src= "https://creazilla-store.fra1.digitaloceanspaces.com/icons/3254231/prometheus-icon-md.png" width= "40" style= "margin-right:0px;"> 4. Monitoreo con prometheus
- Se debe iniciar prometheus y previamente se debio haber añadido el puerto que se consume (8000) en el archivo .yml

## Lista de querys para metricas de servidor de apis con prometheus


 ### 1. Consulta del ultimo codigo de estado reportado

Muestra el ultimo codigo de estado y la hora en que fue reportado en cada API

 - `api_request_status`

  ### 2. Consulta el tiempo que tarda en procesar cada API

Muestra el tiempo que tardo la api en responder a la solicitud

 - `api_request_duration_seconds`


# <img src= "https://logopng.com.br/logos/docker-27.png" alt ="descripcion de la imagen" width= "80" style= "margin-top:40px;" > Integracion y Ejecución Con Docker & Docker Compose 

### 1. Creacion de archivo "dockerfile"
 Crear el archivo dockerfile con las especificaciones correspondientes al proyecto

````
# Usar una imagen base de Python
FROM python:3.12-slim

# Instalar dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar código de la aplicación
COPY . /app
WORKDIR /app

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["python", "ApiConsumo.py"]

````

### 2. Creacion de archivo "requirements.txt"
Se necesita crear el archivo ya que este contiene las dependencias necesarias para que el proyecto se pueda ejecutar.

````
requests
prometheus_client
certifi
urllib3
````
 ### 3. Creacion de archivo "Docker-compose.yml"
Crear el archivo de docker compose, para poder ejecutar todos los contenedores en un mismo entorno.
````
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=your_password
    volumes:
      - grafana-storage:/var/lib/grafana
  api_monitoring:
    build: .
    container_name: api_monitoring
    ports:
      - "8000:8000"
    depends_on:
      - prometheus
volumes:
  grafana-storage:
  prometheus-data:
````
 ### 4. Creacion de archivo "prometheus.yml"
 Es necesario crear este archivo para poder mapear el puerto y la ruta que utilizara ``prometheus`` para monitorear.

````
global: 
  scrape_interval: 15s 

scrape_configs: 
  - job_name: 'api_monitoring' 
    static_configs: 
      - targets: ['api_monitoring:8000']

  - job_name: 'prometheus' 
    static_configs: 
      - targets: ['prometheus:9090']
````

 ### 5. Creacion de la imagen del proyecto con Docker ``(Opcional)``
 Luego de tener todos los archivos creados y entrelazados respectivamente, se ejecuta el siguiente comando para ejecutar el ``"dockerfile"`` y crear la imagen del proyecto

 *(Este comando crea una imagen individual para poder ejecutar el proyecto, el archivo docker-compose crea automaticamente la imagen sin necesidad de este punto.)*

 - el comando debe ser ejecutado en la ruta donde se encuentra el archivo ``dockerfile``

````
docker build -t my-api-monitoring-project .
````

 ### 6. Construccion de contenedores con Docker Compose ``(Obligatorio)``
 ya al tener los archivos de docker correctamente configurados, se puede ejecutar Docker Compose para Crear los contenedores y la imagen automaticamente.
- para iniciar la construcción se ejecuta el siguiente comando, y ``se debe ejecutar desde la raiz donde se encuentren todos los documentos.``

 ````
 docker-compose up --build  
 
(Si la imagen ya esta construida se puede saltar "--build")
 ```` 

 ### 7. Verificación de Ejecución

 Al verificar en docker, los servicios de las aplicaciónes se estan ejecutando en el grupo de contenedores ``consumoapisproject``. 

<img src= "images\succesfull_image.png"> 

````mermaid
journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me