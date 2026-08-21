"""
data.py

- Loads/downloads most recent srd based on AIRAC cycle from NATS AIP
- Loads in open airports data
- Loads in and opens aircraft data

"""
import pandas as pd
from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta as td
from pathlib import Path
from urllib.request import urlopen, Request
from io import BytesIO
from zipfile import ZipFile
import sys

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent.parent


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative_path

    return APP_DIR / relative_path

URL_TEMPLATE = "https://nats-uk.ead-it.com/cms-nats/export/sites/default/en/Publications/digital-datasets/SRD/AIRAC-{month:02}-{year:02}.zip"
LOCAL_SRD_TEMPLATE = "UK and Ireland SRD_{day:02} {month_name} {year}_Excel and Notes.xlsx"
LOCAL_SRD_PATH = APP_DIR / "data" / "srds"
LOCAL_SRD_PATH.mkdir(parents=True, exist_ok=True)
AIRPORTS_DATA_PATH = resource_path("data/airports.csv")
AIRCRAFT_DATA_PATH = resource_path("data/aircrafts.xlsx")


def get_airac_date(current_dt: dt) -> dt:
    """Gets current AIRAC day/month/year
    Adapted from (https://github.com/jwkohnen/airac-java) # TODO: test cases

    Args:
        current_dt (datetime): current datetime as utc

    Returns:
        date Datetime
    """

    # convert to utc
    current_dt = current_dt.astimezone(tz=tz.utc)

    # anchor date (when cycles began at regular 28 day intervals)
    anchor_dt = dt(year=1901,
                   month=1,
                   day=10,
                   hour=0,
                   minute=0,
                   second=0,
                   microsecond=0,
                   tzinfo=tz.utc)

    cycle_duration = td(days=28)

    diff = current_dt - anchor_dt

    # integer number of cycles passed
    cycles = int(diff.total_seconds() / cycle_duration.total_seconds())

    seconds_since_last_cycle = cycle_duration.total_seconds() * cycles

    # cycle start date
    cycle_start_date = anchor_dt + td(seconds=seconds_since_last_cycle)

    return cycle_start_date

# load in srd and srd notes into dataframes for use in checks
date = get_airac_date(dt.now())
day = date.day
month = date.month
month_name = date.strftime("%B")
year = date.year

local_srd_name = LOCAL_SRD_TEMPLATE.format(day=day, month_name=month_name, year=year)
local_srd_file = LOCAL_SRD_PATH / local_srd_name

# check if file exists
if not local_srd_file.exists():
    # download as current srd not present
    url = URL_TEMPLATE.format(month=month, year=year)

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    http_response = urlopen(req)
    zip_file = ZipFile(BytesIO(http_response.read()))
    zip_file.extractall(path=LOCAL_SRD_PATH)

srd = pd.read_excel(LOCAL_SRD_PATH / local_srd_name, sheet_name="Routes")

# build notes dataframe
# load standard routing notes into df
notes_excel = pd.read_excel(LOCAL_SRD_PATH / local_srd_name, sheet_name="Notes", header=None)

current_note_no = None
current_note_title = None
current_note_txt = []

notes = []

def finalize_note():
    # if the length of text is 0 then the note actually had no title, so
    # set title to empty and treat the "title" text as the body
    if len(current_note_txt) == 0:
        text = [current_note_title]
        title = ""
    else:
        text = current_note_txt
        title = current_note_title

    notes.append({
        "Number": current_note_no,
        "Title": title,
        "Text": "\n".join(text).strip()
    })

for row in notes_excel[0].dropna():
    value = str(row).strip()

    if value.startswith("Note "):
        # start of new note or beginning of document
        if current_note_no is not None:
            finalize_note()

        current_note_no = int(value.split(" ")[1])
        current_note_title = None
        current_note_txt = []
        continue

    if current_note_title is None:
        current_note_title = value
    else:
        current_note_txt.append(value)

# flush the final note after the loop ends
if current_note_no is not None:
    finalize_note()

srd_notes = pd.DataFrame(notes)

# load in airports data
airports = pd.read_csv(AIRPORTS_DATA_PATH)

# load in aircraft data
aircraft_aeroplanes = pd.read_excel(AIRCRAFT_DATA_PATH, sheet_name="Aeroplanes")
aircraft_rotorcraft = pd.read_excel(AIRCRAFT_DATA_PATH, sheet_name="Rotorcraft")
