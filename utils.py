from PyQt5.QtGui import QPainter, QImage, qRgba


def to_transparent_image(img: QImage) -> QImage:
    ret = QImage(img.size(), QImage.Format_RGB32)
    ret.fill(qRgba(255, 255, 255, 0))
    p = QPainter(ret)
    p.setCompositionMode(QPainter.CompositionMode_SourceAtop)
    p.drawImage(0, 0, img)
    return ret
