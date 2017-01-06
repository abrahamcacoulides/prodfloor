dict_of_steps = {'Beginning':['Documentacion Inicial',
                                      'Inspeccion Visual',
                                      'Preparacion de Labview',
                                      'Chequeo preliminar de voltajes iniciales'],
                         'Program':['Programacion de Flasheo',
                                    'Programacion del Firmware',
                                    'Programacion del Solid State Starter',
                                    'Programacion de paramtros F1',
                                    'Programacion tarjeta CE Electronics'],
                         'Logic':['Board power test SAFL & SAFS',
                                  'Motor Starter Test',
                                  'Valve control and limits',
                                  'Safety and inspection',
                                  'Door locks and hoistway access',
                                  'Landing system',
                                  'Door Interface',
                                  'COP parte 1',
                                  'Fire Service Phase I',
                                  'Fire Service Phase II',
                                  'Movement Indication',
                                  'Calls',
                                  'Programmable Input/Outputs'],
                         'Ending':['Inspeccion Final',
                                   'Passcode',
                                   'Papeleria Final',
                                   'Respaldo Electronico de la papeleria',
                                   'Desconnecion de Arneces',
                                   'Carro a estacion final'],
                         'Complete':['Fin de pruebas']}
status='Program'
print(dict_of_steps[status])
dict_of_stages = {1:'Beginning',
                         2:'Program',
                         3:'Logic',
                         4:'Ending',
                         5:'Complete'}
for number, stage in dict_of_stages.items():
    if stage == status:
        print (dict_of_stages[number+1])