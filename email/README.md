# Email function
This function just emails the webhook body in json form using Sparkpost.

## Setup:
1. Add a file called secrets.py with contents:
   ```
   SPARKPOST_API_KEY = "<api key>"
   ```
1. Update the `EMAIL_ADDRESS` in the `Makefile`
1. `make deploy-function-email `
