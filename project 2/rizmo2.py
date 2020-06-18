import cv2
import numpy as np  ## used to modifie and read pictures!

#########################################################

def check_z (z,r1,r2):     ## function to check size of z with r1 and r2 parameters
    if ((abs(z) < r1) ^ (abs(z) < r2)).any() :  ##stackoverflow said "and" operator is unusable here
        return np.log(z/r1)
    else :
        return 0

def generate_first_x (new_z,reshape_meter):  ## calculations presented in the description!
    Wx = np.real(new_z)
    Wxmax = max(abs(Wx))
    NewX = ((Wx/Wxmax) + 1) * (len(Y) / 2)
    k = len(NewX)
    for j in range(k):
        NewX[j] = int(NewX[j])
    NewX = NewX.reshape(reshape_meter)
    return NewX

def generate_first_y (new_z,reshape_meter):  ## calculations presented in the description!
    Wy = np.imag(new_z)
    Wymax = max(abs(Wy))
    NewY = ((Wy/Wymax) + 1) * (len(X) / 2)
    k = len(NewY)
    for j in range(k):
        NewY[j] = int(NewY[j])
    NewY = NewY.reshape(reshape_meter)
    return NewY

def triple_pic_height (NewY,X): ## function to generate the third part height.
    NewY = np.tile(NewY, (3,1))
    for j in range(3*len(X)):
        param = int(j / len(X)) * len(X)
        NewY[j] = NewY[j] + param
    return NewY

def update_third_wx (NewX, Wxmax, X): ##making the third Wx
     W3 = (NewX * 2 /len(X) - 1)
     W3 = W3 * Wxmax
     return W3

def update_third_wy (NewY, Wymax, Y): ## making the third Wy
     W3 = (NewY * 2 /len(Y) - 1)
     W3 = W3 * Wymax
     return W3 

def generate_last_x (last_z, X):
     Wx = np.real(last_z)
     Wxmax = np.max(np.abs(Wx))
     LastX = ((Wx/Wxmax) + 1) * (len(X) / 2)
     return LastX

def generate_last_y (last_z, Y):
     Wy = np.imag(last_z)
     Wymax = np.max(np.abs(Wy))
     LastY = ((Wy/Wymax) + 1) * (len(Y) / 2)
     return LastY


clock = cv2.imread("clock.jpg",0)
reshape_meter = clock.shape
Rvector = np.linspace(-1,1, num = len(clock))     ## making a vector from rows
Cvector = np.linspace(-1,1, num = len(clock[1]))  ## making a vector from columns
X , Y = np.meshgrid(Rvector, Cvector)  ## r is the size of X and c is the size of Y
Z = X + 1j * Y  ## new matris that X is the real part and Y in the Imaginary

new_z = []
r1 = 0.2
r2 = 0.9
for j in range (len(X)):
    for i in range (len(Y)):
        result = check_z(Z[j][i],r1,r2)
        new_z.append(result)
NewX = generate_first_x(new_z,reshape_meter)
NewY = generate_first_y(new_z,reshape_meter)
first_one= np.zeros([len(X), len(Y), 3], dtype=np.uint8)
for i in range(len(X)):
    for j in range(len(Y)):
        a = int(NewY[i][j]) - 1
        b = int(NewX[i][j]) - 1
        first_one[a, b] = clock[i][j]

################################################################

second_z = []   ##roatation part!(second part)
circum = 2*np.pi
logarithm = np.log(r2/r1) 
alp = np.arctan(logarithm / circum)
f = np.cos(alp)
for j in range (len(X)):
    for i in range (len(Y)):
        result = Z[i][j] * f * np.power(np.e, 1j * alp)
        second_z.append(result)
SecX = generate_first_x(second_z,reshape_meter)
SecY = generate_first_y(second_z,reshape_meter)
second_one= np.zeros([len(X), len(Y), 3], dtype=np.uint8)
for i in range(len(X)):
    for j in range(len(Y)):
        a = int(SecY[i][j]) - 1
        b = int(SecX[i][j]) - 1
        second_one[a, b] = clock[i][j]




################################################################

## two images merged together vertically (third part) :

NewX = np.tile(NewX, (3,1))
NewY = triple_pic_height(NewY,X)
third_one = np.zeros([len(X) * 3, len(Y), 3], dtype="uint8")
for i in range(3 * len(X)):
    for j in range(len(Y)):
        a = int(NewY[i][j]) - 1
        b = int(NewX[i][j]) - 1
        third_one[a, b] = clock[i % len(X)][j]
Wxthird = update_third_wx(NewX, max(abs(np.real(new_z))),X)
Wythird = update_third_wy(NewY, max(abs(np.imag(new_z))),Y)


#################################################################

last_z = Wxthird + 1j * Wythird   ## initializing the last z for the fourth part.
circum = 2*np.pi
logarithm = np.log(r2/r1) 
alp = np.arctan(logarithm / circum)
f = np.cos(alp)
last_z = last_z * f * np.power(np.e, 1j * alp)  ## generating the last z with the given parameters such as alpha and f
last_z = np.power(np.e, last_z)
LastX = generate_last_x(last_z,X)  ## generating the X and Y inorder the make the shape.
LastY = generate_last_y(last_z,Y)  ## generating the X and Y inorder the make the shape.
last_one = np.zeros([len(X), len(Y), 3], dtype=np.uint8)
for i in range(3 * len(X)):
    for j in range(len(Y)):
        a = int(LastX[i][j]) - 1
        b = int(LastY[i][j]) - 1
        last_one[a, b] = clock[i % len(X)][j]

cv2.imshow('shape', last_one)
cv2.waitKey(0)
cv2.destroyAllWindows()














