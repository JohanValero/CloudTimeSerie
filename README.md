# Cloud Time Serie

- Se utilizó la nube de GCP para integrar un modelo predictivo de series de tiempo en un Dashboard.
- Se utilizó la herramienta de "Secret Managenement" de GCP para ocultar los datos de conexión de base de datos y valores críticos.
- Se utilizó la hermanienta de "Cloud Run" para publicar el microservicio en la nube de forma serverless.
- Se utilizó la herramienta de "Cloud Build" para generar un despliegue continuo de creación, automatización de los pull request antes de publicarse definitivamente.
- Se utilizó la herramienta de "Cloud Storage" para guardar el modelo predictivo entrenado para siempre retornar los mismos resultados para un modelo predictivo.

Dataset original utilizado como fuente del modelo predictivo:
* https://drive.google.com/file/d/1tI7DOx57sF1MwhNGTyx9IImKX-pxqm9S/view

Guia original utilizada para la predicción en series de tiempo:
* https://www.section.io/engineering-education/anomaly-detection-model-on-time-series-data-using-isolation-forest/

Visualización del dataset:
* https://timeserie.grafana.net/dashboard/snapshot/JBuwq2aMyGJ574G7E7f4lmS1RvkNTXjk

Visualización del modelo predictivo:
* https://timeserie.grafana.net/dashboard/snapshot/jw3Rvc4VnAHo8kt1y8QrxW4AFvakLd1J

###CI/CD diagrama de despliegue.                    
```seq
GitHub->Cloud Build: Pull request.
Cloud Build->Secret Management: request database connections.
Secret Management->Cloud Build: Enviroments variables returned.
Cloud Build->Artifact registry: Save the container.
Cloud Build->Cloud run: Deploy the micro-service.
Artifact registry-->Cloud run: get the image container
Cloud run->Cloud Build: Deploy OK.
Cloud Build->GitHub: Pull request OK.
```

###Funcionamiento del mircroservicio.
```seq
Grafana->GCP: Retorname las anomalias\nde la serie de tiempo.
GCP->Cloud Run: Ejecutar microservicio.
Cloud Run->Data Base: Obtener serie de tiempo.
Cloud Run->Cloud Storage: Obtener modelo predictivo.
Note right of Cloud Run: Ejecuta el\nmodelo predictivo. 
Cloud Run->Grafana: Retorna las anomalias en la serie de tiempo.
```