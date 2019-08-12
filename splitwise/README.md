# Splitwise function
This function adds the transaction to Splitwise.

## Setup:
1. Update `SPLITWISE_GROUP_NAME` in the `Makefile`
1. Add a file called secrets.py with contents:
   ```
   SPLITWISE_CONSUMER_KEY = "<splitwise consumer key>"
   SPLITWISE_CONSUMER_SECRET = "<splitwise consumer secret>"
   ```
1. `make deploy-function-splitwise `
