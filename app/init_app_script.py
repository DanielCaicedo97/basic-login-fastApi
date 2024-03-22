import subprocess

def run_server():
    command = ["uvicorn", "main:app", "--reload", "--port", "3000", "--host", "0.0.0.0"]
    subprocess.run(command)

if __name__ == "__main__":
    run_server()