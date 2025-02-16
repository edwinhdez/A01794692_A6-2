import subprocess
import datetime
import os

def run_pylint():
    # Obtener la fecha y hora actuales
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    # Nombre del archivo de resultados
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pylint_reports'))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"pylint_report_{timestamp}.txt")

    # Ruta al archivo computeStatistics.py
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    script_path = os.path.join(script_dir, 'compute_statistics.py')

    # Ejecutar pylint y guardar los resultados en el archivo
    with open(output_file, "w") as f:
        subprocess.run(["pylint", script_path], stdout=f, stderr=subprocess.STDOUT)

    print(f"Pylint report saved to {output_file}")

if __name__ == "__main__":
    run_pylint()