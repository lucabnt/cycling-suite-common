"""Shared Qt shell; product server, data and lifecycle remain in each app."""
import sys
from pathlib import Path

def run_window(url,title,icon,port,started,failed,app_id):
    from PySide6.QtCore import QUrl,QTimer
    from PySide6.QtGui import QIcon,QDesktopServices
    from PySide6.QtWidgets import QApplication,QFileDialog,QMessageBox
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWebEngineCore import QWebEnginePage
    qt=QApplication(sys.argv[:1]);qt.setApplicationName(title);qt.setWindowIcon(QIcon(str(icon)))
    if sys.platform=='win32':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    def external(target):
        if target.scheme()=='mailto' or target.scheme() in ('http','https') and target.host()!='127.0.0.1':
            QDesktopServices.openUrl(target);return True
        return False
    class LocalPage(QWebEnginePage):
        def acceptNavigationRequest(self,target,kind,is_main):
            if external(target):return False
            return target.scheme() in ('blob','data') or target.scheme()=='http' and target.host()=='127.0.0.1' and target.port()==port
    view=QWebEngineView();view.setPage(LocalPage(view));view.setWindowTitle(title);view.resize(1440,960)
    view.page().newWindowRequested.connect(lambda request:external(request.requestedUrl()))
    def download(item):
        filename,_=QFileDialog.getSaveFileName(view,'Salva',item.downloadFileName())
        if filename:
            item.setDownloadDirectory(str(Path(filename).parent));item.setDownloadFileName(Path(filename).name);item.accept()
        else:item.cancel()
    view.page().profile().downloadRequested.connect(download)
    timer=QTimer()
    def ready():
        if started():timer.stop();view.load(QUrl(url));view.show()
        elif failed():timer.stop();QMessageBox.critical(view,'Avvio non riuscito','Consultare il registro locale del server.');qt.quit()
    timer.timeout.connect(ready);timer.start(100)
    return qt.exec()
