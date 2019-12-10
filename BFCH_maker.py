import argparse 
parser = argparse.ArgumentParser(description='Draw sbgraph')
parser.add_argument('-C_prod', type=int, help='C_prod', required=True)
parser.add_argument('-H_prod', type=float, help='H_prod', required=True)
parser.add_argument('-N_prod', type=float, help='N_prod', required=True)
parser.add_argument('-O_prod', type=float, help='O_prod', required=True)
parser.add_argument('-C_start', type=int, help='C_start', required=True)
parser.add_argument('-H_start', type=int, help='H_start', required=True)
parser.add_argument('-O_start', type=int, help='O_start', required=True)
parser.add_argument('-Y', type=float, help='ECONOM_COEF', required=True)
parser.add_argument('-M_of_C_source', type=int, help='M(C_source)', required=True)
args = parser.parse_args()

A1 = 0
A2 = 0
A3 = 0
A4 = 0
A5 = 0
A6 = 0
A7 = 0

#making start substences ratio
C = args.C_start
H = args.H_start
O = args.O_start

#making products substences ratio
C_ = args.C_prod
H_ = args.H_prod
N_ = args.N_prod
O_ = args.O_prod

Mol_w_ADB = 12 * C_ + 1 * H_ + 14 * N_ + 16 * O_
M_C = args.M_of_C_source
print('M(ADB)', '=', Mol_w_ADB, 'g/mol')
print('M', '(','C', C, 'H', H, 'O', O, ')', ' = ', M_C, 'g/mol')
#balance of C
A5 = 1/Mol_w_ADB
A1 = A5 * C_/C 
#default NH4OH = NH5O
#balance of H and O
A2 = A5 * N_
if (A1 * H + A2 * 5) > (A5 * H_):
    A4 = 0 
    A6 = ((A1 * H + A2 * 5) - (A5 * H_)) * 0.5
    if (A1 * O + A2 * 1) > (A5 * O_ + A6 * 1):
        A3 = 0 
        A7 = ((A1 * O + A2 * 1) - (A5 * O_ + A6 * 1)) * 0.5
    else:
        A7 = 0
        A3 = ((A5 * O_ + A6 * 1) - (A1 * O + A2 * 1)) * 0.5
else:
    A6 = 0
    A4 = (A5 * H_ - A1 * H + A2 * 5) * 0.5
    if (A1 * O + A2 * 1 + A4 * 1) > A5 * O_:
        A3 = 0 
        A7 = ((A1 * O + A2 * 1 + A4 * 1) - A5 * O_) * 0.5
    else:
        A7 = 0
        A3 = (A5 * O_ - (A1 * O + A2 * 1 + A4 * 1)) * 0.5

if A3 == 0:
    if A4 == 0:
        print('Anabolism : ',  round(A1, 5), 'C', C, 'H', H, 'O', O, '+',  round(A2, 5), 'NH3OH', ' = ',  round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+',  round(A6, 5), 'H20', '+', round(A7, 5), 'O2')
    else:
        print('Anabolism : ', round(A1, 5), 'C', C, 'H', H, 'O', O, '+', round(A2, 5), 'NH3OH', '+', round(A4, 5), 'H2O', ' = ', round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+', round(A7, 5), 'O2')
else:
    if A4 == 0:
        print('Anabolism : ', round(A1, 5), 'C', C, 'H', H, 'O', O, '+', round(A2, 5), 'NH3OH', '+', round(A3, 5), 'O2', ' = ', round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+', round(A6, 5), 'H20')
    else:
        print('Anabolism : ', round(A1, 5), 'C', C, 'H', H, 'O', O, '+', round(A2, 5), 'NH3OH', '+', round(A3, 5), 'O2', '+', round(A4, 5), 'H2O', ' = ', round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_)

#Catabolism
K1 = 0
K2 = 0
K3 = 0
K4 = 0
K5 = 0

Y = args.Y
S = 1 / Y
print('ΔS', ' = ', S, 'g')
#balance of C
K1 = S / M_C - A1
K3 = K1 * C
#balance of H
K4 = (K1 * H) * 0.5
if (K1 * O) > (K3 * 2 + K4 * 1):
    K5 = ((K1 * O) - (K3 * 2 + K4 * 1)) * 0.5
else:
    K2 = ((K3 * 2 + K4 * 1) - (K1 * O)) * 0.5

if K2 == 0:
    print('Catabolism : ', round(K1, 5), 'C', C, 'H', H, 'O', O, ' = ', round(K3, 5), 'CO2', '+', round(K4, 5), 'H2O', '+', round(K5, 5), 'O2' )
else:
    print('Catabolism : ', round(K1, 5), 'C', C, 'H', H, 'O', O, '+', round(K2, 5), 'O2', ' = ', round(K3, 5), 'CO2', '+', round(K4, 5), 'H2O')

#Metabolism
if (round(A3, 5) + round(K2, 5)) > (round(A7, 5) + round(K5, 5)):
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        print('Metabolism : ', round(round(A1, 5) + round(K1, 5), 5), 'C', C, 'H', H, 'O', O, '+',  round(A2, 5), 'NH3OH', '+', round((round(A3, 5) + round(K2, 5)) - (round(A7, 5) + round(K5, 5)), 5), 'O2', '+', round((round(A4, 5) - (round(A6, 5) + round(K4, 5))), 5), 'H2O', ' = ',  round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+', round(K3, 5), 'CO2')
    else:
        print('Metabolism : ', round(round(A1, 5) + round(K1, 5), 5), 'C', C, 'H', H, 'O', O, '+',  round(A2, 5), 'NH3OH', '+', round((round(A3, 5) + round(K2, 5)) - (round(A7, 5) + round(K5, 5)), 5), 'O2', ' = ',  round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+', round((round(A6, 5) + round(K4, 5) - round(A4, 5)), 5), 'H20', '+', round(K3, 5), 'CO2')
else:
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        print('Metabolism : ', round(round(A1, 5) + round(K1, 5), 5), 'C', C, 'H', H, 'O', O, '+',  round(A2, 5), 'NH3OH', '+', round((round(A3, 5) + round(K2, 5)), 5), 'O2', '+', round((round(A4, 5) - (round(A6, 5) + round(K4, 5))), 5), 'H2O', ' = ',  round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+',  round(round(A6, 5) + round(K4, 5), 5), 'H20', '+', round(K3, 5), '+', 'CO2', round(((round(A7, 5) + round(K5, 5)) - (round(A3, 5) + round(K2, 5))), 5), 'O2')
    else:
        print('Metabolism : ', round(round(A1, 5) + round(K1, 5), 5), 'C', C, 'H', H, 'O', O, '+',  round(A2, 5), 'NH3OH', '+', round((round(A3, 5) + round(K2, 5)) - (round(A7, 5) + round(K5, 5)), 'O2', '+', round(A4, 5), 5), 'H2O', ' = ',  round(A5, 5), 'C', C_, 'H', H_, 'N', N_, 'O', O_, '+', round((round(A6, 5) + round(K4, 5) - round(A4, 5)), 5), 'H20', '+', round(K3, 5), 'CO2', round(((round(A7, 5) + round(K5, 5)) - (round(A3, 5) + round(K2, 5))), 5), 'O2')