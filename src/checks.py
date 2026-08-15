"""
checks.py

Implements flight plan checks for SIDs, Semi-circular rule, SRD compliance and FL compliance

"""

import re

import numpy as np
import pandas as pd

from models import CheckResult, SidCheckDetails, SrdCheckDetails, FlCheckDetails, CheckStatus
from srd import srd, srd_notes, airports

"""Helper functions"""
def route_has_notes(route_idx) -> bool:
    """Checks if route in SRD has any appended notes to warn user

    Args:
        route_idx: index of the route in the SRD

    Returns:
        boolean - True if notes are present, False if notes are not

    """

    if route_idx < len(srd):
        route = srd.iloc[route_idx].fillna("")
        remarks = route["Remarks"]

        if remarks:
            return True

    return False


def fetch_notes(remarks: str) -> list[int]:
    """Passes remarks string in srd to work out the corresponding notes number required

    Args:
        remarks: str

    Returns:
        list of note numbers
    """

    tokens = remarks.split(":", 1)

    if len(tokens) < 2:
        return []

    notes_numbers_str = tokens[1]
    notes_numbers = [int(n.strip()) for n in notes_numbers_str.split("-")]
    return notes_numbers


def fetch_note(note_number: int) -> tuple[int, str, str] | None:
    """Fetch note, retrieves note from note number

    Args:
        note_number: int corresponding to note idenitifer in SRD

    Returns:
        tuple of note number, title and text
        if no note can be found it returns None
    """

    notes = srd_notes[srd_notes["Number"] == note_number]

    if len(notes) == 0:
        return None

    note = notes.iloc[0]

    return note["Number"], note["Title"], note["Text"]

def fetch_route(route_idx: int) -> pd.DataFrame | None:
    """Fetches route from index

    Args:
        route_idx: int corresponding to route id

    Returns:
        Dataframe with route data, returns None if idx not valid
    """

    if route_idx < len(srd):
        return srd.iloc[route_idx]
    else:
        return None

"""SID CHECK"""
def identify_sid(sids: list[str], fpl: str) -> str | None:
    """Identifies if possible instrument departures are in fpl

    Args:
        sids: list of possible sid idenitifers for the airport
        fpl: string containing the fixes/airways to be followed by the aircraft

    Return:
        string corresponding to the first SID identifier found

    """

    tokens = fpl.split(" ")

    for token in tokens:
        for sid in sids:
            if sid in token:
                return sid

    return None


def check_sid(dep: str, fpl: str) -> CheckResult:
    """Checks if filed standard instrument departure is present/valid and raises warnings if any notes pertain to the sid

    Args:
        dep: four letter icao airport identifier
        fpl: string containing the fixes/airways to be followed by the aircraft

    Return:
        CheckResult with details completed by the SidCheckDetails dataclass
        if there are no sids for the airport then the system will return a NA (not applicable)
        if sid is valid and has no notes test status will pass
        if sid is valid and contains notes test status will warn
        if sid is not valid (i.e no sid filed) test status will fail
        in the case sid is valid and has no notes or sid is not valid notes will be left as an empty array

    """

    dep_routes = srd[srd["ADEP/Entry"] == dep]
    sids = list(np.unique(dep_routes["SID"].dropna()))

    if len(sids) == 0:
        return CheckResult(
            CheckStatus.NA,
            f"No SIDS found for departure airport {dep}"
        )

    filed_sid = identify_sid(sids, fpl)

    if filed_sid is None:  # sid not filed correctly
        return CheckResult(
            CheckStatus.FAIL,
            "No valid sid identified from fpl"
        )

    # fetch possible notes pertaining to the airfield (tackles EGNX note 227 BPK SID)
    notes_nos_for_airport = []

    routes_for_airport = srd[srd["ADEP/Entry"] == dep].fillna("")

    for r_idx in range(len(routes_for_airport)):
        note_nos_for_route = fetch_notes(routes_for_airport["Remarks"].iloc[r_idx])
        notes_nos_for_airport += note_nos_for_route

    notes_nos_for_airports_aux = list(set(notes_nos_for_airport))
    notes_nos_for_sid = []

    # search for notes containing SID and the filed SID
    for note_idx in notes_nos_for_airports_aux:

        note = fetch_note(note_idx)

        if not note: # ignore non-existing notes
            continue

        no, title, description = note

        if "SID" in title or filed_sid in title or filed_sid in description:
            notes_nos_for_sid.append(no)

    if len(notes_nos_for_sid) == 0:  # sid found with no notes
        return CheckResult(
            CheckStatus.PASS,
            "SID valid with no warnings",
            SidCheckDetails(
                filed_sid,
                []
            )
        )
    else:
        return CheckResult(
            CheckStatus.WARNING,
            "SID valid with warnings",
            SidCheckDetails(
                filed_sid,
                notes_nos_for_sid
            )
        )


"""SEMI-CIRCULAR RULE CHECK"""


def get_airport_lat_lon(airport_icao: str) -> tuple[float, float] | None:
    """Fetches airports latitude and longitude coordinates

    Args:
        airport_icao: four letter airport icao identifier

    Return:
        tuple of latitude and longitude, if airport not found returns None

    """

    airport_data = airports[airports["icao_code"] == airport_icao]

    if len(airport_data) == 0:
        return None

    lat = airport_data["latitude_deg"].iloc[0]
    lon = airport_data["longitude_deg"].iloc[0]

    return lat, lon


def check_semicircular_rule(dep: str, arr: str, fl: int) -> CheckResult:
    """Checks if flight planned level is complaint with semi-circular rule (even going westbound, odd going eastbound)

    Args:
        dep: four letter icao code for the departure airport
        arr: four letter icao code for the arrival airport
        fl: planned flight level

    Return:
        CheckResult result (pass if correct, fail if incorrect)
        if airport not in database then test will return NA

    """

    # TODO: simplification for long haul flights using the bearing from departure to arrival airport

    dep_coords = get_airport_lat_lon(dep)
    arr_coords = get_airport_lat_lon(arr)

    if dep_coords is None or arr_coords is None:
        return CheckResult(
            CheckStatus.NA,
            f"No airport data found for {dep}/{arr}"
        )

    dep_lat, dep_lon = dep_coords
    arr_lat, arr_lon = arr_coords

    # calculate bearing (https://www.movable-type.co.uk/scripts/latlong.html)

    dep_lat_rad = np.deg2rad(dep_lat)
    dep_lon_rad = np.deg2rad(dep_lon)
    arr_lat_rad = np.deg2rad(arr_lat)
    arr_lon_rad = np.deg2rad(arr_lon)

    y = np.sin(arr_lon_rad - dep_lon_rad) * np.cos(arr_lat_rad)
    x = np.cos(dep_lat_rad) * np.sin(arr_lat_rad) - np.sin(dep_lat_rad) * np.cos(arr_lat_rad) * np.cos(
        arr_lon_rad - dep_lon_rad)
    theta = np.atan2(y, x)

    track = np.rad2deg(theta) % 360

    # track going east - level must be odd
    if 0 <= track < 180:
        if (fl // 10) % 2 == 1:
            return CheckResult(
                CheckStatus.PASS,
                "East track on odd level"
            )
        else:
            return CheckResult(
                CheckStatus.FAIL,
                "East track on even level"
            )

    # track going west - level must be even
    else:
        if (fl // 10) % 2 == 0:
            return CheckResult(
                CheckStatus.PASS,
                "West track on even level"
            )
        else:
            return CheckResult(
                CheckStatus.FAIL,
                "West track on odd level"
            )


"""SRD CHECK"""
def check_route(dep: str, arr: str, fpl: str, ) -> CheckResult:
    """Checks if route is contained within the standard routeing documentation

    Args:
        dep: four letter airport icao code for departure airport
        arr: four letter airport icao code for arrival airport
        fpl: string containing the fixes/airways to be followed by the aircraft

    Returns:
        CheckResult containing SrdCheckDetails containing routes found, verified route if found and the reason for the status
        if no route with the specified entry exit can be found then we return warn
        if there are routes with the specified entry exit but the user has not filed one we return fail
    """

    tokens = fpl.split(" ")

    airway_pattern = re.compile(r"^[A-Z]{1,2}\d+$")

    entry_point = None
    exit_point = None

    entry_fixes = []
    exit_fixes = []

    clean_fpl = ""

    # clean fpl for srd route matching and find entry/exit points in route that match srd
    for token in tokens:
        token = token.split("/")[0]

        clean_fpl += " " + token

        if token == "DCT" or airway_pattern.match(token):
            continue

        if token in srd["ADEP/Entry"].values:
            entry_fixes.append(token)

        if token in srd["ADES/Exit"].values:
            exit_fixes.append(token)

    clean_fpl = clean_fpl.strip()

    # calculate entry/exit points for fpl

    if dep.startswith("EG") and arr.startswith("EG"):
        # flights purely within UK airpsace
        entry_point = dep
        exit_point = arr

    elif dep.startswith("EG") and len(exit_fixes) > 0:
        # flights exiting UK airspace
        entry_point = dep
        exit_point = exit_fixes[-1]

    elif arr.startswith("EG") and len(entry_fixes) > 0:
        # flight entering UK airspace
        exit_point = arr
        entry_point = entry_fixes[0]

    elif len(entry_fixes) > 0 and len(exit_fixes) > 0:
        # flight overflying uk airspace
        entry_point = entry_fixes[0]
        exit_point = exit_fixes[-1]

    if entry_point is not None and exit_point is not None:  # no entry/exit point found

        # find possible srd routing
        routes = srd.loc[(srd["ADEP/Entry"] == entry_point) & (srd["ADES/Exit"] == exit_point)]

        if len(routes) > 0:

            for i in range(len(routes)):

                # add DCT to beginning of route if not present if SID not available for dep
                if dep.startswith("EG") and pd.isna(routes["SID"].iloc[i]) and not clean_fpl.startswith("DCT"):
                    clean_fpl = "DCT " + clean_fpl

                fixes = routes["Route"].fillna("").iloc[i]

                # append entry or exit fix if not airports
                if not exit_point.startswith("EG"):
                    fixes += " " + exit_point

                if not entry_point.startswith("EG"):
                    fixes = entry_point + " " + fixes

                # split on <FRA> to account for Free route airspace
                # TODO: validate Free Route Airspace fixes
                route_sections = re.split(r"\s*<FRA>\s*", fixes.strip())

                # check if route contains all valid routing
                # TODO: this doesn't check order but likely controller will catch fpl this cursed
                route_valid = True

                for route_section in route_sections:
                    if route_section not in clean_fpl:
                        route_valid = False

                # route found
                if route_valid:

                    if not route_has_notes(routes.index[i]):  # return pass if route found and no notes
                        return CheckResult(
                            CheckStatus.PASS,
                            "Route compliant with SRD with no notes",
                            SrdCheckDetails(
                                routes.index.tolist(),
                                entry_point,
                                exit_point,
                                i,
                            )
                        )
                    else:  # return warning if route found and notes
                        return CheckResult(
                            CheckStatus.WARNING,
                            "Route complaint with SRD with notes",
                            SrdCheckDetails(
                                routes.index.tolist(),
                                entry_point,
                                exit_point,
                                i
                            )
                        )

            return CheckResult(
                CheckStatus.FAIL,
                "Route not complaint with SRD",
                SrdCheckDetails(
                    routes.index.tolist(),
                    entry_point,
                    exit_point,
                )
            )

        else:
            return CheckResult(
                CheckStatus.WARNING,
                "No routes found in SRD",
                SrdCheckDetails(
                    [],
                    entry_point,
                    exit_point
                )
            )

    return CheckResult(
        CheckStatus.WARNING,
        "Entry/exit point not identifiable"
    )

"""SRD FL Check"""
def check_fl(fl: int, route_idx: int) -> CheckResult:
    """Checks filed flight level against route restrictions

    Args:
        fl: int Filed flight level
        route_idx: int Index of the route in the srd

    Returns:
        CheckResult - pass if compliant, fail if non compliant
        Details filled with FlCheckDetails containing max and min FL (if MC set as 0)

    """

    if route_idx < len(srd):
        route = srd.iloc[route_idx].fillna("")
        min_fl = route["Min"]
        max_fl = route["Max"]

        if min_fl == "MC":
            min_fl = 0

        if fl > min_fl and fl < max_fl:
            return CheckResult(
                CheckStatus.PASS,
                "FL compliant with SRD routing",
                FlCheckDetails(
                    min_fl,
                    max_fl
                )
            )
        else:
            return CheckResult(
                CheckStatus.FAIL,
                "FL not compliant with SRD routing",
                FlCheckDetails(
                    min_fl,
                    max_fl
                )
            )

    return CheckResult(
        CheckStatus.NA,
        "SRD route not available for index"
    )
