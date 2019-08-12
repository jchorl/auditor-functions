# Google Sheets function
This function appends transaction data to a Google Sheet. When a new transaction comes in, it:
1. Checks to see if a sheet exists with the account name.
  * If not, it copies the sheet with ID `TEMPLATE_SHEET_ID` to a new sheet with the same name as the account.
1. Appends the transaction to the sheet

## Setup:
1. Enable the Sheets API and grab a `credentials.json` file from Google. Just follow step 1 [here](https://developers.google.com/sheets/api/quickstart/python).
1. Update `FINANCE_SPREADSHEET_ID` and `TEMPLATE_SHEET_ID` in the `Makefile`
1. `make deploy-function-sheets`
