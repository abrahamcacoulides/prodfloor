from django.utils.translation import ugettext_lazy as _

dict_m2000_new = {
    'Beginning': [['Documentacion Inicial', [None,], [None,]],
                  ['Inspeccion Visual', [None,], [None,]],
                  ['Preparacion de Labview', [None,], [None,]],
                  ['Chequeo preliminar de voltajes iniciales', [None,], [None,]]],
    'Program': [['Programacion de Flasheo', [None,], [None,]],
                ['Conexion de arneces simulador del carro y arneces cartop', ['COP'], [1]],
                ['Programacion del Firmware(Chip)', [None,], [None,]],
                ['Conexion de arneces del simulador', ['COP'], [0]],
                ['Programacion del Solid State Starter', [None,], [None,]],
                ['Programacion de parametros F1', [None,], [None,]],
                ['Programacion tarjeta CE Electronics', [None,], [None,]]],
    'Logic': [['Board power test SAFL & SAFS', [None,], [None,]],
              ['Motor Starter Test', [None,], [None,]],
              ['Valve control and limits', [None,], [None,]],
              ['Safety and inspection', [None,], [None,]],
              ['Door locks and hoistway access', [None,], [None,]],
              ['Landing system', [None,], [None,]],
              ['Door Interface (Pag CT1, CT2)', ['DCC'], [1]],
              ['COP parte 1 (Pag CPI)', ['DCC'], [1]],
              ['Door Interface (Pag 11, 11X)', ['DCC'], [0]],
              ['COP parte 1 (Pag 12)', ['DCC'], [0]],
              ['Fire Service Phase I (Pag 13)', [None,], [None,]],
              ['Fire Service Phase II (Pag 12)', ['CPI'], [0]],
              ['Movement Indication (Pag 14)', ['CPI'], [0]],
              ['Fire Service Phase II (Pag CPI)', ['CPI'], [1]],
              ['Movement Indication (Pag CPI)', ['CPI'], [1]],
              ['Car Calls (Pag CPI)', ['CPI'], [1]],
              ['Calls (Pag 16)', ['CPI'], [0]],
              ['Serial Hall Calls (Pag SH)', ['SHC'], [1]],
              ['Pruebas de entradas y salidas (Pag 15, 17, etc.)', [None,], [None,]],
              ['Flasheo de Puerto CHP y/o MPU', ['mView','iMon'], [1, 1]],
              ['Flasheo de Puerto CHP y/o MPU', ['mView','iMon'], [0, 1]],
              ['Flasheo de Puerto CHP y/o MPU', ['mView','iMon'], [1, 0]],
              ['Configuracion de PC, Imagen y Softwares', ['PC','mView','iMon'], [1, 1, 1]],
              ['Configuracion de PC, Imagen y Softwares', ['PC','mView','iMon'], [1, 0, 1]],
              ['Configuracion de PC, Imagen y Softwares', ['PC','mView','iMon'], [1, 1, 0]],
              ['Prueba de Monitoring', ['mView','iMon'], [1, 1]],
              ['Prueba de Monitoring', ['mView','iMon'], [0, 1]],
              ['Prueba de Monitoring', ['mView','iMon'], [1, 0]], ],
    'Ending': [['Inspeccion Final', [None,], [None,]],
               ['Passcode', [None,], [None,]],
               ['Papeleria Final', [None,], [None,]],
               ['Respaldo Electronico de la papeleria', [None,], [None,]],
               ['Desconnecion de Arneces', [None,], [None,]],
               ['Carro a estacion final', [None,], [None,]]],
    'Complete': [['Fin de pruebas', [None,], [None,]]],
    'Stopped': [['Detenido', [None,], [None,]]]}
dict_m4000_new = {
    'Beginning': [['Documentacion Inicial', [None], [None]],
                  ['Inspeccion Visual', [None], [None]],
                  ['Preparacion de Labview', [None], [None]],
                  ['Chequeo preliminar de voltajes iniciales', [None], [None]], ],
    'Program': [['Programacion de Flasheo', [None], [None]],
                ['Conexion de arneces simulador del carro y arneces cartop', ['COP'], [1]],  # if cartop
                ['Programacion del Firmware(Chip)', [None], [None]],
                ['Conexion de arneces del simulador', ['COP'], [0]],  # if !cartop
                ['Programacion de parametros F1', [None], [None]],
                ['Programacion de Fecha y Hora', [None], [None]],
                ['Programacion tarjeta CE Electronics', [None], [None]],
                ['Programacion de Parametros F7\n Version Test', [None], [None]],
                ['Programacion de Parametros F5\n Version Test', [None], [None]],
                ['Programacion de R6 Regen Unit', ['R6'], [1]],
                ['Programacion de F4', [None], [None]],
                ['MBRAKE Module\nCalibracion Inicial', ['MBRAKE'], [1]],
                ['Calibracion Brake Coil Discreto Final', ['MBRAKE', 'BCV'], [0, 1]],
                ['Calibracion Brake Coil Discreto Preliminar', ['MBRAKE', 'BCV'], [0, 0]],
                ['Calibracion F6 Floor Learning', [None], [None]],
                ['F7 Terminal Limits', [None], [None]], ],
    'Logic': [['Board power test SAFL & SAFS', [None], [None]],
              ['Drive Interface', [None], [None]],
              ['Emergency Brake', [None], [None]],
              ['Safety and inspection', [None], [None]],
              ['Door locks and hoistway access', [None], [None]],
              ['Landing System', [None], [None]],
              ['Door Interface (Pag CT1, CT2)', ['DCC'], [1]],  # if DCC
              ['COP parte 1 (Pag CPI)', ['DCC'], [1]],  # if DCC
              ['Door Interface (Pag 11, 11X)', ['DCC'], [0]],  # if !DCC
              ['COP parte 1 (Pag 12)', ['DCC'], [0]],  # if !DCC
              ['Fire Service Phase I (Pag 13)', [None], [None]],
              ['Fire Service Phase II (Pag 12)', ['CPI'], [0]],  # if !CPI
              ['Movement Indication (Pag 14)', ['CPI'], [0]],  # if !CPI
              ['Fire Service Phase II (Pag CPI)', ['CPI'], [1]],  # if CPI
              ['Movement Indication (Pag CPI)', ['CPI'], [1]],  # if CPI
              ['Car Calls (Pag CPI)', ['CPI'], [1]],  # if CPI
              ['Calls (Pag 16)', [None], [None]],
              ['Serial Hall Calls (Pag SH)', ['SHC'], [1]],  # if serial hall calls
              ['Pruebas de entradas y salidas (Pag 15, 17, etc.)', [None], [None]],
              ['Calibracion EMCO Board', ['EMCO','COP'], [1, 1]],
              ['Pruebas de entradas y salidas CARTOP (Pag CT1, CT2, etc.)', ['COP'], [1]],
              ['Flasheo de Puerto CHP y/o MPU', ['mView','iMon'], [1, 1]],
              ['Flasheo de Puerto CHP y/o MPU', ['mView','iMon'], [0, 1]],
              ['Flasheo de Puerto CHP y/o MPU', ['mView','iMon'], [1, 0]],
              ['Configuracion de PC, Imagen y Softwares', ['PC','mView','iMon'], [1, 1, 1]],
              ['Configuracion de PC, Imagen y Softwares', ['PC','mView','iMon'], [1, 0, 1]],
              ['Configuracion de PC, Imagen y Softwares', ['PC','mView','iMon'], [1, 1, 0]],
              ['Prueba de Monitoring', ['mView','iMon'], [1, 1]],
              ['Prueba de Monitoring', ['mView','iMon'], [0, 1]],
              ['Prueba de Monitoring', ['mView','iMon'], [1, 0]],
              ['Additional Manual Test\n(Overspeeds and Limits)', [None], [None]],
              ['MBRAKE\nCalibracion Final', ['MBRAKE'], [1]],
              ['Calibracion Brake Coil Discreto Final', ['MBRAKE','BCV'], [0, 0]],
              ['Programacion de Parametros F7\n Version Cliente', [None], [None]],
              ['Programacion de Parametros F5\n Version Cliente', [None], [None]], ],
    'Ending': [['Inspeccion Final', [None], [None]],
               ['Passcode', [None], [None]],
               ['Papeleria Final', [None], [None]],
               ['Respaldo Electronico de la papeleria', [None], [None]],
               ['Desconnecion de Arneces', [None], [None]],
               ['Carro a estacion final', [None], [None]], ],
    'Complete': [['Fin de pruebas', [None], [None]], ],
    'Stopped': [['Detenido', [None], [None]], ]}
dict_elem_new = {
    'Beginning': [['Configuracion Inicial de PC', [None], [None]],
                  ['Conseguir Software(Update) y Parametros(XML)', [None], [None]],
                  ['Crear Carpeta del Job y Crear Archivos de Documentacion:\nStarter REC, Board Information', [None], [None]],
                  ['Escanear Codigos de Barras de Tarjetas y Dispositivos', [None], [None]],
                  ['Crear Documentacion de Visual Inspection List, Tech Report y Passcode', [None], [None]],
                  ['Inspeccionar Jumpers y Switches', [None], [None]],
                  ['Checar Voltajes', [None], [None]], ],
    'Program': [['Flashear HAPS', ['SHC'], [1]],  # If HAPS
                ['Cargar el Software(Update)', [None], [None]],
                ['Conectar Arneces', [None], [None]],
                ['Cargar Software en el LS-EDGE del Cliente', [None], [None]],
                ['Verificar Tolerancias de AC por Medio de LabView', [None], [None]],
                ['Cargar los Parametros(XML)', [None], [None]],
                ['Agregar y Modificar Datos de Test', [None], [None]],
                ['Prueba Automatizada de LabView', [None], [None]], ],
    'Ending': [['Respaldar Electronicamente el Reporte de Prueba Automatizada', [None], [None]],
               ['Devolver Parametros Originales de Cliente', [None], [None]],
               ['Extraer los Parametros(CCF)', [None], [None]],
               ['Introducir el Passcode', [None], [None]],
               ['Poner el Controlador en Construction Mode', [None], [None]],
               ['Imprimir Papeleria Final', [None], [None]],
               ['Hacer Respaldo Electronico de Documentos al Servidor', [None], [None]],
               ['Carro a Estacion Final', [None], [None]], ],
    'Logic': [['', [None], [None]], ],
    'Complete': [['Fin de pruebas', [None], [None]], ],
    'Stopped': [['Detenido', [None], [None]], ]}
times_m2000 = {'Beginning':60,
                         'Program':40,
                         'Logic':110,
                         'Ending':45}
times_m4000 = {'Beginning':240,
                         'Program':205,
                         'Logic':370,
                         'Ending':30}
times_elem = {'Beginning':40,
                         'Program':120,
                         'Ending':60}
stop_reasons = [('Job reassignment', 'Job reassignment'),
                ('Shift ended','Shift ended'),
                ('Error Funcional', 'Error Funcional'),
                ('Tarjetas T', 'Tarjetas T'),
                ('Material Faltante', 'Custom Software Faltante'),
                ('Junta de supervisor', 'Junta de supervisor'),
                ('Tecnico no asignado', 'Tecnico no asignado'),
                ('Personal', 'Personal'),
                ('Ingenieria', 'Ingenieria'),
                ('Falla en equipo de computo', 'Falla en equipo de computo'),
                ('Entrenamiento', 'Entrenamiento')]#TODO is this list still needed?
stations_dict = [('1', 'S1'),
                 ('2', 'S2'),
                 ('3', 'S3'),
                 ('4', 'S4'),
                 ('5', 'S5'),
                 ('6', 'S6'),
                 ('7', 'S7'),
                 ('8', 'S8'),
                 ('9', 'S9'),
                 ('10', 'S10'),
                 ('11', 'S11'),
                 ('12', 'S12'),
                 ('13', 'ELEM1'),
                 ('14', 'ELEM2')]
status_dict = [('Beginning', 'Beginning'),
               ('Program', 'Program'),
               ('Logic', 'Logic'),
               ('Ending', 'Ending'),
               ('Complete', 'Complete'),
               ('Stopped', 'Stopped')]
type_of_jobs = [('2000', 'M2000'),
                ('4000', 'M4000'),
                ('ELEM', 'Element')]
features_list = [('COP','Serial Car Operating Panel'),
                 ('SHC','Serial Hall Calls'),
                 ('HAPS','HAPS battery'),
                 ('OVL','Overlay'),
                 ('GROUP','Group'),
                 ('mView','mView'),
                 ('iMon','iMonitor'),
                 ('DCC',_('Door Control in Cartop')),
                 ('CPI',_('CPI Board Included'))]
features=(('COP','Serial Car Operating Panel'),
          ('SHC','Serial Hall Calls'),
          ('HAPS','HAPS Battery'),
          ('DCC',_('Door Control in Cartop')),
          ('CPI',_('CPI Board Included')),
          ('OVL','Overlay'),
          ('GROUP','Group'),
          ('mView','mView'),
          ('iMon','iMonitor'),
          ('PC','PC de cliente'),
          ('BCV','Brake Coil Voltage > 100'),
          ('MBRAKE','EMBRAKE Module'),
          ('EMCO','EMCO BOARD'),
          ('R6','R6 Regen Unit'),
          ('None',_('None')))
stations_tupple = (('1', 'S1'),
            ('2', 'S2'),
            ('3', 'S3'),
            ('4', 'S4'),
            ('5', 'S5'),
            ('6', 'S6'),
            ('7', 'S7'),
            ('8', 'S8'),
            ('9', 'S9'),
            ('10', 'S10'),
            ('11', 'S11'),
            ('12', 'S12'),
            ('13', 'ELEM1'),
            ('14', 'ELEM2'))
label_admin = [('-', '-'),
               ('A', 'A'),
               ('B', 'B'),
               ('C', 'C'),
               ('D', 'D'),
               ('E', 'E'),
               ('F', 'F'),
               ('G', 'G'),
               ('H', 'H')]
label = (('-', '-'),
         ('A', 'A'),
         ('B', 'B'),
         ('C', 'C'),
         ('D', 'D'),
         ('E', 'E'),
         ('F', 'F'),
         ('G', 'G'),
         ('H', 'H'))
job_type_tupple = (('2000', 'M2000'),
            ('4000', 'M4000'),
            ('ELEM', 'Element'))
stations_by_type = {'2000':{'0':'----',
                            '1': 'S1',
                             '2': 'S2',
                             '3': 'S3',
                             '4': 'S4',
                             '5': 'S5',
                             '6': 'S6'},
                    '4000':{'0':'----',
                            '7': 'S7',
                             '8': 'S8',
                             '9': 'S9',
                             '10': 'S10',
                             '11': 'S11',
                             '12': 'S12'},
                    'ELEM':{'0':'----',
                            '13': 'ELEM1',
                            '14': 'ELEM2'}}
status_dict_tupple = (('Beginning', 'Beginning'),
                      ('Program', 'Program'),
                      ('Logic', 'Logic'),
                      ('Ending', 'Ending'),
                      ('Complete', 'Complete'),
                      ('Stopped', 'Stopped'))
headers = ['Job #',
           'PO',
           'Job Type',
           'Status',
           'Station',
           'Shipping Date',
           'Beginning',
           'Program',
           'Logic',
           'Ending',
           'Elapsed Time on Job',
           '# of Stops',
           'Time on Stops',
           'Effective Time on Job']
stops_headers = ['Job #',
           'PO',
           'Job Type',
           'Reason',
           'Cause',
           'Add. Cause',
           'Description',
           'Solution',
           'Station',
           'Time on Stop']