In the location of the cs5110Final.py run the command:

python cs5110Final.py --U (9 u facelet colors) --D (9 d facelet colors) ...

The faces can be input in any order.  The colors are the first character of the color.

R - red
B - blue
G - green
W - white
O - orange
Y - yellow

The order that the facelets are input are as follows

            ----------
           | U1 U2 U3 |
           | U4 U5 U6 |
           | U7 U8 U9 |
 ---------- ---------- ---------- ----------
| L1 L2 L3 | F1 F2 F3 | R1 R2 R3 | B1 B2 B3 |
| L4 L5 L6 | F4 F5 F6 | R4 R5 R6 | B4 B5 B6 |
| L7 L8 L9 | F7 F8 F9 | R7 R8 R9 | B7 B8 B9 |
 ---------- ---------- ---------- ----------
           | D1 D2 D3 |
           | D4 D5 D6 |
           | D7 D8 D9 |
            ----------

An example input for a fully defined cube to check for validity is:

python cs5110Final.py --U BOWWRGGGG --F ROOGWOWRW --R YRBYGBBYO --D RBRYORYOG --B OWRWYGWBB --L YRYYBWOBG

If there are facelets that unknown then ? can be used to represent the unknown locations for example:

python cs5110Final.py --U BOWWRG??G --F ??OGWOW?W --R YR?YGBBYO --D RB??ORYOG --B ???WYGW?B --L YRYYBWOB?

The output with display all of the valid cubes given the input.  If there are no valid solutions then it will display unsat.