from bdfv5 import BdfA
ob=BdfA('../s01.bdf')
# ob=BdfA('./OpenBCI-Datos-Genericos/OpenBCI-BDF-2019-02-16_19-50-38.bdf')
ob.infor()
ob.filtros()
ob.plots()
ob.teventos()
# ob.clasificacion()