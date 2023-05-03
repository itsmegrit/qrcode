import cv2 as cv
from pyzbar import pyzbar
cap = cv.VideoCapture(0)
ListMaSV=[]
while True:
    ret, frame = cap.read()
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        text = "{}".format(barcodeData)
        if text not in ListMaSV:
            ListMaSV.append(text)        
        cv.putText(frame, text, (x-10, y - 10), cv.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1)
    cv.imshow('Doc Ma Vach - Ma QR', frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
print(ListMaSV)
