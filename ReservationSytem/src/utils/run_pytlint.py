import os
import subprocess
import time

# Definir el folder de resultados de pylint
pylint_reports_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'pylint_reports')
os.makedirs(pylint_reports_folder, exist_ok=True)

# Obtener la hora actual para el sufijo del archivo
current_time = time.strftime("%H%M%S")

# Nombre del archivo de resultados
pylint_report_file = os.path.join(pylint_reports_folder, f'pylint_report_{current_time}.txt')

# Ruta absoluta del archivo a verificar
file_to_check = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reservation_system.py'))

# Ejecutar pylint y guardar los resultados en el archivo
with open(pylint_report_file, 'w') as report_file:
    subprocess.run(['pylint', file_to_check], stdout=report_file, stderr=report_file)

print(f'Pylint report saved to {pylint_report_file}')