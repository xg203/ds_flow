from metaflow import FlowSpec, step, current
import glob
import os
import subprocess
import sys
import yaml
import logging
from dotenv import load_dotenv

load_dotenv()

# Setup logging for the flow
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ds_flow')

class StudentDataFlow(FlowSpec):

    @step
    def start(self):
        # Load Configuration
        with open('config/settings.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        logger.info(f"Loaded config: {self.config}")
        
        # Use config for input pattern
        pattern = self.config['paths']['input_pattern']
        self.files = glob.glob(pattern)
        logger.info(f"Found input files: {self.files}")
        
        # Pass run_id for versioning
        self.run_id = current.run_id
        logger.info(f"Run ID: {self.run_id}")
        
        self.next(self.process_file, foreach='files')

    @step
    def process_file(self):
        self.input_file = self.input
        base_name = os.path.basename(self.input_file)
        # Versioned Output Filename: processed_<base>_<run_id>.csv
        filename_no_ext = os.path.splitext(base_name)[0]
        self.output_file = f"data/processed_{filename_no_ext}_{self.run_id}.csv"
        
        logger.info(f"Processing {self.input_file} via CLI...")
        
        cmd = [
            sys.executable, "scripts/process.py",
            "--input", self.input_file,
            "--output", self.output_file
        ]
        
        subprocess.check_call(cmd)
        
        self.next(self.join)

    @step
    def join(self, inputs):
        # Merge artifacts
        input_paths = [input.output_file for input in inputs]
        self.config = inputs[0].config # Propagate config
        self.run_id = inputs[0].run_id
        
        # Versioned Final Output
        self.final_output = f"data/final_combined_{self.run_id}.csv"
        
        logger.info(f"Combining files into {self.final_output}")
        
        queue = self.config['compute']['lsf_queue']
        
        # Call bash script via LSF using config value
        cmd = [
            "bsub", "-q", queue, "-K",
            "bash", "bash/combine.sh",
            self.final_output
        ] + input_paths
        
        # Ensure PATH includes current dir for mock bsub
        env = os.environ.copy()
        env['PATH'] = f"{os.getcwd()}:{env['PATH']}"
        
        subprocess.check_call(cmd, env=env)
        self.next(self.analyze)

    @step
    def analyze(self):
        logger.info("Analyzing result using Docker...")
        
        data_dir = os.path.abspath(self.config['paths']['data_dir'])
        docker_image = self.config['compute']['docker_image']
        
        # Path inside container
        container_path = f"/data/{os.path.basename(self.final_output)}"
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{data_dir}:/data",
            docker_image,
            "wc", "-l", container_path
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker command returned non-zero exit status: {e}")
        except FileNotFoundError:
            logger.error("Docker executable not found. Please ensure Docker is installed and in your PATH.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            
        self.next(self.end)

    @step
    def end(self):
        logger.info("Flow finished successfully!")
        logger.info(f"Result available at: {self.final_output}")

if __name__ == '__main__':
    StudentDataFlow()
