import csv

from database.db import chicago_crash_db, crashes

#קריאת הקובץ והפיכת כל שורה לדיקשנרי
def read_csv(csv_path):
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

#אתחול הדאטאבייס והכנסת הפרמטרים
def init_crash_chicago():
    for row in read_csv('../data/Traffic_Crashes_-_Crashes - 20k rows.csv'):
        parameters = {
            'CRASH_RECORD_ID': row['CRASH_RECORD_ID'],
            #תאריך התאונה
            'CRASH_DATE': row['CRASH_DATE'],
            #אזור התאונה
            'BEAT_OF_OCCURRENCE': row['BEAT_OF_OCCURRENCE'],
            #סיבת התאונה
            'PRIM_CONTRIBUTORY_CAUSE': row['PRIM_CONTRIBUTORY_CAUSE'],
            #סך כל הפציעות
            'INJURIES_TOTAL': row['INJURIES_TOTAL'],
            #הפציעה החמורה ביותר
            'MOST_SEVERE_INJURY': row['MOST_SEVERE_INJURY'],
            #פציעות קטלניות
            'INJURIES_FATAL': row['INJURIES_FATAL'],
            #פציעות שמונעות תפקוד
            'INJURIES_INCAPACITATING': row['INJURIES_INCAPACITATING'],
            #פציעות שאינן מונעות תפקוד
            'INJURIES_NON_INCAPACITATING': row['INJURIES_NON_INCAPACITATING'],
            #פציעות מדווחות שאינן נראות
            'INJURIES_REPORTED_NOT_EVIDENT': row['INJURIES_REPORTED_NOT_EVIDENT'],
            #פציעות ללא אינדיקציה
            'INJURIES_NO_INDICATION': row['INJURIES_NO_INDICATION'],
            #פציעות לא ידועות
            'INJURIES_UNKNOWN': row['INJURIES_UNKNOWN']
        }
        crashes.insert_one(parameters)