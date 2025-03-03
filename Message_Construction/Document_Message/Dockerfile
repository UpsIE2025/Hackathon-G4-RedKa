# Usar una imagen oficial de Node.js como base
FROM node:18

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de package.json y package-lock.json para instalar dependencias primero
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código fuente
COPY . .

# Exponer el puerto para recibir peticiones HTTP
EXPOSE 3000

# Definir la variable de entorno
ENV NODE_ENV=production

# Comando por defecto al ejecutar el contenedor
CMD ["npm", "start"]
