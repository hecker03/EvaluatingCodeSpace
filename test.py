import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\Shrishailya\\Documents\\GitHub\\EvaluatingCodeSpace\\evacodespace-5bdf194cbebe.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Shriee").sheet1
