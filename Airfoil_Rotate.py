#desafio - fazer um programa que:

#leia um arquivo de texto.                                                          -> OK
#Redimensione o perfil no tamanho que eu quero.                                     -> OK
#rotacione o perfil no angulo que quero.                                            -> OK
#rotacione o perfil no plano que quero.                                             -> OK
#calcular o Centro de masse e/ou centro geométrico para me auxiliar na modelagem.   -> OK
#salvar todos os dados em um excel.                                                 -> OK
#executar a macro do Catia.                                                         

import numpy as np 
import matplotlib.pyplot as plt
import xlsxwriter

#Coloca o ângulo de ataque do perfil definido
def rotate_point(dir, ang):

    points_a = []
    points_b = []
    points_c = []

    arq = np.loadtxt(dir)

    for i in range(len(arq)):
       points_a.append(arq[i][0]*np.cos((ang*np.pi)/180) - arq[i][1]*np.sin((ang*np.pi)/180))
       points_b.append(arq[i][0]*np.sin((ang*np.pi)/180) + arq[i][1]*np.sin((ang*np.pi)/180))
       points_c.append(0)

    return(points_a, points_b, points_c)

#rotaciona o ângulo em relação ao plano (falta testar se esta rotacionando certo)
def rotate_plane(x, y, z, ang):
    points_x = []
    points_y = []
    points_z = []
    for i in range(len(x)):

        points_y.append(y[i])
        points_x.append(x[i]*np.cos((ang*np.pi)/180) - z[i]*np.sin((ang*np.pi)/180))
        points_z.append(x[i]*np.sin((ang*np.pi)/180) + z[i]*np.sin((ang*np.pi)/180))

    return(points_x, points_y, points_z)

#translada nos eixos coordenados e coloca o tamanho da corda do perfil.
#recebe os pontos já rotacionados, aumenta a cora e então translada eles.
#caso translade antes e adicione a corda depois o perfil irá ficar desproporcional.
def translate(trans_x, trans_y, trans_z, x, y, z, chord):

    #possibilidade de fazer as duas coisas no mesmo loop, porém executando o aumento antes. 
    points_x = []
    points_y = []
    points_z = []

    for i in range(len(x)):
        points_x.append(x[i]*chord + trans_x)
        points_y.append(y[i]*chord + trans_y)
        points_z.append(z[i]*chord + trans_z)

    xdot, ydot , zdot = geometric_center(points_x, points_y, points_z)

    points_x.append(xdot)
    points_y.append(ydot)
    points_z.append(zdot)

    grafico = plt.figure().add_subplot(projection="3d")
    grafico.scatter(points_x, points_y, points_z)
    plt.grid(True)
    plt.show()

    return(points_x, points_y, points_z)

#salva a plnilha excel com todas as informações
def excel_save(x, y, z, nome):

    name = str(nome) + ".xlsx"

    workbook = xlsxwriter.Workbook(name)
    worksheet = workbook.add_worksheet("Values")
    
    for i in range(len(x)):
        worksheet.write(i, 0, x[i])
        worksheet.write(i, 1, y[i])
        worksheet.write(i, 2, z[i])
    
    workbook.close()

#Acha o centro geométrico do perfil
def geometric_center(x, y, z):
    xdot = 0
    ydot = 0
    zdot = 0

    for i in range(len(x)):

        xdot += x[i]/len(x)
        ydot += y[i]/len(y)
        zdot += z[i]/len(z)
    
    return(xdot, ydot, zdot)


#primeiro rotaciona em relação ao ponto
x,y,z = (rotate_point(r"C:\Users\U57534\OneDrive - Bühler\Desktop\FINS\GOE-775.txt", 45))

#rotaciona em relação ao eixo
xx, yy, zz = rotate_plane(x,y,z,5)

#translada e aumenta 
xxx, yyy, zzz = translate(0, 0, 0, xx, yy, zz, 100)

#salva em um novo excel, no futuro 
excel_save(xxx, yyy, zzz, "Teste_Perfil")