PROJECT_ID=auditor-219503
UID=$(shell id -u)
GID=$(shell id -g)


deploy-function-email:
	docker run -it --rm \
		-v $(PWD)/email:/auditor/functions/email \
		--env=PROJECT_ID=$(PROJECT_ID) \
		-w /auditor/functions/email \
		jchorl/appengine-python:latest \
		sh -c "echo \"gcloud auth login\ngcloud beta functions deploy email_post --set-env-vars EMAIL_ADDRESS=jchorlton+auditor@gmail.com --trigger-http --runtime python37\" && \
		bash"

deploy-function-splitwise:
	docker run -it --rm \
		-v $(PWD)/splitwise:/auditor/functions/splitwise \
		--env=PROJECT_ID=$(PROJECT_ID) \
		-w /auditor/functions/splitwise \
		jchorl/appengine-python:latest \
		sh -c "echo \"gcloud auth login\ngcloud beta functions deploy handle_charge --set-env-vars SPLITWISE_GROUP_NAME='404 Not Found' --trigger-http --runtime python37\" && \
		bash"

deploy-function-sheets:
	docker run -it --rm \
		-v $(PWD)/sheets:/auditor/functions/sheets \
		--env=PROJECT_ID=$(PROJECT_ID) \
		-w /auditor/functions/sheets \
		jchorl/appengine-python:latest \
		sh -c "echo \"gcloud auth login\ngcloud beta functions deploy process_transaction --set-env-vars FINANCE_SPREADSHEET_ID='1yiHbSLDIIYPZPJrgfSnpJZKelaQ3CFVE9bFPs77MMAI',TEMPLATE_SHEET_ID='525329997' --trigger-http --runtime python37\" && \
		bash"
