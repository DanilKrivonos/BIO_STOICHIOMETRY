import argparse 
parser = argparse.ArgumentParser(description='Draw sbgraph')
parser.add_argument('-C_prod', type=float, help='C_prod', required=True)
parser.add_argument('-H_prod', type=float, help='H_prod', required=True)
parser.add_argument('-N_prod', type=float, help='N_prod', required=True)
parser.add_argument('-O_prod', type=float, help='O_prod', required=True)
parser.add_argument('-C_start', type=int, help='C_start', required=True)
parser.add_argument('-H_start', type=int, help='H_start', required=True)
parser.add_argument('-O_start', type=int, help='O_start', required=True)
parser.add_argument('-C_alt', type=int, help='C_alt', required=True)
parser.add_argument('-H_alt', type=int, help='H_alt', required=True)
parser.add_argument('-O_alt', type=int, help='O_alt', required=True)
parser.add_argument('-G_C_source', type=float, help='Gibbs energy of C source', required=True)
parser.add_argument('-G_C_alt_source', type=float, help='G_C_alt_source', required=True)
parser.add_argument('-Y', type=float, help='ECONOM_COEF', required=True)
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

M_C = 12 * C + 1 * H + 16 * O
print('M(C{}H{}O{}) = {} g/mol'.format(C, H, O, M_C))
#balance of C
A5 = 1
A1 = round(C_ /(C * 12 ), 5)
#default NH4OH = NH5O
#balance of H and O
A2 = round(N_ /14, 5)
if (A1 * H + A2 * 5 - H_ /1) > 0:
    A4 = 0 
    A6 = round((A1 * H + A2 * 5 - H_ /1) * 0.5, 5)
    if (A1 * O + A2 * 1 - O_ /16 - A6 * 1) > 0:
        A3 = 0 
        A7 = round((A1 * O + A2 * 1 - O_ /16 - A6 * 1) * 0.5, 5)
    else:
        A7 = 0
        A3 = round((O_ /16 + A6 * 1 - A1 * O + A2 * 1) * 0.5, 5)
else:
    A6 = 0
    A4 = round((H_ /1 - (A1 * H + A2 * 5)) * 0.5, 5)
    if (A1 * O + A2 * 1 + A4 * 1 - O_ /16 - A6 * 1) > 0:
        A3 = 0 
        A7 = round((A1 * O + A2 * 1 - O_ /16 - A6 * 1) * 0.5, 5)
    else:
        A7 = 0
        A3 = round((O_ /16 + A6 * 1 - A1 * O + A2 * 1) * 0.5, 5)
        
if A3 == 0:
    if A4 == 0:
        print('Anabolism : {} C{}H{}O{} + {} NH4OH  = {} C{}H{}N{}O{} + {} H20 + {} O2'.format(
            A1, C, H, O, A2, A5, C_, H_, N_, O_, A6, A7)
        )
    else:
        print('Anabolism : {} C{}H{}O{} + {} NH4OH + {} H2O  = {} C{}H{}N{}O{} + {} O2'.format(
            A1, C, H, O, A2, A4, A5, C_, H_, N_, O_, A7)
        )
else:
    if A4 == 0:
        print('Anabolism : {} C{}H{}O{} + {} NH4OH + {} O2 = {} C{}H{}N{}O{} + {} H20'.format(
            A1, C, H, O, A2, A3, A5, C_, H_, N_, O_, A6)
        )
    else:
        print('Anabolism : {} C{}H{}O{} + {} NH4OH + {} O2 +{} H2O = {} C{}H{}N{}O{}'.format(
            A1, C, H, O, A2, A3, A4, A5, C_, H_, N_, O_, A6)
        )

#Catabolism
K1 = 0
K2 = 0
K3 = 0
K4 = 0
K5 = 0

Y = args.Y
S = round(1 / Y, 5)
print('ΔS  = {} g'.format(S))
#balance of C
K1 = round(S / M_C - A1, 5)
K3 = round(K1 * C, 5)
#balance of H
K4 = round((K1 * H) * 0.5, 5)
if (K1 * O) > (K3 * 2 + K4 * 1):
    K5 = round(((K1 * O) - (K3 * 2 + K4 * 1)) * 0.5, 5)
else:
    K2 = round(((K3 * 2 + K4 * 1) - (K1 * O)) * 0.5, 5)

if K2 == 0:
    print('Catabolism : {} C{}H{}O{} = {} CO2 + {} H2O + {} O2'.format(
        K1, C, H, O, K3, K4, K5)
    )
else:
    print('Catabolism : {} C{}H{}O{} + {} O2 = {} CO2 + {} H2O'.format(
        K1, C, H, O, K2, K3, K4)
    )

#Metabolism
if (round(A3, 5) + round(K2, 5)) > (round(A7, 5) + round(K5, 5)):
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        print('Metabolism : {} C{}H{}O{} + {} NH4OH + {} O2 + {} H2O = {} C{}H{}N{}O{} + {} CO2'.format(
            round(A1 + K1, 5), C, H, O, A2, round(A3 + K2 - A7 + K5, 5, 5), round(A4 - A6 + K4, 5), A5, C_, H_, N_, O_, K3)
        )
    else:
        print('Metabolism : {} C{}H{}O{} + {} NH4OH + {} O2 = {} C{}H{}N{}O{} + {} H20 + {} CO2'.format(
            round(A1 + K1, 5), C, H, O, A2, round(A3 + K2 - A7 + K5, 5), A5, C_, H_, N_, O_, round(A6 + K4 - A4, 5), K3)
        )
else:
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        print('Metabolism : {} C{}H{}O{} + {} NH4OH + {} H2O = {} C{}H{}N{}O{} + {} CO2 + {} O2'.format(
            round(A1 + K1, 5), C, H, O, A2, round(A4 - A6 + K4, 5), A5, C_, H_, N_, O_, K3, round(A7 + K5 - A3 + K2, 5))
        )
    else:
        print('Metabolism : {} C{}H{}O{} + {} NH4OH = {} C{}H{}N{}O{} + {} H20 + {} CO2 + {} O2'.format(
            round(A1 + K1, 5), C, H, O, A2, A5, round(A6 + K4 - A4, 5), K3, round(A7 + K5 - A3 + K2, 5))
        )

ΔG1 = args.G_C_source#C source
#ignore ΔG2 NH4OH 
ΔG3 = 0 #O2
ΔG4 = -237.23#H2O
#ΔG5 of ADB is not exist
ΔG6 = -237.23#H2O
ΔG7 = -394.37#CO2
ΔG8 = 0#O2

ΔG_of_reaction =0
if (round(A3, 5) + round(K2, 5)) > (round(A7, 5) + round(K5, 5)):
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        ΔG_of_reaction = round(round(K3, 5) * ΔG7 - round((round(A4, 5) - (round(A6, 5) + round(K4, 5))), 5) * ΔG4 - round((round(A3, 5) + round(K2, 5)) - (round(A7, 5) + round(K5, 5)), 5) * ΔG3 - round(round(A1, 5) + round(K1, 5), 5) * ΔG1, 5)
        print('ΔG(reaction) = ΔG(ADB) + ΔGdissipation + {} kJ/mol'.format(ΔG_of_reaction))
    else:
        ΔG_of_reaction = round(round(K3, 5) * ΔG7 + round((round(A6, 5) + round(K4, 5) - round(A4, 5)), 5) * ΔG6 - round((round(A3, 5) + round(K2, 5)) - (round(A7, 5) + round(K5, 5)), 5) * ΔG3 - round(round(A1, 5) + round(K1, 5), 5) * ΔG1, 5)
        print('ΔG(reaction) = ΔG(ADB) + ΔGdissipation + {} kJ/mol'.format(ΔG_of_reaction))
else:
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        ΔG_of_reaction = round(round(K3, 5) * ΔG7 + round(((round(A7, 5) + round(K5, 5)) - (round(A3, 5) + round(K2, 5))), 5) * ΔG8 - round((round(A4, 5) - (round(A6, 5) + round(K4, 5))), 5) * ΔG4 - round(round(A1, 5) + round(K1, 5), 5) * ΔG1, 5)
        print('ΔG(reaction) = ΔG(ADB) + ΔGdissipation + {} kJ/mol'.format(ΔG_of_reaction))
    else:
        ΔG_of_reaction = round(round(K3, 5) * ΔG7 + round((round(A6, 5) + round(K4, 5) - round(A4, 5)), 5) * ΔG6 + round(((round(A7, 5) + round(K5, 5)) - (round(A3, 5) + round(K2, 5))), 5) * ΔG8 - round(round(A1, 5) + round(K1, 5), 5) * ΔG1, 5)
        print('ΔG(reaction) = ΔG(ADB) + ΔGdissipation + {} kJ/mol'.format(ΔG_of_reaction))

#alternative source of C
C = args.C_alt
H = args.H_alt
O = args.O_alt
#balance of C
A5 = 1
A1 = round(C_ /(C * 12 ), 5)
#default NH4OH = NH5O
#balance of H and O
A2 = round(N_ /14, 5)
if (A1 * H + A2 * 5 - H_ /1) > 0:
    A4 = 0 
    A6 = round((A1 * H + A2 * 5 - H_ /1) * 0.5, 5)
    if (A1 * O + A2 * 1 - O_ /16 - A6 * 1) > 0:
        A3 = 0 
        A7 = round((A1 * O + A2 * 1 - O_ /16 - A6 * 1) * 0.5, 5)
    else:
        A7 = 0
        A3 = round((O_ /16 + A6 * 1 - A1 * O - A2 * 1) * 0.5, 5)
else:
    A6 = 0
    A4 = round((H_ /1 - A1 * H - A2 * 5) * 0.5, 5)
    if (A1 * O + A2 * 1 + A4 * 1 - O_ /16 - A6 * 1) > 0:
        A3 = 0 
        A7 = round((A1 * O + A2 * 1 - O_ /16 - A6 * 1) * 0.5, 5)
    else:
        A7 = 0
        A3 = round((O_ /16 + A6 * 1 - A1 * O - A2 * 1) * 0.5, 5)

if A3 == 0:
    if A4 == 0:
        print('Anabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH  = {} C{}H{}N{}O{} + {} H20 + {} O2'.format(
            C, H, O, A1, C, H, O, A2, A5, C_, H_, N_, O_, A6, A7)
        )
    else:
        print('Anabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH + {} H2O  = {} C{}H{}N{}O{} + {} O2'.format(
            C, H, O, A1, C, H, O, A2, A4, A5, C_, H_, N_, O_, A7)
        )
else:
    if A4 == 0:
        print('Anabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH + {} O2 = {} C{}H{}N{}O{} + {} H20'.format(
            C, H, O, A1, C, H, O, A2, A3, A5, C_, H_, N_, O_, A6)
        )
    else:
        print('Anabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH + {} O2 +{} H2O = {} C{}H{}N{}O{}'.format(
            C, H, O, A1, C, H, O, A2, A3, A4, A5, C_, H_, N_, O_, A6)
        )
#Catabolism
K1 = 1
K3 = K1 * C
K4 = K1 * H * 0.5
if K1 > (K3 * 2 + K4 * 1):
    K5 = K1 * O - (K3 * 2 + K4 * 1) /2
else:
    K2 = ((K3 * 2 + K4 * 1) - K1 * O) /2

if K1 > (K3 * 2 + K4 * 1):
    print('Catabolism of C{}H{}O{} : {}X C{}H{}O{} = {}X CO2 + {}X H2O + {}X O2'.format(C, H, O, int(K1), C, H, O, int(K3), int(K4), K5))
else:
    print('Catabolism of C{}H{}O{} : {}X C{}H{}O{} + {}X O2 = {}X CO2 + {}X H2O'.format(C, H, O, int(K1), C, H, O, K2, int(K3), int(K4)))

#Metabolism 
if (A3 + K2) > (A7 + K5):
    if A4 > (A6 + K4):
        print('Metabolism of C{}H{}O{} : {}X+{} C{}H{}O{} + {} NH4OH + {}X+{} O2 + {}-{}X H2O = {} C{}H{}N{}O{} + {}X CO2'.format(
            C, H, O, K1, A1, C, H, O, A2, K2, A3, A4, K4, A5, C_, H_, N_, O_, K3)
        )
    else:
        print('Metabolism of C{}H{}O{} : {}X+{} C{}H{}O{} + {} NH4OH + {}X+{} O2 = {} C{}H{}N{}O{} + {}X CO2 + {}X+{} H2O'.format(
            C, H, O, K1, A1, C, H, O, A2, K2, A3, A5, C_, H_, N_, O_, K3, K4, A6)
        )
else:
    if A4 > (A6 + K4):
        print('Metabolism of C{}H{}O{} : {}X+{} C{}H{}O{} + {} NH4OH + {}-{}X H2O = {} C{}H{}N{}O{} + {}X CO2 + {}X+{} O2'.format(
            C, H, O, K1, A1, C, H, O, A2, A4, K4, A5, C_, H_, N_, O_, K3, K5, A7)
        )
    else:
        print('Metabolism of C{}H{}O{} : {}X+{} C{}H{}O{} + {} NH4OH = {} C{}H{}N{}O{} + {}X CO2 + {}X+{} H2O + {}X-{} O2'.format(
            C, H, O, K1, A1, C, H, O, A2, C, H, O, A5, C_, H_, N_, O_, K3, K4, A6, K5, A7)
        )
  
ΔG1 = args.G_C_alt_source#C source

ΔG_of_reaction_alt_C = 0
ΔG_of_reaction_alt_CX = 0
if (round(A3, 5) + round(K2, 5)) > (round(A7, 5) + round(K5, 5)):
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        ΔG_of_reaction_alt_CX = round(K3 * ΔG7 + K2 * ΔG4 - K4 * ΔG3 - K1 * ΔG1, 5)
        ΔG_of_reaction_alt_C = round(- A4 * ΔG4 -  A3 * ΔG3 - A1 * ΔG1, 5)
        print('ΔG(reaction with alternative C) = ΔG(ADB) + ΔGdissipation + {}X + {} kJ/mol'.format(ΔG_of_reaction_alt_CX, ΔG_of_reaction_alt_C))
    else:
        ΔG_of_reaction_alt_CX = round(K3 * ΔG7 + K4 * ΔG6 - K2 * ΔG3 - K1 * ΔG1, 5)
        ΔG_of_reaction_alt_C = round(A6 * ΔG6 + A3 * ΔG3 - A1 * ΔG1, 5)
        print('ΔG(reaction with alternative C) = ΔG(ADB) + ΔGdissipation + {}X + {} kJ/mol'.format(ΔG_of_reaction_alt_CX, ΔG_of_reaction_alt_C))
else:
    if round(A4, 5) > (round(A6, 5) + round(K4, 5)):
        ΔG_of_reaction_alt_CX = round(K5 * ΔG8 + K3 * ΔG7 + K4 * ΔG4 - K1 * ΔG1, 5)
        ΔG_of_reaction_alt_C =  round(A7 * ΔG8 - A4 *ΔG4 - A1 * ΔG1, 5)
        print('ΔG(reaction with alternative C) = ΔG(ADB) + ΔGdissipation + {}X + {} kJ/mol'.format(ΔG_of_reaction_alt_CX, ΔG_of_reaction_alt_C))
    else:
        ΔG_of_reaction_alt_CX = round(K3 * ΔG7 + K5 * ΔG6 + K5 * ΔG8 - K1 * ΔG1, 5)
        ΔG_of_reaction_alt_C = round(- A7* ΔG6 + A6 * ΔG8 - A1 * ΔG1, 5)
        print('ΔG(reaction with alternative C) = ΔG(ADB) + ΔGdissipation + {}X + {} kJ/mol'.format(ΔG_of_reaction_alt_CX, ΔG_of_reaction_alt_C))

x = round((ΔG_of_reaction - ΔG_of_reaction_alt_C) /ΔG_of_reaction_alt_CX, 5)

#True Catabolism
if K1 > (K3 * 2 + K4 * 1):
    print('Catabolism of C{}H{}O{} : {} C{}H{}O{} = {} CO2 + {} H2O + {} O2'.format(
        C, H, O, round(int(K1) * x, 5), C, H, O, round(int(K3) * x, 5), round(int(K4) * x, 5), round(K5 * x, 5))
    )
else:
    print('Catabolism of C{}H{}O{} : {} C{}H{}O{} + {} O2 = {} CO2 + {} H2O'.format(
        C, H, O, round((int(K1) * x), 5), C, H, O, round(K2 * x, 5), round(int(K3) * x, 5), round(int(K4) * x, 5))
    )

#True Metabolism
if (A3 + K2) > (A7 + K5):
    if A4 > (A6 + K4):
        print('Metabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH + {} O2 + {} H2O = {} C{}H{}N{}O{} + {} CO2'.format(
            C, H, O, round(K1 * x + A1, 5), C, H, O, A2, round(K2 * x + A3, 5), round(A4 - K4 * x, 5), A5, C_, H_, N_, O_, round(K3 * x, 5))
        )
    else:
        print('Metabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH + {} O2 = {} C{}H{}N{}O{} + {} CO2 + {} H2O'.format(
            C, H, O, round(K1 * x + A1, 5), C, H, O, A2, round(K2 * x + A3, 5), A5, C_, H_, N_, O_, round(K3 * x, 5), round(K4 * x + A6, 5))
        )
else:
    if A4 > (A6 + K4):
        print('Metabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH + {} H2O = {} C{}H{}N{}O{} + {} CO2 + {} O2'.format(
            C, H, O, round(K1 * x + A1 , 5), C, H, O, round(A2, 5), round(A4 - x * K4), A5, C_, H_, N_, O_, round(K3 * x, 5), round(K5 * x + A7, 5))
        )
    else:
        print('Metabolism of C{}H{}O{} : {} C{}H{}O{} + {} NH4OH = {} C{}H{}N{}O{} + {} CO2 + {} H2O + {} O2'.format(
            C, H, O, round(K1 * x + A1, 5), C, H, O, A2, C, H, O, A5, C_, H_, N_, O_, round(K3 * x, 5), round(K4 * x + round(A6, 5), 5), round(K5 * x - round(A7, 5), 5))
        )
