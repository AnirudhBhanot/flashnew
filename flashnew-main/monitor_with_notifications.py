#!/usr/bin/env python3
"""
Monitor training progress and send notifications when each model completes
"""

import time
import subprocess
import re
from datetime import datetime
import os

def send_notification(title, message):
    """Send macOS notification"""
    cmd = f'''osascript -e 'display notification "{message}" with title "{title}" sound name "Glass"' '''
    subprocess.run(cmd, shell=True)

def check_training_status(log_file):
    """Check current training status from log file"""
    if not os.path.exists(log_file):
        return None, "Log file not found"
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Check for completion markers
    models_status = {
        'DNA Analyzer': {
            'pattern': r'DNA Analyzer training completed in (\d+\.\d+) minutes',
            'start_pattern': r'TRAINING DNA ANALYZER',
            'completed': False
        },
        'Temporal Model': {
            'pattern': r'Temporal Model training completed in (\d+\.\d+) minutes',
            'start_pattern': r'TRAINING TEMPORAL MODEL',
            'completed': False
        },
        'Industry Model': {
            'pattern': r'Industry Model training completed in (\d+\.\d+) minutes',
            'start_pattern': r'TRAINING INDUSTRY MODEL',
            'completed': False
        },
        'Ensemble Model': {
            'pattern': r'Ensemble Model training completed in (\d+\.\d+) minutes',
            'start_pattern': r'TRAINING ENSEMBLE MODEL',
            'completed': False
        }
    }
    
    # Check what's completed
    for model, info in models_status.items():
        if re.search(info['pattern'], content):
            info['completed'] = True
            match = re.search(info['pattern'], content)
            if match:
                info['time'] = match.group(1)
    
    # Check if training is complete
    if "TRAINING COMPLETE!" in content:
        return "complete", models_status
    
    # Check what's currently training
    current_model = None
    for model, info in models_status.items():
        if re.search(info['start_pattern'], content) and not info['completed']:
            current_model = model
            break
    
    return current_model, models_status

def monitor_training():
    """Main monitoring loop"""
    log_file = "/Users/sf/Desktop/FLASH/training_logs/training_20250604_110743.log"
    pid = 1944
    
    print("="*60)
    print("TRAINING MONITOR WITH NOTIFICATIONS")
    print("="*60)
    print(f"Monitoring PID: {pid}")
    print(f"Log file: {log_file}")
    print("You'll receive notifications when each model completes.")
    print("="*60)
    
    # Track what we've already notified about
    notified = set()
    last_status = None
    
    while True:
        # Check if process is still running
        try:
            subprocess.check_output(f"ps -p {pid}", shell=True)
            process_running = True
        except:
            process_running = False
        
        # Get current status
        current_model, models_status = check_training_status(log_file)
        
        # Check for newly completed models
        for model, info in models_status.items():
            if info['completed'] and model not in notified:
                time_taken = info.get('time', 'unknown')
                send_notification(
                    f"✅ {model} Complete",
                    f"Training completed in {time_taken} minutes"
                )
                print(f"\n✅ {model} completed in {time_taken} minutes")
                notified.add(model)
        
        # Update status display
        if current_model != last_status:
            if current_model == "complete":
                send_notification(
                    "🎉 Training Complete!",
                    "All models have been trained successfully"
                )
                print("\n🎉 All training complete!")
                
                # Show summary
                print("\nTraining Summary:")
                for model, info in models_status.items():
                    if info['completed']:
                        print(f"  - {model}: {info.get('time', 'unknown')} minutes")
                
                break
            elif current_model:
                print(f"\n🔄 Currently training: {current_model}")
                print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                last_status = current_model
        
        if not process_running:
            send_notification(
                "⚠️ Training Stopped",
                "The training process has stopped unexpectedly"
            )
            print("\n⚠️ Training process has stopped!")
            break
        
        # Wait 30 seconds before next check
        time.sleep(30)
        print(".", end="", flush=True)

if __name__ == "__main__":
    try:
        monitor_training()
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        send_notification("❌ Monitor Error", str(e))