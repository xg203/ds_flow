from metaflow import FlowSpec, step
import glob
import os
import subprocess
import sys

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
        
        cmd = [
            sys.executable, "scripts/combine.py",
            "--inputs"
        ] + input_paths + [
            "--output", self.final_output
        ]
        
        subprocess.check_call(cmd)
        self.next(self.end)

    @step
    def end(self):
        print("Flow finished successfully!")
        print(f"Result available at: data/final_combined.csv")

if __name__ == '__main__':
    StudentDataFlow()
