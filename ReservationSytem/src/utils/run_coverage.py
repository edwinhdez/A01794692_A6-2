import time
import subprocess
import os

# Definir el folder de resultados de cobertura
coverage_reports_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'coverage_reports')
os.makedirs(coverage_reports_folder, exist_ok=True)

# Obtener la hora actual para el sufijo del archivo
current_time = time.strftime("%H%M%S")

# Nombre del archivo de resultados
coverage_report_file = os.path.join(coverage_reports_folder, f'coverage_report_{current_time}.txt')

# Ruta absoluta del directorio de tests
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'tests'))

# Ejecutar coverage y guardar los resultados en el archivo
subprocess.run(['coverage', 'run', '-m', 'unittest', 'discover', '-s', tests_dir])
with open(coverage_report_file, 'w') as report_file:
    subprocess.run(['coverage', 'report', '-m'], stdout=report_file)

print(f'Coverage report saved to {coverage_report_file}')
