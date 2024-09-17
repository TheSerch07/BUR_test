import os
import pandas as pd

class WellDirectionRepository:
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)

    def save_directions_to_csv(self, directions, original_filename):
        # Crear un DataFrame a partir de las direcciones
        data = {
            'incl': [direction.incl for direction in directions],
            'azm': [direction.azm for direction in directions],
            'measured_depth': [direction.measured_depth for direction in directions],
            'tvd': [direction.tvd for direction in directions],
            'ns': [direction.ns for direction in directions],
            'ew': [direction.ew for direction in directions],
            'closure': [direction.closure for direction in directions],
            'closure_direction': [direction.closure_direction for direction in directions],
            'vs': [direction.vs for direction in directions],
            'dls': [direction.dls for direction in directions],
            'BUR (Deg/100ft)': [direction.bur_deg_100ft for direction in directions]
        }

        df = pd.DataFrame(data)

        # Guardar el DataFrame como un archivo CSV
        result_path = os.path.join(self.upload_folder, f'result_{original_filename}')
        df.to_csv(result_path, index=False)

        return result_path
