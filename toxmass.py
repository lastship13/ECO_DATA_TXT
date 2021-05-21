import run
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = run.MyMain()
   sys.exit(app.exec_())
