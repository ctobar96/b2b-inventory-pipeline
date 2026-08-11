# b2b-inventory-pipeline





| Variable            | Significado                          | Tu valor           |
| ------------------- | ------------------------------------ | ------------------ |
| `POSTGRES_USER`     | Usuario de PostgreSQL                | `admin_datos`      |
| `POSTGRES_PASSWORD` | Contraseña del usuario               | `superpassword123` |
| `POSTGRES_DB`       | Base de datos inicial                | `b2b_analytics`    |
| `POSTGRES_PORT`     | Puerto expuesto en tu máquina        | `5432`             |
| `POSTGRES_HOST`     | Nombre del servidor dentro de Docker | `postgres`         |



Para evitar esto y enfocarnos solo en la Fase 3, le diremos a Docker que levante exclusivamente el servicio de la base de datos.Sigue esta secuencia exacta en tu terminal:1.Inicia PostgreSQL:Levantar solo la base de datos.Primero, entra a la carpeta de Docker y levanta específicamente el servicio postgres en segundo plano (con la bandera -d):Bashcd docker
docker-compose up -d postgres
Nota: Verás que dice "Started b2b_postgres". Docker descargará la imagen (si no la tiene) y la encenderá en segundos.2.Vuelve a la raíz del proyecto:Asegurar la ruta de ejecución.Tu orquestador principal debe ejecutarse siempre desde la carpeta principal del proyecto, así que retrocede un nivel:Bashcd ..
3.Ejecuta tu Orquestador E2E:La prueba de fuego.Ahora sí, con la base de datos esperando conexiones, lanza el pipeline completo:Bashpython -m src.main
Si toda la configuración es correcta, verás en tu terminal cómo los datos se extraen (Fase 1), se aseguran en tu Data Lake de Amazon S3 (Fase 2) y, finalmente, se limpian y se inyectan en tu base de datos local en Docker (Fase 3), finalizando con el mensaje 🎉 PIPELINE E2E COMPLETADO EXITOSAMENTE.