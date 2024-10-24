from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame,QSystemTrayIcon, QMenu
from PySide6.QtGui import QFont, QPixmap, QMouseEvent, QPainter, QColor, QPen,QFontDatabase,QAction,QIcon
from PySide6.QtCore import Qt, QTimer, QDateTime, QPoint, QTime
import sys


class RoundedFrame(QFrame):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setWidth(0)
        painter.setPen(pen)
        radius = 5  # 保持圆角半径一致
        painter.drawRoundedRect(self.rect(), radius, radius)


class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedSize(450, 200)

        # 去除主布局的背景颜色设置
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 主布局
        main_layout = QVBoxLayout()

        # 加载字体文件
        font_id = QFontDatabase.addApplicationFont("XiangJiaoDaJiangJunLingGanTi-2.ttf")
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # 时间标签
        self.time_label = QLabel()
        self.time_label.setFont(QFont(self.font_family, 40))
        up_text_label = QLabel("下班还有")
        up_text_label.setFont(QFont(self.font_family, 20))
        main_layout.addWidget(up_text_label, 0, Qt.AlignLeft)
        main_layout.addWidget(self.time_label, 0, Qt.AlignLeft)

        # 设定倒计时时间，例如下午6点
        self.end_time = QTime(17, 30, 0)

        # 定时器更新倒计时
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        # 详情和图片布局
        detail_and_image_layout = QHBoxLayout()

        # 详情布局
        detail_layout = QHBoxLayout()

        # 为每个详情创建圆角框架
        for text in ["发薪\n5\n天", "周五\n1\n天", "教师节\n5\n天", "今天赚了\n133.295¥"]:
            if "今天赚了" in text:
                frame = self.create_detail_frame(text, size=1)
            else:
                frame = self.create_detail_frame(text)
            detail_layout.addWidget(frame)

        detail_and_image_layout.addLayout(detail_layout)

        # 图片
        image_label = QLabel()
        pixmap = QPixmap("avatar.png")

        max_img_width, max_img_height = 100, 100
        scaled_pixmap = pixmap.scaled(max_img_width, max_img_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)

        # 图片加入布局
        detail_and_image_layout.addWidget(image_label, 0, Qt.AlignRight)

        # 添加到主布局中
        main_layout.addLayout(detail_and_image_layout)

        # 设置主布局
        self.setLayout(main_layout)

        # 记录鼠标位置
        self.old_pos = QPoint()

         # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("avatar.png"))
        self.tray_icon.setToolTip("Floating Widget")
        self.tray_icon.activated.connect(self.handle_tray_icon_activated)

        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = QAction("显示", self)
        hide_action = QAction("隐藏", self)
        quit_action = QAction("退出", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.quit_application)

        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def handle_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            # 单击托盘图标时显示或隐藏窗口
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        radius = 15
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, radius, radius)

    def create_detail_frame(self, text, size=0):
        frame = QWidget()
        frame.setFixedSize(70, 80) if size == 0 else frame.setFixedSize(90, 80)
        frame.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 5px;")
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setFont(QFont(self.font_family, 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        frame.setLayout(layout)
        return frame

    def update_time(self):
        current_time = QTime.currentTime()
        remaining_time = current_time.secsTo(self.end_time)

        if remaining_time > 0:
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            seconds = remaining_time % 60
            self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        else:
            self.time_label.setText("00:00:00")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if not self.old_pos.isNull():
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = QPoint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = FloatingWidget()
    widget.show()
    sys.exit(app.exec())
