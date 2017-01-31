dict_m4000 = {'Beginning':['Documentacion Inicial',
                                      'Inspeccion Visual',
                                      'Preparacion de Labview',
                                      'Chequeo preliminar de voltajes iniciales'],
                         'Program':['Programacion de Flasheo',
                                    'Conexion de arneces simulador del carro y arneceses cartop',#if cartop
                                    'Programacion del Firmware',
                                    'Conexion de arneces del simulador',#if cartop
                                    'Programacion de parametros F1',
                                    'Programacion tarjeta CE Electronics',
                                    'Programacion de Parametros F7\n Version Test',
                                    'Programacion de Parametros F5\n Version Test',
                                    'MBRAKE Module\nCalibracion Inicial',
                                    'F5 Floor Learning',
                                    'F7 Terminal Limits'],
                         'Logic':['Board power test SAFL & SAFS',
                                  'Drive Interface',
                                  'Emergency Brake',
                                  'Safety and inspection',
                                  'Door locks and hoistway access',
                                  'Landing System',
                                  'Door Interface (Pag CT1, CT2)',#if DCC
                                  'COP parte 1 (Pag CPI)',#if DCC
                                  'Door Interface (Pag 11, 11X)',#if !DCC
                                  'COP parte 1 (Pag 12)',#if !DCC
                                  'Fire Service Phase I (Pag 13)',
                                  'Fire Service Phase II (Pag 12)',#if !CPI
                                  'Movement Indication (Pag 14)',#if !CPI
                                  'Fire Service Phase II (Pag CPI)',#if CPI
                                  'Movement Indication (Pag CPI)',#if CPI
                                  'Car Calls (Pag CPI)',#if CPI
                                  'Calls (Pag 16)',
                                  'Serial Hall Calls (Pag SH)'#if serial hall calls
                                  'Programmable Input/Outputs',
                                  'Additional Manual Test\n(Overspeeds and Limits)',
                                  'MBRAKE\nCalibracion Final',
                                  'Programacion de Parametros F7\n Version Cliente',
                                  'Programacion de Parametros F5\n Version Cliente',],
                         'Ending':['Inspeccion Final',
                                   'Passcode',
                                   'Papeleria Final',
                                   'Respaldo Electronico de la papeleria',
                                   'Desconnecion de Arneces',
                                   'Carro a estacion final'],
                         'Complete':['Fin de pruebas'],
                         'Stopped': ['Detenido']}

if True:
    dict_m4000['Program'].pop(0)
    dict_m4000['Program'].pop(0)
for i in dict_m4000['Program']:
    print(i)