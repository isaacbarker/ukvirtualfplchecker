"""
main_window.py

Main window for the gui, displays Aircraft data model, when passed to slot
"""
from PySide6.QtCore import Slot, QThread, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow
from datetime import datetime as dt

from checks import fetch_note, fetch_route, fetch_notes
from ivao import IvaoWorker
from models import Aircraft, CheckStatus, SidCheckDetails, SrdCheckDetails, FlCheckDetails
from srd import get_airac_date, resource_path
from ui.main_window_ui import Ui_MainWindow

VER = "0.1.1"

def format_notes(note_idxs: list[int]) -> str:
    """Formats notes for checks

    Args:
        note_idxs (list[int]): note numbers as per SRD

    Returns:
        str: formatted notes in the format [number] [title]: [text] or if no title present: [number]: [text]
    """
    note_txt = ""

    for note_idx in note_idxs:
        note = fetch_note(note_idx)

        if note:
            no, title, text = note

            if title:
                note_txt += f"\t{no} {title}: {text}<br>"
            else:
                note_txt += f"\t{no}: {text}<br>"

    return note_txt


class MainWindow(QMainWindow, Ui_MainWindow):
    """MainWindow class

    - main ui
    - loads srd and verifies aircraft inbound from Aurora server
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowIcon(QIcon(str(resource_path("assets/icon.ico"))))

        # setup version/airac label
        airac_date = get_airac_date(dt.now())
        airac_cycle = f"{airac_date.month:02}/{airac_date.year}"
        self.version_label.setText(f"Version {VER} AIRAC {airac_cycle}")

        self.aircraft: Aircraft | None = None

        # initialise ivao connection
        self.ivao_thread: QThread = QThread()
        self.ivao_worker: IvaoWorker = IvaoWorker()
        self.ivao_worker.moveToThread(self.ivao_thread)

        # connect ivao worker signals
        self.ivao_thread.started.connect(self.ivao_worker.connect_to_ivao)
        self.ivao_worker.sig_aurora_connection.connect(self.aurora_connection)
        self.ivao_worker.sig_aircraft.connect(self.set_aircraft)

        self.reconnect_btn.clicked.connect(self.ivao_worker.connect_to_ivao)

        self.ivao_thread.start()

    @Slot(object)
    def set_aircraft(self, aircraft: Aircraft) -> None:
        """Update aircraft UI"""

        self.callsign_label.setText(aircraft.callsign)
        self.dep_label.setText(aircraft.dep_name)
        self.arr_label.setText(aircraft.arr_name)

        check_results_txt = ""

        for check in aircraft.checks.keys():
            check_result = aircraft.checks[check]

            result_text_mapping = {
                CheckStatus.PASS: '<span style="color: #2b8529">PASS</span>',
                CheckStatus.WARNING: '<span style="color: #d17d2e">WARNING</span>',
                CheckStatus.FAIL: '<span style="color: #d12e2e">FAIL</span>',
                CheckStatus.NA: '<span style="color: #efefef">NA</span>',
            }

            check_results_txt += f"{check}...{result_text_mapping[check_result.status]}<br>"
            check_results_txt += f"\t{check_result.reason}<br>"

            # load in details
            if isinstance(check_result.details, SidCheckDetails) and check_result.status != CheckStatus.PASS:
                check_results_txt += f"\tFiled SID: {check_result.details.sid}<br>"
                check_results_txt += format_notes(check_result.details.notes)

            if isinstance(check_result.details, SrdCheckDetails) and check_result.status != CheckStatus.PASS:
                check_results_txt += f"{check_result.details.entry_point} -> {check_result.details.exit_point}<br>"

                if check_result.details.verified_route is not None:
                    route = fetch_route(check_result.details.routes[check_result.details.verified_route])
                    notes = fetch_notes(route["Remarks"])
                    check_results_txt += format_notes(notes)

                elif len(check_result.details.routes) > 0:
                    check_results_txt += "SRD Alternatives: <br>"

                    for route_idx in check_result.details.routes:
                        route = fetch_route(route_idx).fillna("")
                        check_results_txt += f"{route["SID"]} {route["Route"]} {route["STAR"]}<br>"

            if isinstance(check_result.details, FlCheckDetails):
                if check_result.details.min_fl != 0:
                    check_results_txt += f"Min: F{check_result.details.min_fl:02}, Max: F{check_result.details.max_fl:02}<br>"
                else:
                    check_results_txt += f"Min: MC, Max: F{check_result.details.max_fl:02}<br>"


            check_results_txt += "<br>"
            self.check_results.setText(check_results_txt)

    @Slot()
    def aurora_connection(self, is_connected) -> None:
        """Displays aurora connected/disconnected status"""
        if is_connected:
            self.connection_label.setText("IVAO Aurora Connected")
        else:
            self.connection_label.setText("IVAO Aurora Connection Failed")
            self.connection_label.setToolTip("Please ensure 3rd party access is enabled\nRestart app when Aurora is online")
