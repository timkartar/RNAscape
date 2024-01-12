remove solvent
select n. zn+
remove sele
select n. na+
remove sele
select NA, resn DA+DC+DG+DT+PSD+A+C+G+U
select INT, interface
select PRO, not NA or INT
hide cartoon, PRO
show surface, PRO
select PRO_INT, br. PRO within 5 of NA
show sticks, PRO_INT
set cartoon_ring_mode, 3
set cartoon_nucleic_acid_color, salmon
select AT, resn DA+DT+A+U
select CG, resn DC+DG+C+G
set cartoon_ring_color, palegreen, AT
set cartoon_ring_color, lightblue, CG
split_chain
set transparency, 0.7
set surface_color, grey90
set cartoon_color, grey90
set stick_color, grey90
set specular, 0
set ray_trace_mode, 3
set ray_trace_color, black
