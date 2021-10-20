#Importamos la libreria openCV
import cv2 as cv

#Para capturar video le pasamos el valor 0 como parametro para buscar camaras trabakando dentro del pc
#Se pasa parametro 1 para buscar camaras externas.
capturaVideo=cv.VideoCapture(1)

if not capturaVideo.isOpened():
    print("No se encontro una camara")
    exit()
while True:
    tipocamara,Camara=capturaVideo.read()
    grises=cv.cvtColor(Camara, cv.COLOR_BGR2GRAY)

    cv.imshow("En vivo",grises)

    #Para video se pasa como parametro el 1, para fotos el 0
    #ord reconoce una tecla que pasemos.
    if cv.waitKey(1)==ord("p"):
        break
capturaVideo.release()
cv.destroyAllWindows()