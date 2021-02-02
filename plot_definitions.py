plot_definitions = [
    {'page': 'Page 1',
     'parameter_paths':[
         {'file':'vehicle_status_0','parameter':'nav_state'},
         {'file':'vehicle_status_0','parameter':'arming_state'},
         {'file':'vehicle_status_0','parameter':'failsafe'},
         {'file':'vehicle_attitude_0','parameter':'q[1]', 'rename':'Roll'},
         {'file':'vehicle_attitude_0','parameter':'q[2]', 'rename':'Pitch'},
         {'file':'vehicle_attitude_0','parameter':'q[3]', 'rename':'Yaw'},
         {'file':'battery_status_0','parameter': 'voltage_filtered_v', 'rename':'Voltage (V)'},
         {'file':'battery_status_0','parameter': 'current_filtered_a', 'rename':'Current (A)'},
         {'file':'battery_status_0','parameter': 'discharged_mah', 'rename':'Discharged mAh'},
         {'file':'vehicle_local_position_0','parameter': 'z', 'rename':'Altitude (m)'},
         {'file':'vehicle_land_detected_0','parameter': 'landed', 'rename':'Landed'},
         {'file':'vehicle_land_detected_0','parameter': 'in_ground_effect', 'rename':'In Ground Effect'},
         {'file':'vehicle_local_position_0','parameter': 'vy', 'rename':'Y Speed'},
         {'file':'trajectory_setpoint_0','parameter': 'vy', 'rename':'Desired Y Speed'},
         {'file':'vehicle_local_position_0','parameter': 'vz', 'rename':'Z Speed'},
         {'file':'trajectory_setpoint_0','parameter': 'vz', 'rename':'Desired Z Speed'},
         ],
     'params_to_plot':[
         {'parameter': 'Offboard', 'type': 'boolean', 'axis': 1},
         {'parameter': 'Armed', 'type': 'boolean', 'axis': 2},
         {'parameter': 'Landed', 'type': 'boolean', 'axis': 3},
         {'parameter': 'In Ground Effect', 'type': 'boolean', 'axis': 4},
         {'parameter': 'Voltage (V)', 'type': 'analogue', 'axis': 5},
         {'parameter': 'Current (A)', 'type': 'analogue', 'axis': 6},   
         {'parameter': 'Discharged mAh', 'type': 'analogue', 'axis': 7},  
         {'parameter': 'Altitude (m)', 'type': 'analogue', 'axis': 8},
         {'parameter': 'Roll', 'type': 'analogue', 'axis': 9},
         {'parameter': 'Pitch', 'type': 'analogue', 'axis': 10},
         {'parameter': 'Yaw', 'type': 'analogue', 'axis': 11},
         {'parameter': 'Y Speed', 'type': 'analogue', 'axis': 12},
         {'parameter': 'Desired Y Speed', 'type': 'analogue', 'axis': 12},
         {'parameter': 'Z Speed', 'type': 'analogue', 'axis': 13},
         {'parameter': 'Desired Z Speed', 'type': 'analogue', 'axis': 13}
         ]
     },
    {'page': 'Setpoints',
     'parameter_paths':[
         {'file':'vehicle_local_position_0','parameter': 'vx', 'rename':'X Speed'},
         {'file':'trajectory_setpoint_0','parameter': 'vx', 'rename':'Desired X Speed'},
         {'file':'vehicle_local_position_0','parameter': 'vy', 'rename':'Y Speed'},
         {'file':'trajectory_setpoint_0','parameter': 'vy', 'rename':'Desired Y Speed'},
         {'file':'vehicle_local_position_0','parameter': 'vz', 'rename':'Z Speed'},
         {'file':'trajectory_setpoint_0','parameter': 'vz', 'rename':'Desired Z Speed'},
         ],
     'params_to_plot':[
         {'parameter': 'X Speed', 'type': 'analogue', 'axis': 1},
         {'parameter': 'Desired X Speed', 'type': 'analogue', 'axis': 1},
         {'parameter': 'Y Speed', 'type': 'analogue', 'axis': 2},
         {'parameter': 'Desired Y Speed', 'type': 'analogue', 'axis': 2},
         {'parameter': 'Z Speed', 'type': 'analogue', 'axis': 3},
         {'parameter': 'Desired Z Speed', 'type': 'analogue', 'axis': 3}
         ]
     },
    {'page': 'Flight Path',
     'parameter_paths':[
         {'file':'vehicle_local_position_0','parameter': 'x', 'rename':'Local X'},
         {'file':'vehicle_local_position_0','parameter': 'y', 'rename':'Local Y'},
         {'file':'vehicle_local_position_0','parameter': 'z', 'rename':'Local Z'},
         ],
     'params_to_plot':[
         {'parameter': 'X', 'type': 'analogue', 'axis': 1},
         {'parameter': 'Y', 'type': 'analogue', 'axis': 1},
         {'parameter': 'Z', 'type': 'analogue', 'axis': 1},
         ]
     }
]