# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install the required packages
RUN pip install jupyter ipynbname requests python-dotenv zipfile36 pathlib

# Install the new app 
RUN pip install -i https://test.pypi.org/simple/ notebook-gpt --upgrade 

# Copy the Jupyter notebook files to the container
COPY . .

# Expose the Jupyter notebook port
EXPOSE 8888

# Start the Jupyter notebook server
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
