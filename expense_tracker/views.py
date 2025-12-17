from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QDate
import typing


class TransactionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, categories: typing.List[typing.Tuple[int, str]] = None, data: dict = None):
        super().__init__(parent)
        self.setWindowTitle("Transaction")
        self.resize(400, 250)

        if categories is None:
            categories = []
        self.categories = categories

        layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()

        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Date:", self.date_edit)

        self.amount_spin = QtWidgets.QDoubleSpinBox()
        self.amount_spin.setRange(0.01, 1_000_000_000)
        self.amount_spin.setDecimals(2)
        form.addRow("Amount:", self.amount_spin)

        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Expense", "Income"])
        form.addRow("Type:", self.type_combo)

        self.category_combo = QtWidgets.QComboBox()
        for cid, name in self.categories:
            self.category_combo.addItem(name, cid)
        form.addRow("Category:", self.category_combo)

        self.desc_edit = QtWidgets.QLineEdit()
        form.addRow("Description:", self.desc_edit)

        layout.addLayout(form)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

        if data:
            d = QDate.fromString(data.get("date"), "yyyy-MM-dd")
            if d.isValid():
                self.date_edit.setDate(d)
            self.amount_spin.setValue(float(data.get("amount", 0)))
            t = data.get("type", "Expense")
            idx = self.type_combo.findText(t)
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
            cat_id = data.get("category_id")
            if cat_id is not None:
                i = self.category_combo.findData(cat_id)
                if i >= 0:
                    self.category_combo.setCurrentIndex(i)
            self.desc_edit.setText(data.get("description") or "")

    def get_data(self):
        date = self.date_edit.date().toString("yyyy-MM-dd")
        amount = self.amount_spin.value()
        t_type = self.type_combo.currentText()
        cat_id = self.category_combo.currentData()
        desc = self.desc_edit.text().strip()
        return {"date": date, "amount": amount, "type": t_type, "category_id": cat_id, "description": desc}


class CategoryDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, name: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Category")
        self.resize(300, 100)

        layout = QtWidgets.QVBoxLayout(self)
        form = QtWidgets.QFormLayout()
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setText(name)
        form.addRow("Name:", self.name_edit)
        layout.addLayout(form)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_name(self):
        return self.name_edit.text().strip()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finly — Minimal, private finance tracking.")
        self.resize(900, 600)

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        top_h = QtWidgets.QHBoxLayout()
        self.prev_month_btn = QtWidgets.QPushButton("◀")
        self.next_month_btn = QtWidgets.QPushButton("▶")
        self.month_label = QtWidgets.QLabel()
        font = self.month_label.font()
        font.setPointSize(12)
        self.month_label.setFont(font)
        top_h.addWidget(self.prev_month_btn)
        top_h.addWidget(self.month_label)
        top_h.addWidget(self.next_month_btn)
        top_h.addStretch()

        self.income_label = QtWidgets.QLabel("Income: 0.00")
        self.expense_label = QtWidgets.QLabel("Expenses: 0.00")
        self.balance_label = QtWidgets.QLabel("Balance: 0.00")
        top_h.addWidget(self.income_label)
        top_h.addWidget(self.expense_label)
        top_h.addWidget(self.balance_label)

        layout.addLayout(top_h)

        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Amount", "Type", "Category", "Description"]) 
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.hideColumn(0)
        layout.addWidget(self.table)

        btn_h = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Add")
        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.delete_btn = QtWidgets.QPushButton("Delete")
        self.manage_cats_btn = QtWidgets.QPushButton("Manage Categories")
        self.export_btn = QtWidgets.QPushButton("Export CSV")
        btn_h.addWidget(self.add_btn)
        btn_h.addWidget(self.edit_btn)
        btn_h.addWidget(self.delete_btn)
        btn_h.addStretch()
        btn_h.addWidget(self.manage_cats_btn)
        btn_h.addWidget(self.export_btn)
        layout.addLayout(btn_h)

        self.status = self.statusBar()

        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        self.about_action = QtGui.QAction("About Finly", self)
        help_menu.addAction(self.about_action)

        today = QtCore.QDate.currentDate()
        self.current_year = today.year()
        self.current_month = today.month()
        self.update_month_label()

    def update_month_label(self):
        dt = QtCore.QDate(self.current_year, self.current_month, 1)
        self.month_label.setText(dt.toString("MMMM yyyy"))


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Finly")
        self.resize(480, 300)

        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("<h2>Finly</h2>")
        subtitle = QtWidgets.QLabel("<i>Minimal, private finance tracking.</i>")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        mission = QtWidgets.QLabel(
            "Finly provides a simple, transparent, and fully offline way to track personal income and expenses while giving users complete ownership of their financial data."
        )
        mission.setWordWrap(True)
        layout.addWidget(mission)

        values = QtWidgets.QLabel("<b>Core values:</b> Privacy-first, simplicity, ownership, transparency, reliability")
        values.setWordWrap(True)
        layout.addWidget(values)

        layout.addStretch()

        info = QtWidgets.QLabel(
            "Creator: Maloth Harsha<br>Role: Creator (Student, beginner developer)<br>GitHub: <a href=\"https://github.com/harsha-maloth\">harsha-maloth</a>"
        )
        info.setOpenExternalLinks(True)
        info.setWordWrap(True)
        layout.addWidget(info)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        btns.accepted.connect(self.accept)
        layout.addWidget(btns)
