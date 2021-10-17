import config
from googleapiclient.discovery import build
from google.oauth2 import service_account
import schedule
import time
import datetime
import bybit
# Google Sheets Funtion-------------------------------------------------------
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# Sheet ID
SPREADSHEET_ID = '1gMiz39qcZ835PLu4Ov3G0ts-Y8r1HwacfxEMJSEESu0'
service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

# Bybit API
client = bybit.bybit(test=False, api_key=config.BYBIT_API_KEY, api_secret=config.BYBIT_SECERET)

print('Running...')
def job():
    print("Updating Balance...")
    # Ready to send to Google Sheets
    balance = client.Wallet.Wallet_getBalance(coin="BTC").result()
    balance_data_limit = balance[0]['rate_limit_status']
    #balance_request = 
    print(f'Remaining Balance Requests {balance_data_limit}/120')
    total_BTC_balance = [[(balance[0]['result']['BTC']['wallet_balance'])]]
    total_B = balance[0]['result']['BTC']['wallet_balance']
    request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="Main!J1", valueInputOption="USER_ENTERED", body={"values":total_BTC_balance}).execute()
    now = datetime.datetime.now()
    print(f"Updated Balance to ({total_B}) at {now.strftime('%y-%m-%d %H:%M:%S')}")

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)