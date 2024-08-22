import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import math

def rotate (dir, ang1, ang2):
    points_x = []
    points_y = []
    points_z = []

    arq = np.loadtxt(dir)

    for i in range(len(arq)):

        radius = math.sqrt(arq[i][0]**2 + arq[i][1]**2)

        if not(arq[i][0] == 0):
            beta = np.arctan((arq[i][1]/arq[i][0])*180/np.pi)
        else:
            beta = 0

        ldot = radius*np.sin(ang1*np.pi/180)/(np.sin((90 - ang1/2)*np.pi/180))

        points_x.append(float(arq[i][0] - ldot*np.sin((ang1/2 + beta)*np.pi/180)))
        points_y.append(float(arq[i][1] + ldot*np.cos((ang1/2 + beta)*np.pi/180)))
        points_z.append(0)
    
    for j in range(len(arq)):

        radius = points_x[j]

        ldot = radius*np.sin(ang2*np.pi/180)/(np.sin((90 - ang2/2)*np.pi/180))

        points_x[j] = float(points_x[j] - ldot*np.sin((ang2/2)*np.pi/180))
        points_z[j] = float(ldot*np.cos((ang2/2)*np.pi/180))
            
    return(points_x, points_y, points_z)

def excel_save(x, y, z, nome):

    name = str(nome) + ".xlsx"

    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet("Values")
    
    for i in range(len(x)):
        worksheet.write(i, 0, x[i])
        worksheet.write(i, 1, y[i])
        worksheet.write(i, 2, z[i])
    
    workbook.close()

x,y,z = (rotate(r"C:\Users\U57534\OneDrive - Bühler\Desktop\FINS\S1046.txt", 30, 30))
excel_save(x, y, z, "Teste")

