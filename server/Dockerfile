    # install and update python
    FROM python:3.12.0-slim-bookworm

    # set some python related variables
    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1

    # may be adding a base image, not sure
    ENV APP=/app

    # Change the workdir
    WORKDIR $APP

    # Install the requirements
    COPY requirements.txt $APP
    RUN pip3 install -r requirements.txt

    # Copy the rest of the files
    COPY . $APP

    # expose port
    EXPOSE 8000

    # run command to start the application?
    RUN chmod +x /app/entrypoint.sh
    ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
