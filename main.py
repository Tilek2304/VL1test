import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFormLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTranslator

class LabApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("Виртуальная лаборатория"))
        self.setGeometry(100, 100, 900, 600)

        # Центральный виджет с вкладками
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Вкладки
        self.init_tabs()

    def init_tabs(self):
        # Вкладка 1: Ход работы
        self.tab_work = QWidget()
        self.tabs.addTab(self.tab_work, self.tr("Ход работы"))
        self.init_tab_work()

        # Вкладка 2: Эксперимент
        self.tab_experiment = QWidget()
        self.tabs.addTab(self.tab_experiment, self.tr("Эксперимент"))
        self.init_tab_experiment()

        # Вкладка 3: Контрольный вопрос
        self.tab_question = QWidget()
        self.tabs.addTab(self.tab_question, self.tr("Контрольный вопрос"))
        self.init_tab_question()

    def update_teory(self, image_path):
        if not hasattr(self, 'teory'):
            self.teory = QLabel()

        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(500, 200, aspectRatioMode=1)
        self.teory.setPixmap(scaled_pixmap)

    def init_tab_work(self):
        layout = QVBoxLayout()

        text = QLabel(self.tr("""Чтобы подсчитать цену делений шкалы, нужно:
а) выбрать на шкале два ближайших оцифрованных штриха;
б) сосчитать количество делений между ними;
в) разность значений около выбранных штрихов разделить на количество делений.

На этом рисунке в крупном масштабе показана шкала термометра. Проиллюстрируем с ее помощью правило для вычисления цены деления:
а) выбираем оцифрованные штрихи 20 °С и 40 °С;
б) между ними 10 делений (промежутков);
в) вычисляем: (40 °С – 20 °С) : 10 делений = 2 °С/дел.

Ответ: цена делений = 2 °С/дел."""))

        image = QLabel()
        self.update_teory('teory.jpg')
        image.setScaledContents(True)

        layout.addWidget(self.teory, alignment=Qt.AlignCenter)
        layout.addWidget(text)
        self.tab_work.setLayout(layout)

    def update_menzurka_image(self, image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(200, 400, aspectRatioMode=1)
        self.menzurka_image.setPixmap(scaled_pixmap)

    def init_tab_experiment(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.answer1 = QLineEdit()
        self.answer2 = QLineEdit()
        self.answer3 = QLineEdit()
        self.answer4 = QLineEdit()
        form_layout.addRow(self.tr("Объем воды на уровне верхнего штриха:"), self.answer1)
        form_layout.addRow(self.tr("Объем жидкости на уровне первого снизу штриха, обозначенного цифрой, отличной от нуля:"), self.answer2)
        form_layout.addRow(self.tr("Объем жидкости между 2-м и 3-м штрихами, обозначенными цифрами:"), self.answer3)
        form_layout.addRow(self.tr("Объем налитой воды:"), self.answer4)

        self.menzurka_image = QLabel()
        self.update_menzurka_image("empty_menzurka.png")

        self.fill_button = QPushButton(self.tr("Наполнить"))
        self.fill_button.clicked.connect(self.fill_menzurka)
        self.check_button = QPushButton(self.tr("Проверка"))
        self.check_button.clicked.connect(self.check_answers)

        layout.addLayout(form_layout)
        layout.addWidget(self.menzurka_image, alignment=Qt.AlignCenter)
        layout.addWidget(self.fill_button)
        layout.addWidget(self.check_button)
        self.tab_experiment.setLayout(layout)

    def init_tab_question(self):
        layout = QVBoxLayout()
        text = QLabel(self.tr("Ответьте на контрольный вопрос и предоставьте ответ учителю."))
        layout.addWidget(text)
        self.tab_question.setLayout(layout)

    def fill_menzurka(self):
        import random
        levels = ["first_menzurka.png", "second_menzurka.png", "half_menzurka.png", "full_menzurka.png"]
        chosen_level = random.choice(levels)

        self.update_menzurka_image(chosen_level)

        self.correct_answer1 = 1000
        self.correct_answer2 = 100
        self.correct_answer3 = 100

        if "first" in chosen_level:
            self.correct_answer4 = 240
        elif "second" in chosen_level:
            self.correct_answer4 = 540
        elif "half" in chosen_level:
            self.correct_answer4 = 460
        elif "full" in chosen_level:
            self.correct_answer4 = 950

    def check_answers(self):
        try:
            answer1 = int(self.answer1.text())
            answer2 = int(self.answer2.text())
        except ValueError:
            QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Введите числовые значения."))
            return

        if answer1 == self.correct_answer1 and answer2 == self.correct_answer2:
            QMessageBox.information(self, self.tr("Результат"), self.tr("Все верно! Перейдите на следующую вкладку."))
            self.tabs.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, self.tr("Ошибка"), self.tr("Ответы неверны. Попробуйте снова."))


if __name__ == "__main__":

    app = QApplication(sys.argv)    
    translator = QTranslator()
    translator.load("translations/kyrgyz.qm")  # Путь к файлу перевода
    app.installTranslator(translator)
    window = LabApp()
    window.show()
    sys.exit(app.exec_())
