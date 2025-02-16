import subprocess
import datetime
import os

def run_flake8():
    try:
        # Generar el nombre del archivo con el sufijo de fecha y hora
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, '..', 'flake8_reports')
        output_file = os.path.join(output_dir, f"flake8_issues_{timestamp}.txt")
        
        # Crear el directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Ejecutar flake8 y capturar la salida
        result = subprocess.run(['poetry', 'run', 'flake8'], capture_output=True, text=True)
        
        # Guardar la salida en el archivo
        with open(output_file, 'w') as file:
            if result.returncode == 0:
                file.write("No issues found by flake8.\n")
                print("No issues found by flake8.")
            else:
                file.write("flake8 found issues:\n")
                file.write(result.stdout)
                file.write(result.stderr)
                print(f"flake8 found issues. See {output_file} for details.")
    except FileNotFoundError:
        print("flake8 or poetry is not installed or not found in the PATH.")
    except Exception as e:
        print(f"An error occurred while running flake8: {e}")

if __name__ == "__main__":
    run_flake8()