import opendssdirect as dss
from pathlib import Path
from plotter import Plotter


def perform_case_base(dss_main_file, target_buses, transformer_buses_id):
    print('-------- SOLVING BASE CASE --------')
    dss.Text.Command('Redirect {}'.format(dss_main_file))

    # Monitor TR-11
    dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11 '
                     f'element=load.2450100 terminal=1 mode=0')

    # Monitor TR-07
    dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07 '
                     f'element=load.111450100 terminal=1 mode=0')

    # Monitor TR-05
    dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05 '
                     f'element=load.102450100 terminal=1 mode=0')

    dss.Solution.Solve()

    print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
    print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kW')
    print(f'Overload Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
    print(f'Overload Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

    for index, bus in enumerate(target_buses):
        plotter = Plotter()
        dss.Text.Command(f'Export monitors {bus}')
        plotter.set_file(str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_1.csv').resolve()))
        plotter.set_axis(x='hour', y1='V1')
        plotter.set_labels(l1='V1')
        plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
        plotter.perform_plot()
        plotter.show_max_min('V1', 'hour')
        plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
        plotter.save_figure(f'{bus}_base_case_voltage')
        # plotter.show_figure()
        plotter.close_figure()

        plotter = Plotter()
        plotter.set_file(str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_1.csv').resolve()))
        plotter.set_axis(x='hour', y1='I1')
        plotter.set_labels(l1='I1')
        plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
        plotter.perform_plot()
        plotter.show_max_min('I1', 'hour')
        plotter.configure_output(show_legend=False, show_grid=True)
        plotter.save_figure(f'{bus}_base_case_current')
        # plotter.show_figure()
        plotter.close_figure()


def perform_case_with_pv(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id):
    print('-------- SOLVING CASE WITH PV --------')

    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with PV inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))
        dss.Text.Command(f'new PVsystem.pv phases=1 Bus1={gd_saeb_bus} conn=wye kV = 0.24 pf=0.92 kVA=50 '
                         'daily=pv_shape')
        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_PV_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_PV_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_PV_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_PV_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_PV_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_pv_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_PV_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='I1')
            plotter.set_labels(l1='I1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            plotter.perform_plot()
            plotter.show_max_min('I1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_pv_current')
            # plotter.show_figure()
            plotter.close_figure()


def perform_case_with_pv_and_voltwatt(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id,
                                      transformer_buses_id):
    print('------- SOLVING CASE WITH PV and VOLTWATT -------')

    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with PV and VOLTWATT inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))
        dss.Text.Command(f'new PVsystem.pv phases=1 Bus1={gd_saeb_bus} conn=wye kV = 0.24 pf=0.92 kVA=50 '
                         'daily=pv_shape')

        dss.Text.Command(
            'new InvControl.InvPVCtrl Mode=VOLTWATT voltwatt_curve=VoltWatt_curve voltage_curvex_ref=rated '
            'VoltwattYaxis=PMPPU VarChangeTolerance=0.0002 VoltageChangeTolerance=0.1 deltaP_factor=-1 '
            'EventLog=yes')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_PV_VOLTWATT_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_PV_VOLTWATT_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_PV_VOLTWATT_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_PV_VOLTWATT_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_PV_VOLTWATT_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_pv_voltwatt_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_PV_VOLTWATT_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='I1')
            plotter.set_labels(l1='I1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            plotter.perform_plot()
            plotter.show_max_min('I1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_pv_voltwatt_current')
            # plotter.show_figure()
            plotter.close_figure()


def perform_case_with_pv_and_voltvar(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id,
                                     transformer_buses_id):
    print('-------- SOLVING CASE WITH PV and VOLTVAR --------')

    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with PV and VOLTVAR inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))
        dss.Text.Command(f'new PVsystem.pv phases=1 Bus1={gd_saeb_bus} conn=wye kV=0.24 pf=0.92 kVA=50 '
                         'daily=pv_shape')

        dss.Text.Command('new Invcontrol.Inv1 Mode=VOLTVAR voltage_curvex_ref=rated'
                         ' vvc_curve1=vv_curve DeltaQ_factor=-1  voltagechangetolerance=0.1'
                         ' varchangetolerance=0.4 EventLog=yes')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_PV_VOLTVAR_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_PV_VOLTVAR_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_PV_VOLTVAR_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_PV_VOLTVAR_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_PV_VOLTVAR_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_pv_voltvar_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_PV_VOLTVAR_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_pv_voltvar_current')
            # # plotter.show_figure()
            # plotter.close_figure()


def perform_with_saeb(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id,
                      transformer_buses_id):
    print('-------- SOLVING CASE WITH SAEB --------')
    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with SAEB inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))

        dss.Text.Command(f'new storage.ES1 phases=1 bus1={gd_saeb_bus} kV=0.24 pf=0.95 kVA=20 '
                         f'kwhrated=60 state=IDLING %stored=75 DischargeTrigger=0')

        # dss.Text.Command(f'new StorageController.SC element=Transformer.05410_G2000XE9500 terminal=1 modedis=support '
        #                  f'kwtarget=40 modecharge=Time timeChargeTrigger=20 %rateCharge=50 %reserve=10  '
        #                  f'elementList=[ES1] eventlog=yes')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_SAEB_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_SAEB_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_SAEB_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_SAEB_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_current')
            # # plotter.show_figure()
            # plotter.close_figure()


def perform_with_saeb_voltwatt(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id,
                               transformer_buses_id):
    print('-------- SOLVING CASE WITH SAEB AND VOLTWATT --------')
    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with SAEB and voltwatt inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))

        dss.Text.Command(f'new storage.ES1 phases=1 bus1={gd_saeb_bus} kV=0.24 pf=0.95 kVA=20 '
                         f'kwhrated=60 state=IDLING %stored=75 DischargeTrigger=0')

        dss.Text.Command(
            'new InvControl.InvPVCtrl Mode=VOLTWATT voltwatt_curve=VoltWatt_curve voltage_curvex_ref=rated '
            'VoltwattYaxis=PMPPU VarChangeTolerance=0.0002 VoltageChangeTolerance=0.1 deltaP_factor=-1 '
            'EventLog=yes')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_SAEB_VOLTWATT_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_SAEB_VOLTWATT_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_SAEB_VOLTWATT_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_SAEB_VOLTWATT_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_VOLTWATT_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_voltwatt_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_VOLTWATT_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_voltwatt_current')
            # # plotter.show_figure()
            # plotter.close_figure()


def perform_with_saeb_voltvar(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id,
                              transformer_buses_id):
    print('-------- SOLVING CASE WITH SAEB AND VOLTVAR --------')
    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with SAEB and VOLTVAR inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))

        dss.Text.Command(f'new storage.ES1 phases=1 bus1={gd_saeb_bus} kV=0.24 pf=0.95 kVA=20 '
                         f'kwhrated=60 state=IDLING %stored=75 DischargeTrigger=0')

        dss.Text.Command('new Invcontrol.Inv1 Mode=VOLTVAR voltage_curvex_ref=rated'
                         ' vvc_curve1=vv_curve DeltaQ_factor=-1  voltagechangetolerance=0.1'
                         ' varchangetolerance=0.4 EventLog=yes')

        # dss.Text.Command(f'new StorageController.SC element=Transformer.05410_G2000XE9500 terminal=1 modedis=support '
        #                  f'kwtarget=40 modecharge=Time timeChargeTrigger=20 %rateCharge=50 %reserve=10  '
        #                  f'elementList=[ES1] eventlog=yes')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_SAEB_VOLTVAR_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_SAEB_VOLTVAR_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_SAEB_VOLTVAR_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_SAEB_VOLTVAR_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_VOLTVAR_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_voltvar_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_VOLTVAR_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_voltvar_current')
            # # plotter.show_figure()
            # plotter.close_figure()


def perform_with_saeb_pv(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id):
    print('-------- SOLVING CASE WITH SAEB AND PV --------')
    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with SAEB and PV inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))

        dss.Text.Command(f'new storage.ES1 phases=1 bus1={gd_saeb_bus} kV=0.24 pf=0.95 kVA=20 '
                         f'kwhrated=60 state=IDLING %stored=75 DischargeTrigger=0')

        dss.Text.Command(f'new PVsystem.pv phases=1 Bus1={gd_saeb_bus} conn=wye kV = 0.24 pf=0.92 kVA=50 '
                         'daily=pv_shape')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_SAEB_PV_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_SAEB_PV_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_SAEB_PV_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_SAEB_PV_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_PV_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_pv_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_PV_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_pv_current')
            # # plotter.show_figure()
            # plotter.close_figure()


def perform_with_saeb_pv_voltwatt(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id):
    print('-------- SOLVING CASE WITH SAEB, PV e VOLTWATT --------')
    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with SAEB, PV and VOLTWATT inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))

        dss.Text.Command(f'new storage.ES1 phases=1 bus1={gd_saeb_bus} kV=0.24 pf=0.95 kVA=20 '
                         f'kwhrated=60 state=IDLING %stored=75 DischargeTrigger=0')

        dss.Text.Command(f'new PVsystem.pv phases=1 Bus1={gd_saeb_bus} conn=wye kV = 0.24 pf=0.92 kVA=50 '
                         'daily=pv_shape')

        dss.Text.Command(
            'new InvControl.InvPVCtrl Mode=VOLTWATT voltwatt_curve=VoltWatt_curve voltage_curvex_ref=rated '
            'VoltwattYaxis=PMPPU VarChangeTolerance=0.0002 VoltageChangeTolerance=0.1 deltaP_factor=-1 '
            'EventLog=yes')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_SAEB_PV_VOLTWATT_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_SAEB_PV_VOLTWATT_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_SAEB_PV_VOLTWATT_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_SAEB_PV_VOLTWATT_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(
                    f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_PV_VOLTWATT_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_pv_voltwatt_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(
            #         f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_PV_VOLTWATT_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_pv_voltwatt_current')
            # # plotter.show_figure()
            # plotter.close_figure()


def perform_with_saeb_pv_voltvar(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id):
    print('-------- SOLVING CASE WITH SAEB, PV e VOLTVAR --------')
    for index, gd_saeb_bus in enumerate(gd_saeb_buses):
        print(f'Solving with SAEB, PV and VOLTVAR inserted on load {gd_saeb_buses_id[index]}...')

        dss.Text.Command('Redirect {}'.format(dss_main_file))

        dss.Text.Command(f'new storage.ES1 phases=1 bus1={gd_saeb_bus} kV=0.24 pf=0.95 kVA=20 '
                         f'kwhrated=60 state=IDLING %stored=75 DischargeTrigger=0')

        dss.Text.Command(f'new PVsystem.pv phases=1 Bus1={gd_saeb_bus} conn=wye kV = 0.24 pf=0.92 kVA=50 '
                         'daily=pv_shape')

        # Monitor TR-11
        dss.Text.Command(f'new Monitor.G2000XE9500_N283544_sec_1_TR11_SAEB_PV_VOLTVAR_{gd_saeb_buses_id[index]}'
                         f' element=load.2450100 terminal=1 mode=0')

        # Monitor TR-07
        dss.Text.Command(f'new Monitor.G2100AH6800_N283651_sec_1_TR07_SAEB_PV_VOLTVAR_{gd_saeb_buses_id[index]} '
                         f'element=load.111450100 terminal=1 mode=0')

        # Monitor TR-05
        dss.Text.Command(f'new Monitor.G2100CH1800_N1385522_sec_1_TR05_SAEB_PV_VOLTVAR_{gd_saeb_buses_id[index]} '
                         f'element=load.102450100 terminal=1 mode=0')

        dss.Solution.Solve()

        print(f'Losses: {round(dss.Meters.RegisterValues()[12], 3)} kWh')
        print(f'Max kW: {round(dss.Meters.RegisterValues()[2], 3)} kWh')
        print(f'Overload kWh Normal: {round(dss.Meters.RegisterValues()[8], 3)} kWh')
        print(f'Overload kWh Emerg: {round(dss.Meters.RegisterValues()[9], 3)} kWh')

        for bus in target_buses:
            dss.Text.Command(f'Export monitors {bus}_SAEB_PV_VOLTVAR_{gd_saeb_buses_id[index]}')
            plotter = Plotter()
            plotter.set_file(
                str(Path(
                    f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_PV_VOLTVAR_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            plotter.set_axis(x='hour', y1='V1')
            plotter.set_labels(l1='V1')
            plotter.set_axis_name(x_name='Time (h)', y_name='Voltage (V)')
            plotter.perform_plot()
            plotter.show_max_min('V1', 'hour')
            plotter.configure_output(show_legend=False, show_grid=True, limit_up_y=252, limit_down_y=228)
            plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_pv_voltvar_voltage')
            # plotter.show_figure()
            plotter.close_figure()

            # plotter = Plotter()
            # plotter.set_file(
            #     str(Path(
            #         f'{dss_main_folder}/ckt24_Mon_{bus}_SAEB_PV_VOLTVAR_{gd_saeb_buses_id[index]}_1.csv').resolve()))
            # plotter.set_axis(x='hour', y1='I1')
            # plotter.set_labels(l1='I1')
            # plotter.set_axis_name(x_name='Time (h)', y_name='Current (I)')
            # plotter.perform_plot()
            # plotter.show_max_min('I1', 'hour')
            # plotter.configure_output(show_legend=False, show_grid=True)
            # plotter.save_figure(f'{bus}_{gd_saeb_buses_id[index]}_case_with_saeb_pv_voltvar_current')
            # # plotter.show_figure()
            # plotter.close_figure()


if __name__ == '__main__':
    print(f'OpenDSSDirect.py version: {dss.__version__}')
    print(f'Engine information: {dss.Basic.Version()}')

    target_buses = ['g2000xe9500_n283544_sec_1_TR11',
                    'g2100ah6800_n283651_sec_1_TR07',
                    'g2100ch1800_n1385522_sec_1_TR05']

    transformer_buses_id = ['TR-11', 'TR-07', 'TR-05']

    # 5 - bus1=G2100CH1800_N1385522_sec_5.3
    # 21 - bus1=G2100AH6800_N283651_sec_4.3
    # 43 - bus1=G2000XE9500_N283544_sec_8.3
    gd_saeb_buses = ['G2000XE9500_N283544_sec_8.3', 'G2100AH6800_N283651_sec_4.3', 'G2100CH1800_N1385522_sec_5.3']
    # saeb_lines = ['05410_108671UG', '05410_108669UG', '05410_108682UG']
    gd_saeb_buses_id = ['43', '21', '5']

    pv_bus = 'G2000XE9500_N283544_sec_1.3'

    dss_main_file = str(Path('dss/Run_Ckt24.dss').resolve())
    dss_main_folder = str(Path('dss').resolve())
    dss.Basic.DataPath(dss_main_folder)

    # perform_case_base(dss_main_file, target_buses, transformer_buses_id)

    # PART 1
    # perform_case_with_pv(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)
    # perform_case_with_pv_and_voltwatt(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id,
    #                                   transformer_buses_id)
    # perform_case_with_pv_and_voltvar(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)

    # PART 2
    # perform_with_saeb(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)
    # perform_with_saeb_voltwatt(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)
    # perform_with_saeb_voltvar(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)

    # PART 3
    # perform_with_saeb_pv(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)
    # perform_with_saeb_pv_voltwatt(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)
    perform_with_saeb_pv_voltvar(dss_main_file, target_buses, gd_saeb_buses, gd_saeb_buses_id, transformer_buses_id)
