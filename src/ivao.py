"""
ivao.py

- Integrates with Ivao Aurora software sending signals to main window to update ui and run work
"""

import socket
from PySide6.QtCore import QObject, Signal, QTimer

from checks import check_sid, check_semicircular_rule, check_route, check_fl
from models import CheckResult, CheckStatus, Aircraft
from data import airports, srd, aircraft_aeroplanes, aircraft_rotorcraft


class IvaoWorker(QObject):
    """IVAO worker class, runs aurora client interface"""

    sig_aircraft: Signal = Signal(object)
    sig_aurora_connection: Signal = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.s = None
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(1_000)
        self.timer.timeout.connect(self.get_selected_aircraft)

    def connect_to_ivao(self) -> None:
        """Connects to IVAO Aurora Software"""
        try:
            self.timer.stop()
            self.s = socket.create_connection(("127.0.0.1", 1130))
            self.timer.start()
            self.sig_aurora_connection.emit(True)
        except ConnectionRefusedError:
            self.sig_aurora_connection.emit(False)

    def get_selected_aircraft(self) -> None:
        """Fetch selected aircraft from Aurora Software and run FPL checks"""

        if self.s is None:
            return

        # send message
        try:
            self.s.sendall(b"#SELTFC\r\n")
            response = self.s.recv(4096).decode()
        except ConnectionAbortedError:
            self.timer.stop()
            self.sig_aurora_connection.emit(False)
            return


        callsign = response.split(";")[1]

        if not callsign:
            return

        # fetch flight plan
        self.s.sendall(f"#FP;{callsign}\r\n".encode())
        fp_plan_data = self.s.recv(4096).decode().split(";")

        if len(fp_plan_data) != 18: # check data field are all included
            return

        # check aircraft is ifr
        flight_rules = fp_plan_data[8]

        departure_icao = fp_plan_data[2]
        arrival_icao = fp_plan_data[3]
        aircraft_type = fp_plan_data[6]
        wake_cat = fp_plan_data[7]

        if fp_plan_data[11] == "VFR":
            fl = 0
        else:
            fl = int(fp_plan_data[11][1:])

        route = fp_plan_data[15]

        # fetch dep/arr names
        airport_data_dep = airports[airports["icao_code"] == departure_icao].iloc[0]
        airport_data_arr = airports[airports["icao_code"] == arrival_icao].iloc[0]

        departure_name = f"{airport_data_dep["name"]} ({airport_data_dep["municipality"]})"
        arrival_name = f"{airport_data_arr["name"]} ({airport_data_arr["municipality"]})"

        # fetch aircraft name and CAA wake cat
        if aircraft_type in aircraft_aeroplanes["ICAO Type Designator"].values:
            aircraft = aircraft_aeroplanes[aircraft_aeroplanes["ICAO Type Designator"] == aircraft_type].iloc[0]
            aircraft_name = f"{aircraft["Manufacturer"]} - {aircraft["Model"]}"
            wake_cat_dep_caa = aircraft["UK Departure WTC"]
            wake_cap_arr_caa = aircraft["UK Arrival WTC"]

        elif aircraft_type in aircraft_rotorcraft["ICAO Type Designator"].values:
            aircraft = aircraft_rotorcraft[aircraft_rotorcraft["ICAO Type Designator"] == aircraft_type].iloc[0]
            aircraft_name = f"{aircraft["Manufacturer"] - aircraft["Model"]}"
            wake_cat_dep_caa = aircraft["UK Departure WTC"]
            wake_cap_arr_caa = aircraft["UK Arrival WTC"]

        else:
            aircraft_name = None
            wake_cat_dep_caa = None
            wake_cap_arr_caa = None

        if flight_rules == "I":
            # run checks
            result_semicircular_rule = check_semicircular_rule(departure_icao, arrival_icao, fl)

            result_sid = check_sid(departure_icao, route)

            if result_sid.details and result_sid.details.sid:
                result_srd = check_route(departure_icao, arrival_icao, route, result_sid.details.sid)
            else:
                result_srd = check_route(departure_icao, arrival_icao, route)

            if result_srd.details is not None and result_srd.details.verified_route is not None:
                result_fl_srd = check_fl(fl, result_srd.details.routes[result_srd.details.verified_route])
            else:
                result_fl_srd = CheckResult(
                    CheckStatus.NA,
                    "No identified SRD route, so FL restrictions not determined"
                )

            checks = {
                "Semi-Circular Rule": result_semicircular_rule,
                "SID": result_sid,
                "SRD Route": result_srd,
                "SRD FL": result_fl_srd
            }
        else:
            checks = {}

        # package information into Aircraft data
        aircraft = Aircraft(
            callsign=callsign,
            route=route,
            fl=fl,
            aircraft_type=aircraft_type,
            aircraft_name=aircraft_name,
            wake_cat=wake_cat,
            wake_cat_dep_caa=wake_cat_dep_caa,
            wake_cat_arr_caa=wake_cap_arr_caa,
            dep=departure_icao,
            arr=arrival_icao,
            dep_name=departure_name,
            arr_name=arrival_name,
            checks=checks
        )

        self.sig_aircraft.emit(aircraft)

