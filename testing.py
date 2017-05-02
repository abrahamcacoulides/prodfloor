def remaining_steps(remaining_steps,starting_index, dict, status, features_in_job):
    c=0 #number of matching steps
    index = starting_index #index provided by user in which the index in which to start is provided
    steps = dict[status] #list of steps, is determined in function of the status which is provided by the cust
    while index<len(steps):#loop to be performed if
        current = steps[index]
        features_to_compare = current[1]
        if None in features_to_compare:
            c += 1
            if index < len(steps):
                index += 1
            else:
                if c == remaining_steps:
                    return True
                else:
                    return False
        else:#this else is for the steps with features
            count = 0
            meet_the_criteria = False
            while count < len(features_to_compare):
                current = steps[index]
                features_to_compare = current[1]
                values = current[2]
                feature_to_compare = features_to_compare[count]
                value = values[count]
                if any(i == feature_to_compare for i in features_in_job):  # the feature to compare is IN the job features
                    if value == 1:  # the feature to compare is wanted in the step and is in it
                        count += 1
                        if count == len(features_to_compare):
                            meet_the_criteria = True
                    else:  # the feature to compare is NOT wanted in the step but it is there
                        # should restart the function but skipping the current step
                        break
                else:  # the feature to compare is NOT in the job features
                    if value == 0:  # the feature to compare is NOT wanted in the step and is NOT in it
                        count += 1
                        if count == len(features_to_compare):
                            meet_the_criteria = True
                    else:  # the feature to compare is wanted in the step but it is NOT there
                        # should restart the function but skipping the current step
                        break
            if meet_the_criteria:
                c += 1
            else:
                pass
            if index < len(steps):
                index += 1
            else:
                if c == remaining_steps:
                    return True
                else:
                    return False
    if c == remaining_steps:
        return True
    else:
        return False

print(remaining_steps(1,6,{
    'Beginning': [['Documentacion Inicial', [None,], [None,]],
                  ['Inspeccion Visual', [None,], [None,]],
                  ['Preparacion de Labview', [None,], [None,]],
                  ['Chequeo preliminar de voltajes iniciales', [None,], [None,]]],
    'Program': [['Programacion de Flasheo', [None,], [None,]],#0
                ['Conexion de arneces simulador del carro y arneces cartop', ['COP'], [1]],#1
                ['Programacion del Firmware(Chip)', [None,], [None,]],#2
                ['Conexion de arneces del simulador', ['COP'], [0]],#3
                ['Programacion del Solid State Starter', [None,], [None,]],#4
                ['Programacion de parametros F1', [None,], [None,]],#5
                ['Programacion tarjeta CE Electronics', ['COP',], [0,]]],#6
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
    'Stopped': ['Detenido']},'Program',['SHC','COP']))