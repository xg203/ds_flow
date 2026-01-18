from metaflow import FlowSpec, step
import pandas as pd
import glob
import os
from datetime import datetime

class StudentDataFlow(FlowSpec):

    @step
    def start(self):
        self.files = glob.glob('data/*.csv')
        print(f"Found files: {self.files}")
        self.next(self.process_file, foreach='files')

    @step
    def process_file(self):
        self.filename = self.input
        print(f"Processing {self.filename}")
        
        # Read the file
        df = pd.read_csv(self.filename)
        
        # Add a column
        df['processed_at'] = datetime.now()
        df['source_file'] = os.path.basename(self.filename)
        
        self.df = df
        self.next(self.join)

    @step
    def join(self, inputs):
        self.combined_df = pd.concat([input.df for input in inputs])
        print("Combined Data:")
        print(self.combined_df)
        self.next(self.end)

    @step
    def end(self):
        print("Flow finished!")

if __name__ == '__main__':
    StudentDataFlow()
