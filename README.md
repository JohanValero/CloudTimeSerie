# Cloud Time Serie

- Se utilizó la nube de GCP para integrar un modelo predictivo de series de tiempo en un Dashboard.
- Se utilizó la herramienta de "Secret Managenement" de GCP para ocultar los datos de conexión de base de datos y valores críticos.
- Se utilizó la hermanienta de "Cloud Run" para publicar el microservicio en la nube de forma serverless.
- Se utilizó la herramienta de "Cloud Build" para generar un despliegue continuo de creación, automatización de los pull request antes de publicarse definitivamente.
- Se utilizó la herramienta de "Cloud Storage" para guardar el modelo predictivo entrenado para siempre retornar los mismos resultados para un modelo predictivo.

# Despliegue en GCP.
![](https://raw.githubusercontent.com/JohanValero/CloudTimeSerie/main/Notebook/Deploy%20diagram.png)
> CI/CD deploy diagram.

# Consumo por el Dashboard.
![](https://raw.githubusercontent.com/JohanValero/CloudTimeSerie/main/Notebook/Microservice%20diagram.png)
> Funcionamiento del mircroservicio.

# Visualización.
Visualización del dataset:
* https://timeserie.grafana.net/dashboard/snapshot/JBuwq2aMyGJ574G7E7f4lmS1RvkNTXjk

Visualización del modelo predictivo:
* https://timeserie.grafana.net/dashboard/snapshot/jw3Rvc4VnAHo8kt1y8QrxW4AFvakLd1J

# Fuentes.
Dataset original utilizado como fuente del modelo predictivo:
* https://drive.google.com/file/d/1tI7DOx57sF1MwhNGTyx9IImKX-pxqm9S/view

Guia original utilizada para la predicción en series de tiempo:
* https://www.section.io/engineering-education/anomaly-detection-model-on-time-series-data-using-isolation-forest/