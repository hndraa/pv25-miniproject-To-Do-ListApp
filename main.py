import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QLineEdit, QTextEdit, QScrollArea, QFrame, QGridLayout, QGraphicsDropShadowEffect, QComboBox, QSpinBox, QSlider, QCheckBox, QRadioButton, QMessageBox, QDateEdit,  QStyle, QStyleOptionSlider, QToolButton, QMenu, QWidgetAction, QInputDialog,QDialog)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QDate, QSize, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon, QPainter
from datetime import datetime 
from functools import partial
from random import randint

class WelcomePage(QWidget):
    def __init__(self, switch_func):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Hapus margin
        layout.setSpacing(0)  # Hapus jarak antar elemen

        # Tambahkan stretch di atas untuk mendorong elemen ke bawah
        layout.addStretch()

        # Layout untuk elemen tengah (logo dan tombol)
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)

        # Tambahkan logo gambar
        self.logo = QLabel()
        logo_path = "logo.png"  # Ganti dengan path logo Anda
        if QIcon(logo_path).isNull():
            print(f"Error: Gambar logo tidak ditemukan di {logo_path}")
        else:
            self.logo.setPixmap(QIcon(logo_path).pixmap(150, 150))  # Atur ukuran logo
        self.logo.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(self.logo)

        # Tambahkan tombol mulai
        self.button = QPushButton("Mulai")
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(switch_func)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 25px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #005fa3;
            }
        """)
        center_layout.addWidget(self.button)

        # Tambahkan layout tengah ke layout utama
        layout.addLayout(center_layout)

        # Tambahkan stretch di bawah untuk mendorong elemen ke atas
        layout.addStretch()

        # Tambahkan label Student ID dan Student Name di bagian bawah
        self.student_info_label = QLabel("© Hendra Ahmad Yani - F1D022122")
        self.student_info_label.setAlignment(Qt.AlignCenter)
        self.student_info_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #666; /* Warna abu-abu */
                margin-top: 20px;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(self.student_info_label, alignment=Qt.AlignBottom)

        self.setLayout(layout)


        # Inisialisasi posisi gambar
        self.background_positions = [
            {"image": "Bg/todolist.png", "x": 0, "y": 0, "width": 80, "height": 80},
            {"image": "Bg/alarm.png", "x": 200, "y": 100, "width": 100, "height": 100},
            {"image": "Bg/check.png", "x": 400, "y": 200, "width": 120, "height": 120},
            {"image": "Bg/clock.png", "x": 600, "y": 300, "width": 90, "height": 90},
            {"image": "Bg/notes.png", "x": 800, "y": 400, "width": 110, "height": 110},
            {"image": "Bg/palette.png", "x": 1000, "y": 500, "width": 130, "height": 130},
            {"image": "Bg/pen.png", "x": 1200, "y": 600, "width": 70, "height": 70},
            {"image": "Bg/pencil.png", "x": 1400, "y": 700, "width": 100, "height": 100},
            {"image": "Bg/round.png", "x": 1600, "y": 800, "width": 90, "height": 90},
            {"image": "Bg/todolist.png", "x": 1800, "y": 900, "width": 120, "height": 120}
        ]

        # Timer untuk animasi
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_background_positions)
        self.timer.start(50)  # Perbarui setiap 50ms

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Gambar latar belakang dengan posisi dan ukuran yang diperbarui
        for bg in self.background_positions:
            pixmap = QIcon(bg["image"]).pixmap(bg["width"], bg["height"])  # Gunakan ukuran gambar
            painter.drawPixmap(bg["x"], bg["y"], pixmap)

    def update_background_positions(self):
        # Perbarui posisi gambar untuk menciptakan efek gerakan diagonal
        for bg in self.background_positions:
            bg["x"] += 2  # Gerakkan ke kanan
            bg["y"] += 1  # Gerakkan ke bawah

            # Reset posisi jika gambar keluar dari layar
            if bg["x"] > self.width():
                bg["x"] = -bg["width"]  # Reset ke luar layar di kiri
                bg["y"] = randint(0, self.height() - bg["height"])  # Posisi acak di sumbu Y
            if bg["y"] > self.height():
                bg["y"] = -bg["height"]  # Reset ke luar layar di atas
                bg["x"] = randint(0, self.width() - bg["width"])  # Posisi acak di sumbu X

            # Periksa tumpang tindih dengan gambar lain
            for other_bg in self.background_positions:
                if bg == other_bg:
                    continue  # Jangan periksa diri sendiri
                if self.is_overlapping(bg, other_bg):
                    # Jika bertabrakan, pindahkan gambar ke posisi baru
                    bg["x"] = randint(0, self.width() - bg["width"])
                    bg["y"] = randint(0, self.height() - bg["height"])

        # Paksa repaint untuk memperbarui tampilan
        self.update()

    def is_overlapping(self, rect1, rect2):
        return not (
            rect1["x"] + rect1["width"] <= rect2["x"] or
            rect1["x"] >= rect2["x"] + rect2["width"] or
            rect1["y"] + rect1["height"] <= rect2["y"] or
            rect1["y"] >= rect2["y"] + rect2["height"]
        )

class ToDoCard(QFrame):
    def __init__(self, title, description, created_time=None):
        super().__init__()
        self.setFixedSize(200, 320)
        self.setStyleSheet("""
            QFrame {
                background-color: #f2f2f2;
                border-radius: 15px; /* Tambahkan border radius */
                border: none; /* Hapus border default */
                
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(4, 4)
        self.setGraphicsEffect(shadow)

        # Jika waktu pembuatan tidak diberikan, gunakan waktu saat ini
        if created_time is None:
            created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Layout utama untuk konten dalam kotak
        inner_layout = QVBoxLayout()
        self.lbl_desc = QLabel(description)
        self.lbl_desc.setWordWrap(True)
        inner_layout.addWidget(self.lbl_desc)
        inner_layout.addStretch()  # Tambahkan stretch untuk mendorong konten ke atas

        # Tambahkan judul di bawah kotak
        self.lbl_title = QLabel(title)
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

        # Tambahkan waktu pembuatan di bawah judul
        self.lbl_time = QLabel(f"Dibuat: {created_time}")
        self.lbl_time.setAlignment(Qt.AlignCenter)
        self.lbl_time.setStyleSheet("font-size: 10px; color: gray;")

        # Layout untuk judul dan waktu di luar kotak
        outer_layout = QVBoxLayout()
        frame = QFrame()
        frame.setLayout(inner_layout)
        outer_layout.addWidget(frame)
        outer_layout.addWidget(self.lbl_title)
        outer_layout.addWidget(self.lbl_time)
        outer_layout.setAlignment(Qt.AlignCenter)

        # Atur layout utama
        self.setLayout(outer_layout)

class MainPage(QWidget):
    def __init__(self, switch_to_add):
        super().__init__()
        self.is_select_mode = False  # Awalnya tidak dalam mode seleksi
        self.switch_to_add = switch_to_add  # Simpan referensi ke metode switch_to_add
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FFDEE9, stop: 1 #B5FFFC
                ); /* Gradasi warna pastel */
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Hapus margin
        layout.setSpacing(0)  # Hapus jarak antar elemen

        # Tambahkan header
        self.header_label = QLabel("Daftar Kegiatan")  # Simpan sebagai atribut kelas
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(self.header_label)

        search_layout = QHBoxLayout()
        # Tambahkan widget container untuk search_layout
        search_widget = QWidget()
        search_widget.setLayout(search_layout)
        search_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #FFDEE9, stop: 1 #B5FFFC
                ); /* Gradasi warna pastel */
            }
        """)
        layout.addWidget(search_widget)

        # Tambahkan tombol menu aksi
        self.action_button = QToolButton()
        self.action_button.setIcon(QIcon("Icon/action.png"))  # Ganti dengan path ikon Anda
        self.action_button.setPopupMode(QToolButton.InstantPopup)
        self.action_button.setStyleSheet("""
            QToolButton {
                background: #28a745; /* Latar belakang transparan */
                border: 2px solid #ccc;
                border-radius: 15px;
                padding: 8px;
                font-size: 14px;
                color: #333;
            }
            QToolButton:hover {
                background-color: #f0f0f0;
                border: 2px solid #0078D7;
            }
            QToolButton::menu-indicator {
                width: 0px; /* Sembunyikan tanda dropdown */
            }
        """)

        # Tambahkan menu dropdown untuk tombol aksi
        self.action_menu = QMenu()
        delete_action = self.action_menu.addAction("Delete")
        view_action = self.action_menu.addAction("View")
        edit_action = self.action_menu.addAction("Edit")
        self.action_button.setMenu(self.action_menu)
        self.action_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff; /* Warna latar belakang menu */
                border: none; /* Hilangkan border */
                outline: none;
                border-radius: 10px; /* Membuat sudut membulat */
                padding: 5px; /* Jarak dalam menu */
            }
            QMenu::item {
                padding: 8px 20px; /* Jarak dalam item menu */
                border-radius: 8px; /* Membuat sudut membulat pada item */
                color: #333; /* Warna teks */
                font-size: 14px; /* Ukuran font */
            }
            QMenu::item:selected {
                background-color: #0078D7; /* Warna latar belakang saat hover */
                color: #ffffff; /* Warna teks saat hover */
            }
        """)

        # Tambahkan tombol aksi ke search layout
        search_layout.addWidget(self.action_button)
    

        # Hubungkan aksi menu
        delete_action.triggered.connect(self.enter_delete_mode)
        view_action.triggered.connect(self.enter_view_mode)
        edit_action.triggered.connect(self.enter_edit_mode)

        # Tambahkan input pencarian
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari berdasarkan judul...")
        self.search_input.textChanged.connect(self.filter_tasks)
        search_layout.addWidget(self.search_input)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 15px;
                font-size: 14px;
                background: transparent; /* Latar belakang transparan */
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #0078D7;
                background-color: #ffffff;
            }
        """)

        # Tambahkan tombol menu filter
        self.filter_button = QToolButton()
        self.filter_button.setIcon(QIcon("Icon/filter.png"))  # Ganti dengan path ikon menu
        self.filter_button.setPopupMode(QToolButton.InstantPopup)
        self.filter_button.setStyleSheet("""
            QToolButton {
                background: #28a745; /* Latar belakang transparan */
                border: 2px solid #ccc;
                border-radius: 15px;
                padding: 8px;
                font-size: 14px;
                color: #333;
            }
            QToolButton:hover {
                background-color: #f0f0f0;
                border: 2px solid #0078D7;
            }
            QToolButton::menu-indicator {
                width: 0px; /* Sembunyikan tanda dropdown */
            }
        """)

        # Tambahkan menu dropdown
        self.filter_menu = QMenu()
        self.filter_menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff; /* Warna latar belakang menu */
                border: none; /* Hilangkan border */
                outline: none;
                border-radius: 10px; /* Membuat sudut membulat */
                padding: 5px; /* Jarak dalam menu */
            }
            QMenu::item {
                padding: 8px 20px; /* Jarak dalam item menu */
                border-radius: 8px; /* Membuat sudut membulat pada item */
                color: #333; /* Warna teks */
                font-size: 14px; /* Ukuran font */
            }
            QMenu::item:selected {
                background-color: #0078D7; /* Warna latar belakang saat hover */
                color: #ffffff; /* Warna teks saat hover */
            }
        """)
        self.date_filter_action = QWidgetAction(self.filter_menu)
        self.priority_filter_action = QWidgetAction(self.filter_menu)

        # Filter tanggal
        date_filter_widget = QWidget()
        date_filter_layout = QVBoxLayout(date_filter_widget)
        date_filter_label = QLabel("Filter Tanggal:")
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.dateChanged.connect(self.filter_tasks)
        date_filter_layout.addWidget(date_filter_label)
        date_filter_layout.addWidget(self.date_filter)
        self.date_filter_action.setDefaultWidget(date_filter_widget)
        self.date_filter.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
                background-color: #f9f9f9;
                color: #333;
            }
            QDateEdit:focus {
                border: 2px solid #0078D7;
                background-color: #ffffff;
            }
        """)

        # Filter prioritas
        priority_filter_widget = QWidget()
        priority_filter_layout = QVBoxLayout(priority_filter_widget)
        priority_filter_label = QLabel("Filter Prioritas:")
        self.priority_slider = NumberedSlider(Qt.Horizontal)
        self.priority_slider.setRange(0, 10)
        self.priority_slider.setValue(0)  # Default ke 0 (tidak ada filter prioritas)
        self.priority_slider.valueChanged.connect(self.filter_tasks)
        priority_filter_layout.addWidget(priority_filter_label)
        priority_filter_layout.addWidget(self.priority_slider)
        self.priority_filter_action.setDefaultWidget(priority_filter_widget)
        self.priority_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #ccc;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 20px;
                height: 20px;
                background: #0078D7;
                border-radius: 10px;
                border: 2px solid #005fa3;
            }
            QSlider::handle:horizontal:hover {
                background: #005fa3;
            }
        """)

        # Filter waktu pelaksanaan
        waktu_filter_widget = QWidget()
        waktu_filter_layout = QVBoxLayout(waktu_filter_widget)
        waktu_filter_label = QLabel("Filter Waktu Pelaksanaan:")
        self.waktu_filter_combo = QComboBox()
        self.waktu_filter_combo.addItems(["Semua", "Pagi", "Siang", "Malam"])
        self.waktu_filter_combo.currentTextChanged.connect(self.filter_tasks)
        waktu_filter_layout.addWidget(waktu_filter_label)
        waktu_filter_layout.addWidget(self.waktu_filter_combo)
        waktu_filter_action = QWidgetAction(self.filter_menu)
        waktu_filter_action.setDefaultWidget(waktu_filter_widget)
        self.waktu_filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
                background-color: #f9f9f9;
                color: #333;
            }
            QComboBox:focus {
                border: 2px solid #0078D7;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 0px;
            }
            QComboBox QAbstractItemView {
                border: none;
                background-color: #ffffff;
                selection-background-color: #0078D7;
                selection-color: #ffffff;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        # Tambahkan filter ke menu
        self.filter_menu.addAction(self.date_filter_action)
        self.filter_menu.addAction(self.priority_filter_action)
        self.filter_menu.addAction(waktu_filter_action)

        self.filter_button.setMenu(self.filter_menu)

        search_layout.addWidget(self.filter_button)

        layout.addLayout(search_layout)

        # Tambahkan area scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none; /* Hilangkan border */
                background: transparent; /* Latar belakang transparan */
            }
            QScrollBar:vertical {
                border: none;
                background: #f2f2f2;
                width: 8px;
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #0078D7;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::handle:vertical:hover {
                background: #005fa3;
            }
        """)
        self.container = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        # Tambahkan layout utama ke container
        self.container_layout = QVBoxLayout()
        self.container.setLayout(self.container_layout)
        self.container_layout.addLayout(self.grid)

        self.scroll_area.setWidget(self.container)

        # Tambahkan scroll area ke layout utama
        layout.addWidget(self.scroll_area, stretch=1)  # Stretch agar memenuhi ruang

        # Tambahkan tombol melayang menggunakan QFrame
        self.floating_frame = QFrame(self)
        self.floating_frame.setStyleSheet("background: transparent;")
        self.floating_frame.setGeometry(self.width() - 80, self.height() - 100, 60, 60)  # Posisi tombol
        self.floating_frame.setFixedSize(60, 60)

        self.add_button = QPushButton(self.floating_frame)
        self.add_button.setFixedSize(60, 60)
        self.add_button.setIcon(QIcon("Icon/add.png"))  # Ganti dengan path ikon Anda
        self.add_button.setIconSize(QSize(30, 30))  # Atur ukuran ikon
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 30px; /* Membuat tombol berbentuk lingkaran */
                border: none;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.add_button.clicked.connect(switch_to_add)

        # Panggil resizeEvent secara manual untuk memastikan posisi tombol melayang benar
        self.resizeEvent(None)

        # Simpan daftar tugas untuk pencarian
        self.tasks = []
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Atur ulang posisi tombol melayang
        self.floating_frame.move(self.width() - 80, self.height() - 100)

    def add_task(self, title, description, important=False, priority=1, duration=0, duration_unit="Hari", waktu_pelaksanaan="Pagi"):
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        card = ToDoCard(title, f"{description}\nDurasi: {duration} {duration_unit}\nWaktu: {waktu_pelaksanaan}", created_time)
        
        # Simpan data tugas ke dalam self.tasks
        self.tasks.append({
            "title": title,
            "description": description,
            "created_time": created_time,
            "priority": priority,
            "duration": duration,
            "duration_unit": duration_unit,
            "waktu_pelaksanaan": waktu_pelaksanaan,
            "card": card
        })

        # Atur event handler berdasarkan mode seleksi
        if self.is_select_mode:
            if self.header_label.text() == "Delete":
                card.setStyleSheet("""
                    QFrame {
                        background-color: #f2f2f2;
                        border: 2px dashed #ff0000;
                        border-radius: 15px;
                    }
                """)
                card.mousePressEvent = lambda event, w=card: self.delete_task(w)
            elif self.header_label.text() == "View":
                card.setStyleSheet("""
                    QFrame {
                        background-color: #e6f7ff;
                        border: 2px dashed #0078D7;
                        border-radius: 15px;
                    }
                """)
                card.mousePressEvent = partial(self.handle_view_task_click, card)
            elif self.header_label.text() == "Edit Task":
                card.setStyleSheet("""
                    QFrame {
                        background-color: #DE1FFE1;
                        border: 2px dashed #0E8C11;
                        border-radius: 15px;
                    }
                """)
                card.mousePressEvent = partial(self.handle_edit_task_click, card)

        # Tambahkan kartu tugas ke grid layout
        if important:
            # Simpan semua widget yang ada ke dalam daftar sementara
            existing_widgets = []
            for i in range(self.grid.count()):
                widget = self.grid.itemAt(i).widget()
                existing_widgets.append(widget)

            # Hapus semua widget dari layout
            while self.grid.count():
                widget = self.grid.takeAt(0).widget()
                if widget:
                    widget.setParent(None)

            # Tambahkan tugas penting di urutan pertama
            self.grid.addWidget(card, 0, 0)

            # Tambahkan kembali widget yang tersisa
            for index, widget in enumerate(existing_widgets):
                row = (index + 1) // 2
                col = (index + 1) % 2
                self.grid.addWidget(widget, row, col)
        else:
            # Tambahkan tugas biasa di akhir
            count = self.grid.count()
            row = count // 2
            col = count % 2
            self.grid.addWidget(card, row, col)
    def filter_tasks(self):
        search_text = self.search_input.text().lower()
        selected_date = self.date_filter.date().toString("yyyy-MM-dd")
        selected_priority = self.priority_slider.value()
        selected_waktu = self.waktu_filter_combo.currentText()

        # Hapus semua widget dari layout
        while self.grid.count():
            widget = self.grid.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        # Tambahkan kembali widget yang sesuai dengan filter
        for task in self.tasks:
            task_date = task["created_time"].split(" ")[0]
            task_priority = task["priority"]
            task_waktu = task.get("waktu_pelaksanaan", "Semua")
            if (
                (search_text in task["title"].lower() or not search_text) and
                (task_date == selected_date or not selected_date) and
                (task_priority == selected_priority or selected_priority == 0) and
                (task_waktu == selected_waktu or selected_waktu == "Semua")
            ):
                count = self.grid.count()
                row = count // 2
                col = count % 2
                self.grid.addWidget(task["card"], row, col)

    def enter_delete_mode(self):
        self.is_select_mode = True  # Aktifkan mode seleksi
        self.header_label.setText("Delete")
        QMessageBox.information(self, "Delete Mode", "Pilih tugas yang ingin dihapus. Klik tombol kembali untuk keluar dari mode seleksi.")
        
        # Ubah ikon tombol melayang menjadi ikon "back"
        self.add_button.setIcon(QIcon("Icon/back_icon.png"))  # Ganti dengan path ikon back
        self.add_button.setIconSize(QSize(30, 30))
        self.add_button.clicked.disconnect()  # Lepaskan koneksi sebelumnya
        self.add_button.clicked.connect(self.exit_select_mode)  # Hubungkan ke fungsi keluar mode seleksi

        # Tampilkan border merah pada semua tugas
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ToDoCard):
                widget.setStyleSheet("""
                    QFrame {
                        background-color: #f2f2f2; /* Warna merah muda untuk mode seleksi */
                        border: 2px dashed #ff0000; /* Border merah untuk seleksi */
                        border-radius: 15px;
                    }
                """)
                widget.mousePressEvent = lambda event, w=widget: self.delete_task(w)

    def exit_select_mode(self):
        self.is_select_mode = False  # Nonaktifkan mode seleksi
        self.header_label.setText("Daftar Kegiatan")  # Kembalikan judul halaman ke default

        # Ubah ikon tombol melayang kembali menjadi ikon tambah task
        self.add_button.setIcon(QIcon("Icon/add.png"))  # Ganti dengan path ikon tambah
        self.add_button.setIconSize(QSize(30, 30))
        self.add_button.clicked.disconnect()  # Lepaskan koneksi sebelumnya
        self.add_button.clicked.connect(self.switch_to_add)  # Hubungkan kembali ke fungsi tambah task

        # Hapus border dari semua tugas dan reset mousePressEvent
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ToDoCard):
                widget.setStyleSheet("""
                    QFrame {
                        background-color: #f2f2f2; /* Kembalikan ke warna default */
                        border-radius: 15px;
                    }
                """)
                widget.mousePressEvent = None  # Hapus koneksi mousePressEvent

    def delete_task(self, widget):
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus tugas ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Hapus widget dari layout dan daftar tugas
            for i, task in enumerate(self.tasks):
                if task["card"] == widget:
                    self.tasks.pop(i)
                    break
            widget.setParent(None)  # Hapus widget dari layout

            # Atur ulang posisi widget yang tersisa
            self.rearrange_tasks()
    
    def enter_view_mode(self):
        self.is_select_mode = True  # Aktifkan mode seleksi
        self.header_label.setText("View")  # Ubah judul halaman menjadi "View"

        # Ubah ikon tombol melayang menjadi ikon "back"
        self.add_button.setIcon(QIcon("Icon/back_icon.png"))  # Ganti dengan path ikon back
        self.add_button.setIconSize(QSize(30, 30))
        self.add_button.clicked.disconnect()  # Lepaskan koneksi sebelumnya
        self.add_button.clicked.connect(self.exit_select_mode)  # Hubungkan ke fungsi keluar mode seleksi

        # Tampilkan border biru pada semua tugas untuk menandakan mode View
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ToDoCard):
                widget.setStyleSheet("""
                    QFrame {
                        background-color: #e6f7ff; /* Warna biru muda untuk mode View */
                        border: 2px dashed #0078D7; /* Border biru untuk seleksi */
                        border-radius: 15px;
                    }
                """)
                # Gunakan partial untuk memastikan setiap widget memiliki koneksi unik
                widget.mousePressEvent = partial(self.handle_view_task_click, widget)
    
    def handle_view_task_click(self, widget, event):
        self.show_task_details(widget)

    def rearrange_tasks(self):
        # Hapus semua widget dari layout
        while self.grid.count():
            widget = self.grid.takeAt(0).widget()
            if widget:
                widget.setParent(None)

        # Tambahkan kembali widget yang tersisa ke layout
        for index, task in enumerate(self.tasks):
            row = index // 2
            col = index % 2
            self.grid.addWidget(task["card"], row, col)

    def view_task(self):
        QMessageBox.information(self, "View Mode", "Klik pada tugas untuk melihat detail.")
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ToDoCard):
                widget.mousePressEvent = lambda event, w=widget: self.show_task_details(w)

    def show_task_details(self, widget):
        for task in self.tasks:
            if task["card"] == widget:
                details = f"""
                Judul: {task['title']}
                Deskripsi: {task['description']}
                Prioritas: {task['priority']}
                Durasi: {task['duration']} {task['duration_unit']}
                Waktu Pelaksanaan: {task['waktu_pelaksanaan']}
                Dibuat: {task['created_time']}
                """
                QMessageBox.information(self, "Detail Tugas", details)
                break

    def enter_edit_mode(self):
        self.is_select_mode = True  # Aktifkan mode seleksi
        self.header_label.setText("Edit Task")  # Ubah judul halaman menjadi "Edit Task"
        QMessageBox.information(self, "Edit Mode", "Pilih tugas yang ingin diedit. Klik tombol kembali untuk keluar dari mode edit.")

        # Ubah ikon tombol melayang menjadi ikon "back"
        self.add_button.setIcon(QIcon("Icon/back_icon.png"))  # Ganti dengan path ikon back
        self.add_button.setIconSize(QSize(30, 30))
        self.add_button.clicked.disconnect()  # Lepaskan koneksi sebelumnya
        self.add_button.clicked.connect(self.exit_select_mode)  # Hubungkan ke fungsi keluar mode seleksi

        # Tampilkan border hijau pada semua tugas untuk menandakan mode Edit
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ToDoCard):
                widget.setStyleSheet("""
                    QFrame {
                        background-color: #DE1FFE1; /* Warna hijau muda untuk mode Edit */
                        border: 2px dashed #0E8C11; /* Border hijau untuk seleksi */
                        border-radius: 15px;
                    }
                """)
                # Gunakan partial untuk memastikan setiap widget memiliki koneksi unik
                widget.mousePressEvent = partial(self.handle_edit_task_click, widget)

    def handle_edit_task_click(self, widget, event):
        for task in self.tasks:
            if task["card"] == widget:
                # Tampilkan form edit
                self.show_edit_form(task)
                break

    def show_edit_form(self, task):
        # Form untuk mengedit task
        title, ok = QInputDialog.getText(self, "Edit Judul", "Masukkan judul baru:", QLineEdit.Normal, task["title"])
        if not ok:  # Jika dialog dibatalkan, keluar dari fungsi
            return
        if not title.strip():  # Validasi hanya jika dialog tidak dibatalkan
            QMessageBox.warning(self, "Error", "Judul tidak boleh kosong!")
            return

        description, ok = QInputDialog.getMultiLineText(self, "Edit Deskripsi", "Masukkan deskripsi baru:", task["description"])
        if not ok:  # Jika dialog dibatalkan, keluar dari fungsi
            return
        if not description.strip():  # Validasi hanya jika dialog tidak dibatalkan
            QMessageBox.warning(self, "Error", "Deskripsi tidak boleh kosong!")
            return

        # Gunakan dialog kustom untuk memilih waktu pelaksanaan
        dialog = WaktuPelaksanaanDialog(self, current_value=task["waktu_pelaksanaan"])
        if dialog.exec_() == QDialog.Accepted:
            waktu_pelaksanaan = dialog.get_selected_value()
        else:  # Jika dialog dibatalkan, keluar dari fungsi
            return

        # Perbarui task
        task["title"] = title
        task["description"] = description
        task["waktu_pelaksanaan"] = waktu_pelaksanaan

        # Perbarui tampilan kartu
        task["card"].lbl_title.setText(title)
        task["card"].lbl_desc.setText(
            f"{description}\nDurasi: {task['duration']} {task['duration_unit']}\nWaktu: {waktu_pelaksanaan}"
        )
class AddTaskPage(QWidget):
    def __init__(self, add_task_callback, back_to_main_callback):
        super().__init__()
        self.add_task_callback = add_task_callback
        self.back_to_main_callback = back_to_main_callback

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Header layout untuk tombol kembali dan judul
        header_layout = QHBoxLayout()

        # Tombol kembali
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon("Icon/back_icon.png"))  # Ganti dengan path ikon Anda
        self.back_button.setFixedSize(40, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                border: 2px solid #ccc;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.back_button.clicked.connect(self.back_to_main_callback)
        header_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Judul halaman
        title_label = QLabel("Tambah Kegiatan Baru")
        title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #222;")
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        # Tambahkan header layout ke layout utama
        layout.addLayout(header_layout)

        # Judul tugas
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul kegiatan...")
        self.title_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0078D7;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.title_input)

        # Deskripsi tugas
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Deskripsi kegiatan...")
        self.desc_input.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #0078D7;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.desc_input)

        # QComboBox - kategori
        self.category_combo = QComboBox()
        self.category_combo.addItem("Pilih Kategori")  # Tambahkan item awal
        self.category_combo.addItems(["Belajar", "Kerja", "Santai", "Olahraga", "Lainnya"])
        self.category_combo.setCurrentIndex(0)  # Set item awal sebagai default
        self.category_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 12px;
                font-size: 14px;
                background-color: #f9f9f9;
                color: #333;
            }
            QComboBox:focus {
                border: 2px solid #0078D7;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 0px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #0078D7;
                background-color: #ffffff;
                selection-background-color: #0078D7;
                selection-color: #ffffff;
                border-radius: 10px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.category_combo)

        # QSpinBox dan QComboBox untuk durasi
        durasi_layout = QHBoxLayout()
        durasi_label = QLabel("Durasi:")
        durasi_label.setStyleSheet("font-size: 14px; color: #333;")
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(0, 999)  # Nilai durasi dari 0 hingga 999
        self.duration_spin.setValue(0)  # Nilai default
        self.duration_spin.setStyleSheet("""
            QSpinBox {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 12px;
                font-size: 14px;
                background-color: #f9f9f9;
                color: #333;
                min-height: 15px; /* Tinggi minimum */
                min-width: 120px; /* Lebar minimum */
            }
            QSpinBox:focus {
                border: 2px solid #0078D7;
                background-color: #ffffff;
            }
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 30px;
                height: 40px;
                border: none;
                background-color: #4A90E2;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }
            QSpinBox::up-button:hover {
                background-color: #357ABD;
            }
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: top left;
                width: 30px;
                height: 40px;
                border: none;
                background-color: #4A90E2;
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
            }
            QSpinBox::down-button:hover {
                background-color: #357ABD;
            }
            QSpinBox::up-arrow {
                width: 12px;
                height: 12px;
                image: url('Icon/plus.png'); /* Path relatif ke ikon plus */
            }
            QSpinBox::down-arrow {
                width: 12px;
                height: 12px;
                image: url('Icon/minus.png'); /* Path relatif ke ikon minus */
            }
        """)

        self.duration_unit_combo = QComboBox()
        self.duration_unit_combo.addItems(["Detik", "Menit", "Jam", "Hari", "Minggu", "Bulan", "Tahun"])
        self.duration_unit_combo.setCurrentText("Hari")  # Set default ke "Hari"
        self.duration_unit_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 12px;
                font-size: 14px;
                background-color: #f9f9f9;
                color: #333;
            }
            QComboBox:focus {
                border: 2px solid #0078D7;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                width: 0px;
            }
        """)

        durasi_layout.addWidget(durasi_label)
        durasi_layout.addWidget(self.duration_spin)
        durasi_layout.addWidget(self.duration_unit_combo)
        layout.addLayout(durasi_layout)

        # QSlider - prioritas
        slider_layout = QVBoxLayout()
        self.priority_slider = NumberedSlider(Qt.Horizontal)
        slider_layout.addWidget(QLabel("Prioritas (0-10):"))
        slider_layout.addWidget(self.priority_slider)
        layout.addLayout(slider_layout)


        # QCheckBox - penting atau tidak
        self.important_checkbox = QCheckBox("Tandai sebagai penting")
        self.important_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #333;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked {
                background-color: #0078D7;
                border: 2px solid #005fa3;
            }
        """)
        layout.addWidget(self.important_checkbox)

        # QRadioButton - waktu pelaksanaan
        layout.addWidget(QLabel("Waktu Pelaksanaan:"))
        waktu_layout = QHBoxLayout()

        self.radio_pilih = QRadioButton("Pilih Waktu")
        self.radio_pilih.setChecked(True)  # Set default ke "Pilih Waktu"
        self.radio_pagi = QRadioButton("Pagi")
        self.radio_siang = QRadioButton("Siang")
        self.radio_malam = QRadioButton("Malam")

        for radio in [self.radio_pilih, self.radio_pagi, self.radio_siang, self.radio_malam]:
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 14px;
                    color: #333;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                    border-radius: 8px; /* Membuat indikator menjadi lingkaran */
                    border: 2px solid #ccc;
                    background-color: white;
                }
                QRadioButton::indicator:checked {
                    background-color: #0078D7;
                    border: 2px solid #005fa3;
                }
            """)
            waktu_layout.addWidget(radio)

        layout.addLayout(waktu_layout)

        # Tombol Simpan
        self.save_button = QPushButton("Simpan")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.save_button.clicked.connect(self.save_task)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_task(self):
        title = self.title_input.text()
        description = self.desc_input.toPlainText()
        category = self.category_combo.currentText()
        priority = self.priority_slider.value()
        important = self.important_checkbox.isChecked()
        duration = self.duration_spin.value()
        duration_unit = self.duration_unit_combo.currentText()

        # Tentukan waktu pelaksanaan
        if self.radio_pagi.isChecked():
            waktu_pelaksanaan = "Pagi"
        elif self.radio_siang.isChecked():
            waktu_pelaksanaan = "Siang"
        elif self.radio_malam.isChecked():
            waktu_pelaksanaan = "Malam"
        else:
            waktu_pelaksanaan = None

        # Validasi input
        if not title.strip():
            QMessageBox.warning(self, "Error", "Judul tidak boleh kosong!")
            return

        if category == "Pilih Kategori":
            QMessageBox.warning(self, "Error", "Silakan pilih kategori!")
            return

        if priority == 0:
            QMessageBox.warning(self, "Error", "Silakan pilih prioritas antara 1 - 10!")
            return

        if duration == 0:
            QMessageBox.warning(self, "Error", "Durasi tidak boleh 0!")
            return

        if not waktu_pelaksanaan:
            QMessageBox.warning(self, "Error", "Silakan pilih waktu pelaksanaan!")
            return

        # Simpan tugas jika validasi lolos
        self.add_task_callback(title, description, important, priority, duration, duration_unit, waktu_pelaksanaan)
        self.back_to_main_callback()
        self.clear_inputs()
    
    
    def clear_inputs(self):
        self.title_input.clear()
        self.desc_input.clear()
        self.category_combo.setCurrentIndex(0)  # Reset ke item awal
        self.duration_spin.setValue(0)  # Atur durasi ke 0
        self.duration_unit_combo.setCurrentText("Hari")  # Atur satuan durasi ke "Hari"
        self.priority_slider.setValue(0)  # Atur prioritas ke 0
        self.important_checkbox.setChecked(False)
        self.radio_pilih.setChecked(True)



class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List Modern")
        self.setFixedSize(500, 650)

        self.welcome = WelcomePage(self.show_main_page)
        self.main = MainPage(self.show_add_page)
        self.add_page = AddTaskPage(self.add_task, self.show_main_page)

        self.addWidget(self.welcome)
        self.addWidget(self.main)
        self.addWidget(self.add_page)

        # Tambahkan data dummy
        self.add_dummy_tasks()

    def add_dummy_tasks(self):
        # Data dummy
        dummy_tasks = [
            {"title": "Belajar Pemrograman", "description": "Menyelesaikan tugas kuliah tentang Python.", "important": True, "priority": 8, "duration": 2, "duration_unit": "Jam", "waktu_pelaksanaan": "Pagi"},
            {"title": "Olahraga Pagi", "description": "Jogging selama 30 menit di taman.", "important": False, "priority": 5, "duration": 30, "duration_unit": "Menit", "waktu_pelaksanaan": "Pagi"},
            {"title": "Meeting Kerja", "description": "Diskusi proyek dengan tim pada pukul 10:00.", "important": True, "priority": 9, "duration": 1, "duration_unit": "Jam", "waktu_pelaksanaan": "Siang"},
            {"title": "Membaca Buku", "description": "Membaca buku tentang pengembangan diri.", "important": False, "priority": 4, "duration": 3, "duration_unit": "Jam", "waktu_pelaksanaan": "Malam"},
            {"title": "Belanja Bulanan", "description": "Membeli kebutuhan rumah tangga di supermarket.", "important": False, "priority": 3, "duration": 2, "duration_unit": "Jam", "waktu_pelaksanaan": "Siang"},
        ]

        # Tambahkan setiap tugas ke daftar
        for task in dummy_tasks:
            self.main.add_task(task["title"], task["description"], task["important"], task["priority"], task["duration"], task["duration_unit"], task["waktu_pelaksanaan"])

    def animate_switch(self, index):
        current_widget = self.currentWidget()
        next_widget = self.widget(index)
        next_widget.setGeometry(0, self.height(), self.width(), self.height())
        self.setCurrentIndex(index)

        self.anim = QPropertyAnimation(next_widget, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(QRect(0, self.height(), self.width(), self.height()))
        self.anim.setEndValue(QRect(0, 0, self.width(), self.height()))
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def show_main_page(self):
        self.animate_switch(1)

    def show_add_page(self):
        self.animate_switch(2)

    def add_task(self, title, description, important=False, priority=1, duration=0, duration_unit="Hari", waktu_pelaksanaan="Pagi"):
        if title.strip():
            self.main.add_task(title, description, important, priority, duration, duration_unit, waktu_pelaksanaan)
            self.add_page.clear_inputs()
            self.show_main_page()

class NumberedSlider(QSlider):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setRange(0, 10)  # Skala slider dari 0 hingga 10
        self.setValue(0)  # Nilai default
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px; /* Tinggi jalur slider */
                background: #ccc;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 24px; /* Lebar tombol slider */
                height: 24px; /* Tinggi tombol slider */
                background: #0078D7;
                border-radius: 12px; /* Membuat tombol berbentuk lingkaran */
                border: 2px solid #005fa3;
                margin: -10px 0; /* Memastikan tombol lebih besar dari jalur */
            }
            QSlider::handle:horizontal:hover {
                background: #005fa3; /* Warna saat hover */
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        option = QStyleOptionSlider()
        self.initStyleOption(option)

        # Dapatkan posisi handle
        handle_rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self
        )
        handle_center = handle_rect.center()

        # Gambar angka di atas handle
        painter.setRenderHint(QPainter.Antialiasing)  # Aktifkan anti-aliasing
        painter.setPen(QColor("#ffffff"))  # Warna angka (putih)
        painter.setFont(QFont("Arial", 10, QFont.Bold))  # Font angka
        painter.drawText(
            handle_center.x() - 12, handle_center.y() - 12, 24, 24,
            Qt.AlignCenter, str(self.value())
        )
        painter.end()

class WaktuPelaksanaanDialog(QDialog):
    def __init__(self, parent=None, current_value="Pagi"):
        super().__init__(parent)
        self.setWindowTitle("Edit Waktu Pelaksanaan")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        # Label
        label = QLabel("Pilih waktu pelaksanaan:")
        label.setStyleSheet("font-size: 14px; color: #333;")
        layout.addWidget(label)

        # ComboBox untuk pilihan waktu pelaksanaan
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Pagi", "Siang", "Malam"])
        self.combo_box.setCurrentText(current_value)
        self.combo_box.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 14px;
                background-color: #ffffff; /* Warna putih */
                color: #333;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff; /* Warna putih untuk daftar */
                selection-background-color: #0078D7; /* Warna biru saat dipilih */
                selection-color: #ffffff; /* Warna teks saat dipilih */
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.combo_box)

        # Tombol OK dan Cancel
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def get_selected_value(self):
        return self.combo_box.currentText()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
