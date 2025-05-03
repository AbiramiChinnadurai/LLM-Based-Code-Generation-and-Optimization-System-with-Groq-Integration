# Use an official Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the local project files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install streamlit -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 5000

# Make sure the script has execute permissions inside the container
RUN chmod +x /app/start.sh

# Use CMD instead of ENTRYPOINT for flexibility
CMD ["/bin/bash", "/app/start.sh"]
