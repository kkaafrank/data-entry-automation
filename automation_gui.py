import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import practice_fusion_scraper
import spreadsheet_parser
import system13_entry
from config import config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_prep_button = QPushButton("Clean and Parse Spreadsheet")
        self.pf_scraping_button = QPushButton("Get Patient Data")
        self.sys_13_entry_button = QPushButton("Enter Claims Info")

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(QLabel("Clean and Parse Spreadsheet:"))
        vertical_layout.addWidget(self.data_prep_button)
        vertical_layout.addWidget(QLabel("Get Required Patient Data from Practice Fusion:"))
        vertical_layout.addWidget(self.pf_scraping_button)
        vertical_layout.addWidget(QLabel("Enter Claims Information"))
        vertical_layout.addWidget(self.sys_13_entry_button)

        central_widget = QWidget()
        central_widget.setLayout(vertical_layout)
        self.setCentralWidget(central_widget)

        self.data_prep_button.clicked.connect(self.data_prep_button_clicked)
        self.pf_scraping_button.clicked.connect(practice_fusion_scraper.get_all_patient_data)
        self.sys_13_entry_button.clicked.connect(system13_entry.enter_all_patient_data)

    def data_prep_button_clicked(self):
        file, _ = QFileDialog.getOpenFileName(
            parent=None,
            filter="Excel Files (*.xlsx);; All Files (.*)",
            dir="./data"
        )

        spreadsheet_parser.parse_spreadsheet(file)


def main() -> int:
    application = QApplication([])
    main_window = MainWindow()
    main_window.show()

    application.exec()

    return 0

if __name__ == '__main__':
    sys.exit(main())
