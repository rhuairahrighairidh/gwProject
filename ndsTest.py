import nds2
conn=nds2.connection('nds.ligo-wa.caltech.edu',31200)
print conn

buf = conn.fetch(1024417918, 1024417919, 'H1:PSL-ISS_PDA_OUT_DQ')#,'H1:PSL_ISS_PDB_OUT_DQ'])

print buf
#'H1:PSL_ISS_PDB_OUT_DQ'
