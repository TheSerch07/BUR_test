import numpy as np

class WellTrajectoryCalculator:
    def __init__(self, target_direction=106.49):
        self.target_direction = target_direction

    @staticmethod
    def convert_deg_rad(degrees):
        return np.radians(degrees)

    def calculate_trajectory(self, directions, places=2):
        for i in range(1, len(directions)):
            prev_dir = directions[i-1]
            current_dir = directions[i]

            incl_x = current_dir.incl
            incl_x_1 = prev_dir.incl
            azm_x = current_dir.azm
            azm_x_1 = prev_dir.azm
            depth_delta = current_dir.measured_depth - prev_dir.measured_depth

            # Calculo de TVD
            tvd_delta = (np.cos(self.convert_deg_rad(incl_x_1)) + np.cos(self.convert_deg_rad(incl_x))) * (depth_delta / 2)
            tvd = round(prev_dir.tvd + tvd_delta, places)

            # Calculo de NS
            ns_delta = ((np.sin(self.convert_deg_rad(incl_x_1)) * np.cos(self.convert_deg_rad(azm_x_1))) + 
                        (np.sin(self.convert_deg_rad(incl_x)) * np.cos(self.convert_deg_rad(azm_x)))) * (depth_delta / 2)
            ns = round(prev_dir.ns + ns_delta, places)

            # Calculo de EW
            ew_delta = ((np.sin(self.convert_deg_rad(incl_x_1)) * np.sin(self.convert_deg_rad(azm_x_1))) + 
                        (np.sin(self.convert_deg_rad(incl_x)) * np.sin(self.convert_deg_rad(azm_x)))) * (depth_delta / 2)
            ew = round(prev_dir.ew + ew_delta, places)

            # Calculo de Closure
            closure_delta = np.sqrt((prev_dir.ns - ns)**2 + (prev_dir.ew - ew)**2)
            closure = round(closure_delta, places)

            # Calculo de Closure Direction
            closure_dir = self.calculate_closure_direction(ns, ew)

            # Calculo de VS
            vs_delta = closure * np.cos(np.radians(closure_dir) - np.radians(self.target_direction))
            vs = round(prev_dir.vs + vs_delta, places)

            # Calculo de DLS
            dl = np.arccos(np.cos(self.convert_deg_rad(incl_x - incl_x_1)) - 
                           (np.sin(self.convert_deg_rad(incl_x_1)) * np.sin(self.convert_deg_rad(incl_x)) * 
                            (1 - np.cos(self.convert_deg_rad(azm_x - azm_x_1)))))
            dl_deg = np.degrees(dl)
            dls = round((dl_deg / depth_delta) * 100, places)

            # Calculo de BUR
            bur = ((incl_x - incl_x_1) / depth_delta) * 100
            bur_deg_100ft = round(bur, places)

            # Actualizar la dirección actual con los valores calculados
            current_dir.update_values(tvd, ns, ew, closure, closure_dir, vs, dls, bur_deg_100ft)

    @staticmethod
    def calculate_closure_direction(ns, ew):
        if ns > 0 and ew >= 0:
            closure_dir = np.degrees(np.arctan(ew / ns))
        elif ns < 0 and ew >= 0:
            closure_dir = np.degrees(np.arctan(ew / ns)) + 180
        elif ns < 0 and ew < 0:
            closure_dir = np.degrees(np.arctan(ew / ns)) + 180
        elif ns > 0 and ew < 0:
            closure_dir = np.degrees(np.arctan(ew / ns)) + 360
        else:
            closure_dir = np.degrees(np.pi / 2)  # Asignar 90 grados si EW es >= 0 o -90 si es negativo
        return closure_dir
