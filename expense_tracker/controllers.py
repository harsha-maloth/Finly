from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from .models import Database
from .views import MainWindow, TransactionDialog, CategoryDialog
import os


class Controller:
    def __init__(self, app: QtWidgets.QApplication):
        self.app = app
        self.db = Database()
        self.window = MainWindow()
        self._connect_signals()
        self.refresh()

    def _connect_signals(self):
        w = self.window
        w.add_btn.clicked.connect(self.add_transaction)
        w.edit_btn.clicked.connect(self.edit_transaction)
        w.delete_btn.clicked.connect(self.delete_transaction)
        w.manage_cats_btn.clicked.connect(self.manage_categories)
        w.export_btn.clicked.connect(self.export_csv)
        w.prev_month_btn.clicked.connect(self.prev_month)
        w.next_month_btn.clicked.connect(self.next_month)
        try:
            w.about_action.triggered.connect(self.show_about)
        except Exception:
            pass

    def load_categories(self):
        cats = self.db.get_categories()
        return [(c["id"], c["name"]) for c in cats]

    def refresh(self):
        self.refresh_table()
        self.refresh_summary()

    def refresh_table(self):
        w = self.window
        cats = self.load_categories()
        rows = self.db.get_transactions(year=w.current_year, month=w.current_month)
        w.table.setRowCount(0)
        for r in rows:
            row = w.table.rowCount()
            w.table.insertRow(row)
            w.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(r["id"])))
            w.table.setItem(row, 1, QtWidgets.QTableWidgetItem(r["date"]))
            w.table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{r['amount']:.2f}"))
            w.table.setItem(row, 3, QtWidgets.QTableWidgetItem(r["type"]))
            w.table.setItem(row, 4, QtWidgets.QTableWidgetItem(r["category"] or "Uncategorized"))
            w.table.setItem(row, 5, QtWidgets.QTableWidgetItem(r["description"] or ""))

    def refresh_summary(self):
        w = self.window
        income, expense, balance = self.db.get_monthly_summary(w.current_year, w.current_month)
        w.income_label.setText(f"Income: {income:.2f}")
        w.expense_label.setText(f"Expenses: {expense:.2f}")
        w.balance_label.setText(f"Balance: {balance:.2f}")

    def add_transaction(self):
        cats = self.load_categories()
        dlg = TransactionDialog(self.window, categories=cats)
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            data = dlg.get_data()
            if data["amount"] <= 0:
                QtWidgets.QMessageBox.warning(self.window, "Validation", "Amount must be greater than zero.")
                return
            self.db.add_transaction(data["date"], data["amount"], data["category_id"], data["type"], data["description"])
            self.refresh()

    def _selected_tx_id(self):
        sel = self.window.table.selectedItems()
        if not sel:
            return None
        row = sel[0].row()
        item = self.window.table.item(row, 0)
        return int(item.text())

    def edit_transaction(self):
        tx_id = self._selected_tx_id()
        if tx_id is None:
            QtWidgets.QMessageBox.information(self.window, "Edit", "Please select a transaction to edit.")
            return
        rows = self.db.conn.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,)).fetchone()
        if not rows:
            return
        data = {
            "date": rows["date"],
            "amount": rows["amount"],
            "type": rows["type"],
            "category_id": rows["category_id"],
            "description": rows["description"],
        }
        dlg = TransactionDialog(self.window, categories=self.load_categories(), data=data)
        if dlg.exec() == QtWidgets.QDialog.Accepted:
            nd = dlg.get_data()
            if nd["amount"] <= 0:
                QtWidgets.QMessageBox.warning(self.window, "Validation", "Amount must be greater than zero.")
                return
            self.db.update_transaction(tx_id, nd["date"], nd["amount"], nd["category_id"], nd["type"], nd["description"])
            self.refresh()

    def delete_transaction(self):
        tx_id = self._selected_tx_id()
        if tx_id is None:
            QtWidgets.QMessageBox.information(self.window, "Delete", "Please select a transaction to delete.")
            return
        if QtWidgets.QMessageBox.question(self.window, "Delete", "Delete selected transaction?") == QtWidgets.QMessageBox.StandardButton.Yes:
            self.db.delete_transaction(tx_id)
            self.refresh()

    def manage_categories(self):
        dlg = QtWidgets.QDialog(self.window)
        dlg.setWindowTitle("Manage Categories — Finly")
        dlg.resize(400, 300)
        layout = QtWidgets.QVBoxLayout(dlg)
        listw = QtWidgets.QListWidget()
        layout.addWidget(listw)
        btn_h = QtWidgets.QHBoxLayout()
        add = QtWidgets.QPushButton("Add")
        edit = QtWidgets.QPushButton("Edit")
        delete = QtWidgets.QPushButton("Delete")
        btn_h.addWidget(add)
        btn_h.addWidget(edit)
        btn_h.addWidget(delete)
        layout.addLayout(btn_h)

        def load_list():
            listw.clear()
            for cid, name in self.load_categories():
                item = QtWidgets.QListWidgetItem(name)
                item.setData(Qt.UserRole, cid)
                listw.addItem(item)

        def on_add():
            cd = CategoryDialog(dlg)
            if cd.exec() == QtWidgets.QDialog.Accepted:
                name = cd.get_name()
                if name:
                    try:
                        self.db.add_category(name)
                    except Exception as e:
                        QtWidgets.QMessageBox.warning(dlg, "Error", f"Could not add category: {e}")
                load_list()

        def on_edit():
            item = listw.currentItem()
            if not item:
                return
            cid = item.data(Qt.UserRole)
            name = item.text()
            cd = CategoryDialog(dlg, name=name)
            if cd.exec() == QtWidgets.QDialog.Accepted:
                new_name = cd.get_name()
                if new_name:
                    self.db.update_category(cid, new_name)
                load_list()

        def on_delete():
            item = listw.currentItem()
            if not item:
                return
            cid = item.data(Qt.UserRole)
            if QtWidgets.QMessageBox.question(dlg, "Delete", f"Delete category '{item.text()}'?") == QtWidgets.QMessageBox.StandardButton.Yes:
                ok = self.db.delete_category(cid)
                if not ok:
                    QtWidgets.QMessageBox.warning(dlg, "Cannot delete", "Category is used by transactions or is protected.")
                load_list()

        add.clicked.connect(on_add)
        edit.clicked.connect(on_edit)
        delete.clicked.connect(on_delete)

        load_list()
        dlg.exec()
        self.refresh()

    def export_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self.window, "Export CSV", os.path.expanduser("~/transactions.csv"), "CSV Files (*.csv)")
        if not path:
            return
        try:
            self.db.export_csv(path)
            QtWidgets.QMessageBox.information(self.window, "Export", f"Exported to {path}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.window, "Error", f"Export failed: {e}")

    def show_about(self):
        # Show the About dialog (views.AboutDialog)
        try:
            dlg = AboutDialog(self.window)
        except Exception:
            # import lazily to avoid circular import if necessary
            from .views import AboutDialog
            dlg = AboutDialog(self.window)
        dlg.exec()

    def prev_month(self):
        w = self.window
        if w.current_month == 1:
            w.current_month = 12
            w.current_year -= 1
        else:
            w.current_month -= 1
        w.update_month_label()
        self.refresh()

    def next_month(self):
        w = self.window
        if w.current_month == 12:
            w.current_month = 1
            w.current_year += 1
        else:
            w.current_month += 1
        w.update_month_label()
        self.refresh()

    def run(self):
        self.window.show()
