from z3 import *
import sys
import string
import argparse

NUMBER_OF_CORNER_CUBIES = 8
NUMBER_OF_EDGE_CUBIES   = 12
NUMBER_OF_FACELETS      = 54
NUMBER_OF_FACES         = 6
NUMBER_OF_FACELETS_PER_FACE = 9
U_CENTER_FACELET_INDEX = 4
D_CENTER_FACELET_INDEX = 13
L_CENTER_FACELET_INDEX = 22
R_CENTER_FACELET_INDEX = 31
F_CENTER_FACELET_INDEX = 40
B_CENTER_FACELET_INDEX = 49
CENTER_FACELET_INDEX_LIST = [U_CENTER_FACELET_INDEX, D_CENTER_FACELET_INDEX, L_CENTER_FACELET_INDEX,
                             R_CENTER_FACELET_INDEX, F_CENTER_FACELET_INDEX, B_CENTER_FACELET_INDEX]
U_FACE_INDEX = 0
D_FACE_INDEX = 1
L_FACE_INDEX = 2
R_FACE_INDEX = 3
F_FACE_INDEX = 4
B_FACE_INDEX = 5

U_FACELET_START_INDEX = 0
U_FACELET_END_INDEX   = 9
D_FACELET_START_INDEX = 9
D_FACELET_END_INDEX   = 18
L_FACELET_START_INDEX = 18
L_FACELET_END_INDEX   = 27
R_FACELET_START_INDEX = 27
R_FACELET_END_INDEX   = 36
F_FACELET_START_INDEX = 36
F_FACELET_END_INDEX   = 45
B_FACELET_START_INDEX = 45
B_FACELET_END_INDEX   = 53

# Corner facelet locations
cornerFacelets = [
	[ 8,  27, 38 ],		# URF
	[ 6,  36, 20 ],		# UFL
	[ 0,  18, 47 ],		# ULB
	[ 2,  45, 29 ],		# UBR
	[ 11, 44, 33 ],		# DFR
	[  9, 26, 42 ],		# DLF
	[ 15, 53, 24 ],		# DBL
	[ 17, 35, 51 ] ]	# DRB

# # Edge facelet locations
edgeFacelets = [
	[  7, 37 ],		# UF
	[  3, 19 ],		# UL
	[  1, 46 ],		# UB
	[  5, 28 ],		# UR
	[ 10, 43 ],		# DF
	[ 12, 25 ],		# DL
	[ 16, 52 ],		# DB
	[ 14, 34 ],		# DR
	[ 30, 41 ],		# RF
	[ 23, 39 ],		# LF
	[ 21, 50 ],		# LB
	[ 32, 48 ] ]	# RB

def isValidCharacter(chararacter):
	if character != 'R' and character != 'B' and character != 'W' and \
	   character != 'Y' and character != 'G' and character != 'O' and character != '?':
		return False
	else:
		return True

def validateCube(faceletList):
	cubeSolver = Solver()

	faceletValues = []
	for x in range(NUMBER_OF_FACELETS):
		faceletValues.append(Int("F" + str(x)))

	for x in range(NUMBER_OF_FACELETS):
		if(faceletList[x] == faceletList[U_CENTER_FACELET_INDEX] and faceletList[U_CENTER_FACELET_INDEX] != '?'):
			cubeSolver.add( faceletValues[x] == U_FACE_INDEX )
		elif(faceletList[x] == faceletList[D_CENTER_FACELET_INDEX] and faceletList[D_CENTER_FACELET_INDEX] != '?'):
			cubeSolver.add( faceletValues[x] == D_FACE_INDEX )
		elif(faceletList[x] == faceletList[L_CENTER_FACELET_INDEX] and faceletList[L_CENTER_FACELET_INDEX] != '?'):
			cubeSolver.add( faceletValues[x] == L_FACE_INDEX )
		elif(faceletList[x] == faceletList[R_CENTER_FACELET_INDEX] and faceletList[R_CENTER_FACELET_INDEX] != '?'):
			cubeSolver.add( faceletValues[x] == R_FACE_INDEX )
		elif(faceletList[x] == faceletList[F_CENTER_FACELET_INDEX] and faceletList[F_CENTER_FACELET_INDEX] != '?'):
			cubeSolver.add( faceletValues[x] == F_FACE_INDEX )
		elif(faceletList[x] == faceletList[B_CENTER_FACELET_INDEX] and faceletList[B_CENTER_FACELET_INDEX] != '?'):
			cubeSolver.add( faceletValues[x] == B_FACE_INDEX )
		#else: Don't add any constraints for unknown faces
	## Each center is distinct
	cubeSolver.add(Distinct([faceletValues[centerIndex] for centerIndex in CENTER_FACELET_INDEX_LIST]))

	for x in range(NUMBER_OF_FACELETS):
		cubeSolver.add(faceletValues[centerIndex] >= 0)
		cubeSolver.add(faceletValues[centerIndex] < NUMBER_OF_FACES)

	## Check for opposite colors of centers
	# for x in range(NUMBER_OF_FACES / 2):
	# 	if faceletIntList[x*18 + 4] % 2 == 0:
	# 		cubeSolver.add( faceletValues[(x*18 + 4) + 9] == faceletValues[x*18 + 4] + 1)
	# 	else:
	# 		cubeSolver.add( faceletValues[(x*18 + 4) + 9] == faceletValues[x*18 + 4] - 1)
	
	## Check UFL Centers to see if they are valid relative to eachother
	# if faceletIntList[4] == 0 or faceletIntList[4] == 3 or faceletIntList[4] == 4:
	# 	if faceletIntList[22] > faceletIntList[40]:
	# 		cubeSolver.add((faceletValues[22] - faceletValues[40]) % 2 == 1) # is even
	# 	else:
	# 		cubeSolver.add((faceletValues[40] - faceletValues[22]) % 2 == 0) # is odd
	# else:# faceletIntList[4] % 2 == 1:
	# 	if faceletIntList[22] > faceletIntList[40]:
	# 		cubeSolver.add((faceletValues[22] - faceletValues[40]) % 2 == 0) # is even
	# 	else:
	# 		cubeSolver.add((faceletValues[40] - faceletValues[22]) % 2 == 1) # is odd

	## Check for distinct edge cubies
	for edge in edgeFacelets:
		cubeSolver.add(Distinct([faceletValues[edge[0]],faceletValues[edge[1]]]))

	cubeSolver.add(Distinct([faceletValues[edge[0]] * faceletValues[edge[0]] * faceletValues[edge[0]] + faceletValues[edge[1]] * faceletValues[edge[1]] * faceletValues[edge[1]] for edge in edgeFacelets]))

	## Check for distnct corner cubies
	for corner in cornerFacelets:
		cubeSolver.add(Distinct([faceletValues[corner[0]],faceletValues[corner[1]], faceletValues[corner[2]]]))
 
	cubeSolver.add(Distinct([faceletValues[corner[0]] * faceletValues[corner[0]] * faceletValues[corner[0]] + faceletValues[corner[1]] * faceletValues[corner[1]] * faceletValues[corner[1]] + faceletValues[corner[2]] * faceletValues[corner[2]] * faceletValues[corner[2]] for corner in cornerFacelets]))

	# Valid corner orientation combination
	cornerOrientationValues = []
	for x in range(NUMBER_OF_CORNER_CUBIES):
		cornerOrientationValues.append(Int("CO" + str(x)))

	for x in range(NUMBER_OF_CORNER_CUBIES):
		cubeSolver.add(cornerOrientationValues[x] == If(Or(faceletValues[cornerFacelets[x][0]] == faceletValues[U_CENTER_FACELET_INDEX], faceletValues[cornerFacelets[x][0]] == faceletValues[D_CENTER_FACELET_INDEX]), 0, \
					                                 If(Or(faceletValues[cornerFacelets[x][1]] == faceletValues[U_CENTER_FACELET_INDEX], faceletValues[cornerFacelets[x][1]] == faceletValues[D_CENTER_FACELET_INDEX]), 1, 2)))
		cubeSolver.add(cornerOrientationValues[x] >= 0)
		cubeSolver.add(cornerOrientationValues[x] < 3)

	cubeSolver.add((cornerOrientationValues[0] + cornerOrientationValues[1] + cornerOrientationValues[2] + cornerOrientationValues[3] + cornerOrientationValues[4] + cornerOrientationValues[5] + cornerOrientationValues[6] + cornerOrientationValues[7]) % 3 == 0)

	# Valid edge orientation combination
	edgeOrientationValues = []
	for x in range(NUMBER_OF_EDGE_CUBIES):
		edgeOrientationValues.append(Int("EO" + str(x)))

	for x in range(NUMBER_OF_EDGE_CUBIES):
		cubeSolver.add(edgeOrientationValues[x] == If(Or(faceletValues[edgeFacelets[x][0]] == faceletValues[U_CENTER_FACELET_INDEX], faceletValues[edgeFacelets[x][0]] == faceletValues[D_CENTER_FACELET_INDEX]), 0, \
					                               If(Or(faceletValues[edgeFacelets[x][1]] == faceletValues[U_CENTER_FACELET_INDEX], faceletValues[edgeFacelets[x][1]] == faceletValues[D_CENTER_FACELET_INDEX]), 1, \
					                               If(Or(faceletValues[edgeFacelets[x][0]] == faceletValues[R_CENTER_FACELET_INDEX], faceletValues[edgeFacelets[x][0]] == faceletValues[L_CENTER_FACELET_INDEX]), 0, 1))))
		cubeSolver.add(edgeOrientationValues[x] >= 0)
		cubeSolver.add(edgeOrientationValues[x] < 2)

	cubeSolver.add((edgeOrientationValues[0] + edgeOrientationValues[1] + edgeOrientationValues[2] + edgeOrientationValues[3] + edgeOrientationValues[4] + edgeOrientationValues[5] + edgeOrientationValues[6] + edgeOrientationValues[7] + edgeOrientationValues[8] + edgeOrientationValues[9] + edgeOrientationValues[10] + edgeOrientationValues[11]) % 2 == 0)

	cornerPositionValues = []
	for x in range(NUMBER_OF_CORNER_CUBIES):
		cornerPositionValues.append(Int("CP" + str(x)))

	for x in range(NUMBER_OF_CORNER_CUBIES):
		cubeSolver.add(cornerPositionValues[x] == If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX + R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX), 0, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX + L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX), 1, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX + L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX), 2, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX + R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX), 3, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX + R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX), 4, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX + L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX), 5, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX + L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX), 6, \
			If((faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] * faceletValues[cornerFacelets[x][0]] + faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] * faceletValues[cornerFacelets[x][1]] + faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] * faceletValues[cornerFacelets[x][2]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX + R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX), 7, -1 )))))))))
		cubeSolver.add(cornerPositionValues[x] >= 0)

	edgePositionValues = []
	for x in range(NUMBER_OF_EDGE_CUBIES):
		edgePositionValues.append(Int("EP" + str(x)))

	for x in range(NUMBER_OF_EDGE_CUBIES):
		cubeSolver.add(edgePositionValues[x] == If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX), 0, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX), 1, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX), 2, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == U_FACE_INDEX * U_FACE_INDEX * U_FACE_INDEX + R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX), 3, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX), 4, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX), 5, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX), 6, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == D_FACE_INDEX * D_FACE_INDEX * D_FACE_INDEX + R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX), 7, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX), 8, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX + F_FACE_INDEX * F_FACE_INDEX * F_FACE_INDEX), 9, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == L_FACE_INDEX * L_FACE_INDEX * L_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX), 10, \
			If((faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] * faceletValues[edgeFacelets[x][0]] + faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] * faceletValues[edgeFacelets[x][1]] == R_FACE_INDEX * R_FACE_INDEX * R_FACE_INDEX + B_FACE_INDEX * B_FACE_INDEX * B_FACE_INDEX), 11, -1 )))))))))))))
		cubeSolver.add(edgePositionValues[x] >= 0)

	for x in range(NUMBER_OF_CORNER_CUBIES):
		cubeSolver.add(Or(faceletValues[cornerFacelets[x][0]] == If((cornerOrientationValues[x] == 0),                                                                                                                                faceletValues[U_CENTER_FACELET_INDEX], \
			                                                     If((cornerOrientationValues[x] == 1), If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[F_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[L_CENTER_FACELET_INDEX]),
			                                                  										   If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[L_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[F_CENTER_FACELET_INDEX]))), \
                          faceletValues[cornerFacelets[x][0]] == If((cornerOrientationValues[x] == 0),                                                                                                                                faceletValues[D_CENTER_FACELET_INDEX], \
			                                                     If((cornerOrientationValues[x] == 1), If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[B_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[R_CENTER_FACELET_INDEX]), \
			                                                  										   If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[R_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[B_CENTER_FACELET_INDEX])))))

		cubeSolver.add(Or(faceletValues[cornerFacelets[x][1]] == If((cornerOrientationValues[x] == 1),                                                                                                                                faceletValues[U_CENTER_FACELET_INDEX], \
			                                                     If((cornerOrientationValues[x] == 2), If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[F_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[L_CENTER_FACELET_INDEX]), \
			                                                  										   If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[L_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[F_CENTER_FACELET_INDEX]))), \
                          faceletValues[cornerFacelets[x][1]] == If((cornerOrientationValues[x] == 1),                                                                                                                                faceletValues[D_CENTER_FACELET_INDEX], \
			                                                     If((cornerOrientationValues[x] == 2), If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[B_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[R_CENTER_FACELET_INDEX]), \
			                                                  										   If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[R_CENTER_FACELET_INDEX], \
			                                                  										   				                                                                                                                  faceletValues[B_CENTER_FACELET_INDEX])))))
		cubeSolver.add(Or(faceletValues[cornerFacelets[x][2]] == If((cornerOrientationValues[x] == 2),                                                                                                                                faceletValues[U_CENTER_FACELET_INDEX], \
			                                                     If((cornerOrientationValues[x] == 0), If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[F_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[L_CENTER_FACELET_INDEX]), \
			                                                  										   If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[L_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[F_CENTER_FACELET_INDEX]))), \
                          faceletValues[cornerFacelets[x][2]] == If((cornerOrientationValues[x] == 2),                                                                                                                                faceletValues[D_CENTER_FACELET_INDEX], \
			                                                     If((cornerOrientationValues[x] == 0), If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[B_CENTER_FACELET_INDEX], \
			                                                                                                                                                                                                                          faceletValues[R_CENTER_FACELET_INDEX]), \
			                                                  										   If(Or(cornerPositionValues[x] == 0, cornerPositionValues[x] == 2, cornerPositionValues[x] == 5, cornerPositionValues[x] == 7), faceletValues[R_CENTER_FACELET_INDEX], \
			                                                  										   				                                                                                                                  faceletValues[B_CENTER_FACELET_INDEX])))))
	# for x in range(NUMBER_OF_EDGE_CUBIES):
	# 	cubeSolver.add(Or(faceletValues[edgeFacelets[x][0]] == If((edgeOrientationValues[x] == 0), faceletValues[U_CENTER_FACELET_INDEX], \
	# 		                                                                                       faceletValues[F_CENTER_FACELET_INDEX]), \
	# 					  faceletValues[edgeFacelets[x][0]] == If((edgeOrientationValues[x] == 0), faceletValues[D_CENTER_FACELET_INDEX], \
	# 		                                                                                       faceletValues[B_CENTER_FACELET_INDEX]), \
	# 					  faceletValues[edgeFacelets[x][0]] == faceletValues[L_CENTER_FACELET_INDEX], \
	# 					  faceletValues[edgeFacelets[x][0]] == faceletValues[R_CENTER_FACELET_INDEX])) 

 #        cubeSolver.add(Or(faceletValues[edgeFacelets[x][1]] == If((edgeOrientationValues[x] == 0), faceletValues[U_CENTER_FACELET_INDEX], \
	# 		                                                                                       faceletValues[F_CENTER_FACELET_INDEX]), \
	# 					  faceletValues[edgeFacelets[x][1]] == If((edgeOrientationValues[x] == 0), faceletValues[D_CENTER_FACELET_INDEX], \
	# 		                                                                                       faceletValues[B_CENTER_FACELET_INDEX]), \
	# 					  faceletValues[edgeFacelets[x][1]] == faceletValues[L_CENTER_FACELET_INDEX], \
	# 					  faceletValues[edgeFacelets[x][1]] == faceletValues[R_CENTER_FACELET_INDEX])) 

    # Edge Corner Position Parity
	CPPs = []
	for x in range(NUMBER_OF_CORNER_CUBIES - 1):
		CPPs.append(Int("CPP" + str(x)))

	for x in range(NUMBER_OF_CORNER_CUBIES - 1):
		compareList = []
		for y in range(x + 1, NUMBER_OF_CORNER_CUBIES):
			compareList.append(If((cornerPositionValues[x] < cornerPositionValues[y]), 1, 0))
		cubeSolver.add(CPPs[x] == Sum(compareList))

	cubeSolver.add(Int('CPPTotal') == Sum(CPPs))

	EPPs = []
	for x in range(NUMBER_OF_EDGE_CUBIES - 1):
		EPPs.append(Int("EPP" + str(x)))

	for x in range(NUMBER_OF_EDGE_CUBIES - 1):
		compareList = []
		for y in range(x + 1, NUMBER_OF_EDGE_CUBIES):
			compareList.append(If((edgePositionValues[x] < edgePositionValues[y]), 1, 0))
		cubeSolver.add(EPPs[x] == Sum(compareList))

	cubeSolver.add(Int('EPPTotal') == Sum(EPPs))

	cubeSolver.add(Int('CPPTotal') % 2 == Int('EPPTotal') % 2)

 	# Print Assertions
	# for c in cubeSolver.assertions():
	# 	print c

	output = cubeSolver.check()

	if output == sat:
		inputCubeString = "U:" + ''.join(faceletList[0:9])  + \
				             " D:" + ''.join(faceletList[9:18]) + \
				             " L:" + ''.join(faceletList[18:27]) + \
				             " R:" + ''.join(faceletList[27:36]) + \
				             " F:" + ''.join(faceletList[36:45]) + \
				             " B:" + ''.join(faceletList[45:54])
		print "Input -   \t" + inputCubeString
		numberOfSolutions = 0
		foundAll = False 
		while not foundAll:
			numberOfSolutions += 1
			solutionList = []
			model = cubeSolver.model()

			modelString = str(model)
			#print model
			
			solutionString = "U:"
			for x in range(NUMBER_OF_FACELETS):
				if x == 9:
					solutionString += " D:"
				elif x == 18:
					solutionString += " L:"
				elif x == 27:
					solutionString += " R:"
				elif x == 36:
					solutionString += " F:"
				elif x == 45:
					solutionString += " B:"

				faceletInt = int(modelString.split("F" + str(x) + " = ")[1][0])

				if faceletInt == 0:
					solutionString += faceletList[U_CENTER_FACELET_INDEX]
					solutionList.append(0)
				elif faceletInt == 1:
					solutionString += faceletList[D_CENTER_FACELET_INDEX]
					solutionList.append(1)
				elif faceletInt == 2:
					solutionString += faceletList[L_CENTER_FACELET_INDEX]
					solutionList.append(2)
				elif faceletInt == 3:
					solutionString += faceletList[R_CENTER_FACELET_INDEX]
					solutionList.append(3)
				elif faceletInt == 4:
					solutionString += faceletList[F_CENTER_FACELET_INDEX]
					solutionList.append(4)
				elif faceletInt == 5:
					solutionString += faceletList[B_CENTER_FACELET_INDEX]
					solutionList.append(5)
			print "Output " + str(numberOfSolutions) + " -\t" + solutionString

			cubeSolver.add(Int('Check' + str(numberOfSolutions)) == And([Int('F' + str(x)) == solutionList[x] for x in range(NUMBER_OF_FACELETS)]))
			cubeSolver.add(Int('Check' + str(numberOfSolutions)) == 0)

			#Print Assertions
			# for c in cubeSolver.assertions():
			# 	print c

			check = cubeSolver.check()
			if check != sat:
				foundAll = True
	else:
		print "Invalid - " + str(output)
		exit()
	print "Found " + str(numberOfSolutions) + " Solution(s)"

def verifyFaceletCount(Face, FaceSideString):
	if len(Face) != NUMBER_OF_FACELETS_PER_FACE:
  		if len(Face) > NUMBER_OF_FACELETS_PER_FACE:
  			print("Too many facelets for " + FaceSideString + " side")
  			exit()
  		else:
  			print("Too few faclets for " + FaceSideString + " side")
  			exit()

# main entry point for this script
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="""Z3 Cube Verifier""")

	parser.add_argument("--U", action="store", type= str, default= "", required= True, help="Input Up side cubies")
	parser.add_argument("--F", action="store", type= str, default= "", required= True, help="Input Front side cubies")
	parser.add_argument("--R", action="store", type= str, default= "", required= True, help="Input Right side cubies")
	parser.add_argument("--D", action="store", type= str, default= "", required= True, help="Input Down side cubies")
	parser.add_argument("--B", action="store", type= str, default= "", required= True, help="Input Back side cubies")
	parser.add_argument("--L", action="store", type= str, default= "", required= True, help="Input Left side cubies")

  	args = parser.parse_args()

#Verify that the correct number of facelets is given

	try:
		verifyFaceletCount(args.U, "Up") 
		verifyFaceletCount(args.F, "Front") 
		verifyFaceletCount(args.R, "Right") 
		verifyFaceletCount(args.D, "Down") 
		verifyFaceletCount(args.B, "Back") 
		verifyFaceletCount(args.L, "Left") 

		UList = list(args.U)
		FList = list(args.F)
		RList = list(args.R)
		DList = list(args.D)
		BList = list(args.B)
		LList = list(args.L)

		for character in (UList + DList + LList + RList + FList + BList):
			if not isValidCharacter(character):
				print "Invalid character " + str(character)
				exit()

		validateCube(UList + DList + LList + RList + FList + BList)
	except KeyboardInterrupt:
		print "Aborted Gracefully!"
