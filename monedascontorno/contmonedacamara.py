#Importamos la libreria openCV
from cv2 import cv2
#Importamos la libreria numpy para trabajar con matrices
import numpy as np

def ordenarpuntos(puntos):

    #Enlaza matrices y tolist convierte el valor en una lista
    n_puntos=np.concatenate([puntos[0],puntos[1],puntos[2],puntos[3]]).tolist()
    #Primer punto del eje y
    y_order=sorted(n_puntos,key=lambda n_puntos:n_puntos[1])

    #Punto 1
    x1_order=y_order[:2]
    #Punto 2
    x1_order=sorted(x1_order,key=lambda x1_order:x1_order[0])
    #Punto 3
    x2_order=y_order[2:4]
    #Punto 4
    x2_order=sorted(x2_order,key=lambda x2_order:x2_order[0])

    return [x1_order[0],x1_order[1],x2_order[0],x2_order[1]]
    
def alineamiento(imagen,ancho,alto):

    imagen_alineada=None

    #imagen en escala de grises
    grises=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    #umbral
    tipoumbral,umbral=cv2.threshold(grises, 150,255, cv2.THRESH_BINARY)
    #mostrar
    cv2.imshow("Umbral", umbral)
    contorno=cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contorno=sorted(contorno,key=cv2.contourArea,reverse=True)[:1]

    for c in contorno:
        #arclength para sacar el contorno se multiplica para evitar el ruido
        epsilon=0.01*cv2.arcLength(c, True)

        approximacion=cv2.approxPolyDP(c, epsilon, True)
        if len(approximacion)==4:
            puntos=ordenarpuntos(approximacion)
            puntos1=np.float32(puntos)
            puntos2=np.float32([[0,0],[ancho,0],[0,alto],[ancho,alto]])
            M = cv2.getPerspectiveTransform(puntos1, puntos2)
            imagen_alineada=cv2.warpPerspective(imagen, M, (ancho,alto))
    return imagen_alineada
capturavideo= cv2.VideoCapture(1)

#Reconocimiento de camara  
while True:
    tipocamara,camara=capturavideo.read()
    if tipocamara==False:
        break
    imagen_A6=alineamiento(camara,ancho=480,alto=640)
    if imagen_A6 is not None:
        puntos=[]
        imagen_gris=cv2.cvtColor(imagen_A6,cv2.COLOR_BGR2GRAY)

        #Realiza un desenfoque y elimina el primer ruido
        blur=cv2.GaussianBlur(imagen_gris,(5,5),1)
        _,umbral2=cv2.threshold(blur,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
        cv2.imshow("Umbral",umbral2)
        contorno2=cv2.findContours(umbral2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        cv2.drawContours(imagen_A6, contorno2, -1, (255,0,0),2)
        suma1=0
        suma2=0
        for c_2 in contorno2:
            area=cv2.contourArea(c_2)
            Momentos = cv2.moments(c_2)
            if(Momentos["m00"]==0):
                Momentos["m00"]=1.0
            x=int(Momentos["m10"]/Momentos["m00"])
            y=int(Momentos["m01"]/Momentos["m00"])

            
            #Area caja    
            if area<10000 and area>4000:
            
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imagen_A6, "caja de fosforos",(x,y) , font, 0.75, (0,255,0),2)
                suma1=suma1+200
            
            #Area moneda de 100
            if area<3500 and area>1000:
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(imagen_A6, "moneda",(x,y) , font, 0.75, (234,67,53),2)
                suma2=suma2+100
        total=suma1+suma2
        print("Total valor:",round(total,2))
       # print("Sumatoria total en Centimetros:",round(total,2))
        total = 0
        cv2.imshow("Imagen A6", imagen_A6)
        #cv2.imshow("camara", camara)
    if cv2.waitKey(1) == ord('s'):
        break
capturavideo.release()
cv2.destroyAllWindows()







    



 


