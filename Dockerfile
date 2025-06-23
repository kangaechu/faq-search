FROM public.ecr.aws/lambda/python:3

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY *.py ${LAMBDA_TASK_ROOT}
COPY data/index ${LAMBDA_TASK_ROOT}/data/index

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "handler.faq_qa" ]
