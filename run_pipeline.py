# run_pipeline.py
# ../run_pipeline.py
# Script to run the entire data pipeline: collection, cleaning, and prediction

import subprocess
import os

# Function to run a script and handle errors
def run_script(script_path, script_dir):
    try:
        subprocess.run(['python', script_path], cwd=script_dir, check=True)
        print(f"Successfully ran {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")

# Ensure plot_images directory exists
plot_images_dir = os.path.expanduser("../data/plot_images")
if not os.path.exists(plot_images_dir):
    os.makedirs(plot_images_dir)

# Paths to the scripts and their directories
data_collection_script = 'data_collection.py'
data_cleaning_script = 'data_cleaning.py'
prediction_script = 'prediction.py'

data_collection_dir = os.path.join('data_collection')
data_cleaning_dir = os.path.join('data_cleaning')
prediction_dir = os.path.join('prediction')

# Run the scripts sequentially
run_script(data_collection_script, data_collection_dir)
run_script(data_cleaning_script, data_cleaning_dir)
run_script(prediction_script, prediction_dir)

print("Data pipeline execution complete.")
