# syntax=docker/dockerfile:1.4

FROM node:16 as build

WORKDIR /app

# Install dependencies
RUN npm install -g http-server nodemon codemirror

# Copy the frontend source code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Run the application.
CMD ["npx", "nodemon", "--watch", ".", "--exec", "http-server", "-p", "8080"]
