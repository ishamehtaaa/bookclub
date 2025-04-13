FROM node:18-alpine
WORKDIR /app
# Copy package.json and package-lock.json
COPY package*.json ./
# Install dependencies
RUN npm install
# Copy the rest of the application
COPY . .
# Expose the port Parcel runs on
EXPOSE 1234
CMD ["npm", "build"]
