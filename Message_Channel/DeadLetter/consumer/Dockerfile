# Etapa de construcción
FROM maven:3.9-amazoncorretto-21 AS build
WORKDIR /app

# Copiamos el proyecto completo
COPY pom.xml ./pom.xml
COPY src ./src


# Empaquetamos la aplicación
RUN mvn package -DskipTests

# Etapa de ejecución
FROM amazoncorretto:21-alpine



WORKDIR /app

# Copiamos todo el directorio quarkus-app
COPY --from=build /app/target/quarkus-app/ /app/


EXPOSE 8081
ENTRYPOINT ["java", "-jar", "quarkus-run.jar"]
