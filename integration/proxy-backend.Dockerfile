FROM node:18-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY proxy-backend-package.json ./package.json
RUN npm install

# Copy application code
COPY proxy-backend.js ./

# Expose the API port
EXPOSE 3000

# Command to run the API
CMD ["npm", "start"] 