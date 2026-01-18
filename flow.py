from metaflow import FlowSpec, step, current
import glob
import os
import subprocess
import sys
import yaml
import logging
from dotenv import load_dotenv

load_dotenv()

# Setup logging
def setup_logging(log_dir, run_id):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"run_{run_id}.log")
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('ds_flow')

# Placeholder until config loaded
logger = logging.getLogger('ds_flow_init')

class StudentDataFlow(FlowSpec):

    @step
    def start(self):
        self.run_id = current.run_id
        
        # Load Configuration
        with open('config/settings.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Re-configure logging with correct path
        global logger
        logger = setup_logging(self.config['paths']['log_dir'], self.run_id)
        
        logger.info(f"Loaded config: {self.config}")
        logger.info(f"Run ID: {self.run_id}")
        
        # Read Sample Batches from Config
        self.sample_batches = self.config['compute'].get('sample_batches', [])
        logger.info(f"Sample Batches: {self.sample_batches}")
        
        # Ensure output directory exists
        os.makedirs(self.config['paths']['output_dir'], exist_ok=True)
        
        pattern = self.config['paths']['input_pattern']
        self.files = glob.glob(pattern)
        logger.info(f"Found input files: {self.files}")
        
        self.next(self.process_file, foreach='files')

    @step
    def process_file(self):
        self.input_file = self.input
        base_name = os.path.basename(self.input_file)
        filename_no_ext = os.path.splitext(base_name)[0]
        
        # Output to 'out/' directory
        out_dir = self.config['paths']['output_dir']
        self.output_file = os.path.join(out_dir, f"processed_{filename_no_ext}_{self.run_id}.csv")
        
        logger.info(f"Processing {self.input_file} -> {self.output_file}")
        
        cmd = [
            sys.executable, "scripts/process.py",
            "--input", self.input_file,
            "--output", self.output_file
        ]
        
        subprocess.check_call(cmd)
        self.next(self.join)

    @step
    def join(self, inputs):
        input_paths = [input.output_file for input in inputs]
        self.config = inputs[0].config
        self.run_id = inputs[0].run_id
        
        out_dir = self.config['paths']['output_dir']
        self.final_output = os.path.join(out_dir, f"final_combined_{self.run_id}.csv")
        
        logger.info(f"Combining files into {self.final_output}")
        
        queue = self.config['compute']['lsf_queue']
        
        cmd = [
            "bsub", "-q", queue, "-K",
            "bash", "bash/combine.sh",
            self.final_output
        ] + input_paths
        
        env = os.environ.copy()
        env['PATH'] = f"{os.getcwd()}:{env['PATH']}"
        
        subprocess.check_call(cmd, env=env)
        self.next(self.analyze)

    @step
    def analyze(self):
        logger.info("Analyzing result using Docker...")
        
        # Mount the output directory instead of data directory
        out_dir = os.path.abspath(self.config['paths']['output_dir'])
        docker_image = self.config['compute']['docker_image']
        
        # File is at /out/<filename> inside container
        container_path = f"/out/{os.path.basename(self.final_output)}"
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{out_dir}:/out",
            docker_image,
            "wc", "-l", container_path
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        try:
            subprocess.check_call(cmd)
        except (subprocess.CalledProcessError, FileNotFoundError, Exception) as e:
            logger.error(f"Docker analysis failed: {e}")
            
        self.next(self.end)

    @step
    def end(self):
        logger.info("Flow finished successfully!")
        logger.info(f"Result available at: {self.final_output}")

if __name__ == '__main__':
    StudentDataFlow()
