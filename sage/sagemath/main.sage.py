# This file was *autogenerated* from the file main.sage
from sage.all_cmdline import *   # import sage library
_sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_1p67 = RealNumber('1.67'); _sage_const_2p5 = RealNumber('2.5'); _sage_const_4 = Integer(4); _sage_const_1p0 = RealNumber('1.0'); _sage_const_1p36 = RealNumber('1.36'); _sage_const_8 = Integer(8); _sage_const_1p5 = RealNumber('1.5'); _sage_const_0p40 = RealNumber('0.40'); _sage_const_0p67 = RealNumber('0.67'); _sage_const_10 = Integer(10); _sage_const_100 = Integer(100); _sage_const_1p = RealNumber('1.'); _sage_const_0p55 = RealNumber('0.55'); _sage_const_0p4 = RealNumber('0.4'); _sage_const_15 = Integer(15); _sage_const_0p6 = RealNumber('0.6'); _sage_const_0p10 = RealNumber('0.10'); _sage_const_0p05 = RealNumber('0.05')
"""@package docstring
This module contain code to process the data
obtain from input.sage
"""


def funSaog(soilType, timePrd):
  """
  function to pick values according to
  type of soil selected
  ...
  """
  t1 = _sage_const_0 ; t2 = _sage_const_0 ; t3 = _sage_const_0 ; t4 = _sage_const_0 
  eq3num = _sage_const_0 
  t2 = _sage_const_0p10 
  if(soilType=='I'):
      t3 = _sage_const_0p40 ; eq3num = _sage_const_1p0 
  elif (soilType=='II'):
      t3 = _sage_const_0p55 ; eq3num = _sage_const_1p36 
  elif(soilType=='III'):
      t3 = _sage_const_0p67 ; eq3num = _sage_const_1p67 
  else:
      Print('Unexpected soil type')
  if (timePrd < t2):
      sag = _sage_const_1p  + _sage_const_15  * timePrd
  elif(timePrd > t3):
      sag = eq3num / timePrd
  else:
      sag = _sage_const_2p5 
  return sag

"""main program ... """
#loading input variables from input.sage
load('input.sage')
#changing style of brackets for latex output
latex.matrix_delimiters("[","]")

#converting mass in diagonal matrix
Mass=matrix(Number_of_storeys,Number_of_storeys)
for i in range(Number_of_storeys):
    for j in range(Number_of_storeys):
        if(i==j):
            Mass[i,j]=mass[j,_sage_const_0 ]
        else:
            Mass[i,j]=_sage_const_0 
#calculating level of floors from its height
Level_floor=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
for storey_i in range(Number_of_storeys):
    Level_floor[storey_i,_sage_const_0 ] = Height_storey[storey_i,_sage_const_0 ]
    if(storey_i>_sage_const_0 ):
        Level_floor[storey_i,_sage_const_0 ]=(
        Level_floor[storey_i,_sage_const_0 ]+Level_floor[storey_i-_sage_const_1 ,_sage_const_0 ])

#calcutaing stiffness matrix from stiffness of storeys
Stiffness_matrix=zero_matrix(QQ,Number_of_storeys,Number_of_storeys)
for storey_i in range(Number_of_storeys):
	Stiffness_matrix[storey_i, storey_i] = Stiffness_storey[storey_i][_sage_const_0 ]
	if (storey_i < Number_of_storeys-_sage_const_1 ):
		Stiffness_matrix[storey_i, storey_i]=(
			Stiffness_matrix[storey_i, storey_i] +
			Stiffness_storey[storey_i + _sage_const_1 ][_sage_const_0 ])
		Stiffness_matrix[storey_i, storey_i + _sage_const_1 ]=(
		-Stiffness_storey[storey_i + _sage_const_1 ][_sage_const_0 ])
		Stiffness_matrix[storey_i + _sage_const_1 , storey_i]=(
		Stiffness_matrix[storey_i, storey_i + _sage_const_1 ])
#calculating eginvalues
w=var('w')
q=Stiffness_matrix-(w**_sage_const_2 )*Mass
A=Stiffness_matrix*Mass.inverse()
Omega_square=A.eigenvalues()

#calculating W and time period
Omega=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
Time_period=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
for i in range( Number_of_storeys):
	q=sqrt(Omega_square[i])
	Omega[i,_sage_const_0 ]=n(q)
	Time_period[i,_sage_const_0 ]=n(_sage_const_2 *pi)/q
#Frequency=list()
#for storey_i in range(Number_of_storeys):
	#Frequency.append(sqrt(Omega_square[storey_i].n(digits=4)))
#calculating egin vectors
z=A.eigenvectors_left()

J=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
X=zero_matrix(RR,Number_of_storeys,Number_of_storeys)
for x in range(Number_of_storeys):
	q=matrix(z[x][_sage_const_1 ][_sage_const_0 ])
	mid=q*Mass*q.transpose()
	J[x,_sage_const_0 ]=n(mid[_sage_const_0 ][_sage_const_0 ])
	X[x]=matrix(q/sqrt(abs(J[x])))
#ModesContributionX = 0;
#Number_of_modes_to_be_considered = 0;
#for Number_of_modes_to_be_considered in range(Number_of_storeys):
	#ModesContributionX = ModesContributionX+Modal_contribution(Number_of_modes_to_be_considered);
 	#if (ModesContributionX > 90):
 		#break;

#calculating Modal participation factor ,sum of modal mass
#and modal mass
Modal_participation_factor=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
Modal_mass=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
sum_modal_mass=_sage_const_0 
for j in range(Number_of_storeys):
        P1,P2=_sage_const_0 ,_sage_const_0 
        m=X[j,:]
        for i in range(Number_of_storeys):
            P1=P1+Mass[i][i]*m[_sage_const_0 ][i]
            P2=P2+Mass[i][i]*(m[_sage_const_0 ][i])**_sage_const_2 
        Modal_participation_factor[j,_sage_const_0 ]=P1/P2
        Modal_mass[j,_sage_const_0 ]=(P1)**_sage_const_2 /(P2)
        sum_modal_mass = sum_modal_mass + Modal_mass[j,_sage_const_0 ]
XX=X.transpose()
#calculating modal contribution of each storey
Modal_contribution=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
for i in range(Number_of_storeys):
	Modal_contribution[i,_sage_const_0 ]=((_sage_const_100  / sum_modal_mass )*Modal_mass[i,_sage_const_0 ]).n(digits=_sage_const_4 )

#getting type of soil and dependent variables
Type_of_soil=''
for i in range (Soil_type):
   Type_of_soil = Type_of_soil+'I'
Sa_by_g=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
A_h=zero_matrix(RR,Number_of_storeys,Number_of_storeys)
for index_time in range(Number_of_storeys):
	Sa_by_g[index_time,_sage_const_0 ] = funSaog(
	Type_of_soil, Time_period[index_time,_sage_const_0 ])
 	A_h[index_time,_sage_const_1 ]= (
 	Zone_factor/_sage_const_2 *Importance_factor/
 	Response_reduction_factor * Sa_by_g[index_time,_sage_const_0 ])

#calculating design lateral force


Design_lateral_force=zero_matrix(RR,Number_of_storeys,Number_of_storeys)
for index_i in range(Number_of_storeys):
    q=Mass*XX[:,index_i]
    z=q*matrix(A_h[index_i]*Modal_participation_factor[index_i,_sage_const_0 ]*
    Gravity_acceleration)
    Design_lateral_force[: , index_i]=z[:,_sage_const_1 ]


#calculating Peak shear force
Peak_shear_force = zero_matrix(RR,Number_of_storeys, Number_of_storeys)
for index_j in range(Number_of_storeys):
	for index_i in range(Number_of_storeys):
		for index_k in range(Number_of_storeys - index_i ):
			Peak_shear_force[index_i,index_j]=(
			Design_lateral_force[index_k + index_i,index_j] +
			 Peak_shear_force[index_i,index_j])


#storey shear force for all modes
Storey_shear_force = zero_matrix(RR,Number_of_storeys,_sage_const_1 )
Storey_shear_force2 = zero_matrix(RR,Number_of_storeys,_sage_const_1 )
if (Modes_considered == _sage_const_0 ):
  Modes_considered = Number_of_modes_to_be_considered
for index_i in range(Number_of_storeys):
    for index_j in range(Modes_considered):
        Storey_shear_force[index_i,_sage_const_0 ]=(Storey_shear_force[index_i,_sage_const_0 ]+
        abs(Peak_shear_force[index_i,index_j]))
        Storey_shear_force2[index_i,_sage_const_0 ]=(Storey_shear_force2[index_i,_sage_const_0 ]+
        Peak_shear_force[index_i,index_j]**_sage_const_2 )
    Storey_shear_force2[index_i,_sage_const_0 ] = sqrt(Storey_shear_force2[index_i,_sage_const_0 ])
P=zero_matrix(RR,Number_of_storeys,Number_of_storeys)
B=zero_matrix(RR,Number_of_storeys,Number_of_storeys)
for i in range(Number_of_storeys):
	for j in range(Number_of_storeys):
		q=Omega[i,_sage_const_0 ]
		r=Omega[j,_sage_const_0 ]
		B[i,j]=(r/q)
B=B.n(digits=_sage_const_4 )

for i in range(Number_of_storeys):
	for j in range(Number_of_storeys):
		b=_sage_const_1 +B[i,j]
		q=_sage_const_8 *(_sage_const_0p05 )**_sage_const_2 *(b)*B[i,j]**_sage_const_1p5 
		e=(_sage_const_1 -B[i,j]**_sage_const_2 )**_sage_const_2 +_sage_const_4 *(_sage_const_0p05 )*B[i,j]*(b)**_sage_const_2 
		P[i,j]=q/e
Lateral_force=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
for i in range(Number_of_storeys):
	l=Peak_shear_force[:,i].transpose()*P*Peak_shear_force[:,i]
	Lateral_force[i,_sage_const_0 ]=sqrt(l[_sage_const_0 ,_sage_const_0 ])
Force=zero_matrix(RR,Number_of_storeys,_sage_const_1 )
for i in range(Number_of_storeys):
	if(i==Number_of_storeys-_sage_const_1 ):
		Force[i,_sage_const_0 ]=Lateral_force[i,_sage_const_0 ]
		break
	Force[i,_sage_const_0 ]=Lateral_force[i,_sage_const_0 ]-Lateral_force[i+_sage_const_1 ,_sage_const_0 ]

#making graph for eigen vectors of calculated
p=list()
for i in range(Number_of_storeys):
	for j in range(Number_of_storeys):
		if(j==_sage_const_0 ):
			p.append(line([(XX[j,i],Level_floor[j,_sage_const_0 ]),(_sage_const_0 ,_sage_const_0 )],
			color=hue(_sage_const_0p4  + _sage_const_0p6 *(i/_sage_const_10 ))))
		else:
			p.append(line([(XX[j,i],Level_floor[j,_sage_const_0 ]),
			(XX[j-_sage_const_1 ,i],Level_floor[j-_sage_const_1 ,_sage_const_0 ])],marker='o',
			color=hue(_sage_const_0p4  + _sage_const_0p6 *(i/_sage_const_10 ))))
Graph=plot([])
for r in range(Number_of_storeys**_sage_const_2 ):
	Graph= Graph+p[r]

Omega_square=matrix(Omega_square).n(digits=_sage_const_4 )
Time_period=Time_period.n(digits=_sage_const_4 )
Omega=Omega.n(digits=_sage_const_4 )
Level_floor=(Level_floor).n(digits=_sage_const_4 )
Modal_participation_factor=(Modal_participation_factor).n(digits=_sage_const_4 )
Modal_mass=(Modal_mass).n(digits=_sage_const_4 )
Modal_contribution=Modal_contribution.n(digits=_sage_const_4 )
Sa_by_g=Sa_by_g.n(digits=_sage_const_4 )
A_h=A_h.n(digits=_sage_const_4 )
Design_lateral_force=Design_lateral_force.n(digits=_sage_const_4 )
Peak_shear_force=Peak_shear_force.n(digits=_sage_const_4 )
storey_shear_force3=Storey_shear_force[:].n(digits=_sage_const_4 )
Storey_shear_force2=Storey_shear_force2[:].n(digits=_sage_const_4 )
Lateral_force=Lateral_force.n(digits=_sage_const_4 )
Force=Force.n(digits=_sage_const_4 )
