FROM python:3.8-alpine

# Install requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy Source
COPY cli.py cli.py
COPY color_treatment.py color_treatment.py
COPY openhab_lib.py openhab_lib.py
COPY purple.py purple.py
COPY airlamp.sh airlamp.sh


CMD ./airlamp.sh
