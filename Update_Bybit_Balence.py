import config
from googleapiclient.discovery import build
from google.oauth2 import service_account
import schedule
import time
import datetime
import bybit
import requests


# Telegram Funtion
def send_tele_msg(msg):
    base_url = f'https://api.telegram.org/bot2031005847:AAGAs94VzLbg9msKGCun79VxR0xTKcybLug/sendMessage?chat_id=-678853724&text="{msg}"'
    requests.get(base_url)

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
    
    balance = client.Wallet.Wallet_getBalance(coin="BTC").result()
    gs_total_BTC_balance = [[(balance[0]['result']['BTC']['wallet_balance'])]]
    total_B = balance[0]['result']['BTC']['wallet_balance']

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Main!J1").execute()
    old_B = result.get('values')
    old_B = old_B[0][0]
    old_B = float(old_B)
    
    if total_B > old_B or total_B < old_B:
        now = datetime.datetime.now()
        request = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range="Main!J1", valueInputOption="USER_ENTERED", body={"values":gs_total_BTC_balance}).execute()
        message = f"Updated Balance to ({total_B}) at {now.strftime('%y-%m-%d  (%H:%M:%S)')}"
        print(message)
        send_tele_msg(message)

schedule.every(60).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
