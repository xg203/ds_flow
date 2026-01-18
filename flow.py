from metaflow import FlowSpec, step
import glob
import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

class StudentDataFlow(FlowSpec):

    @step
    def start(self):
        self.files = glob.glob('data/student_*.csv')
        print(f"Found files: {self.files}")
        self.next(self.process_file, foreach='files')

    @step
    def process_file(self):
        self.input_file = self.input
        base_name = os.path.basename(self.input_file)
        self.output_file = f"data/processed_{base_name}"
        
        print(f"Processing {self.input_file} via CLI...")
        
        # Construct command to run the process script
        # Using sys.executable ensures we use the same environment
        cmd = [
            sys.executable, "scripts/process.py",
            "--input", self.input_file,
            "--output", self.output_file
        ]
        
        subprocess.check_call(cmd)
        
        self.next(self.join)

    @step
    def join(self, inputs):
        # Collect all output files from the parallel steps
        input_paths = [input.output_file for input in inputs]
        self.final_output = "data/final_combined.csv"
        
        print(f"Combining files via CLI: {input_paths}")
        
        # Call bash script via LSF: bsub -q short -K bash bash/combine.sh <output> <inputs...>
        cmd = [
            "bsub", "-q", "short", "-K",
            "bash", "bash/combine.sh",
            self.final_output
        ] + input_paths
        
        # Ensure PATH includes current dir for mock bsub
        env = os.environ.copy()
        env['PATH'] = f"{os.getcwd()}:{env['PATH']}"
        
        subprocess.check_call(cmd, env=env)
        subprocess.check_call(cmd, env=env)
        self.next(self.analyze)

    @step
    def analyze(self):
        print("Analyzing result using Docker...")
        
        # Absolute path for volume mounting
        data_dir = os.path.abspath("data")
        
        # Command: docker run -v /abs/path/data:/data ubuntu wc -l /data/final_combined.csv
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{data_dir}:/data",
            "ubuntu",
            "wc", "-l", "/data/final_combined.csv"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        print(f"Running: {' '.join(cmd)}")
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print(f"Docker command returned non-zero exit status: {e}")
        except FileNotFoundError:
            print("Docker executable not found. Please ensure Docker is installed and in your PATH.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        self.next(self.end)

    @step
    def end(self):
        print("Flow finished successfully!")
        print(f"Result available at: data/final_combined.csv")

if __name__ == '__main__':
    StudentDataFlow()
