from flask import Flask, jsonify, request, send_file
import threading
import sys
import os
import glob

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.hr_agent.agent import HRAgent, load_config

app = Flask(__name__)

# Global state (MVP style)
class AgentState:
    def __init__(self):
        self.is_running = False
        self.last_report = None
        self.status = "Idle"

state = AgentState()

def run_agent_task():
    global state
    state.is_running = True
    state.status = "Running Analysis..."
    
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'hr_competitors.yaml')
        config = load_config(config_path)
        agent = HRAgent(config)
        
        # Run Analysis
        df = agent.run_analysis()
        
        # Generate Report
        agent.generate_report(df)
        
        # Find the latest report
        list_of_files = glob.glob('*.xlsx')
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            state.last_report = latest_file
            
        state.status = "Completed"
    except Exception as e:
        state.status = f"Error: {str(e)}"
        print(f"Error running agent: {e}")
    finally:
        state.is_running = False

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "HR Competitive Analysis Agent API is running.",
        "endpoints": [
            "POST /api/v1/analyze",
            "GET /api/v1/status",
            "GET /api/v1/report/latest"
        ]
    })

@app.route('/api/v1/analyze', methods=['POST'])
def trigger_analysis():
    if state.is_running:
        return jsonify({"message": "Analysis already running", "status": state.status}), 409
    
    thread = threading.Thread(target=run_agent_task)
    thread.start()
    
    return jsonify({"message": "Analysis started", "status": "Running"}), 202

@app.route('/api/v1/status', methods=['GET'])
def get_status():
    return jsonify({
        "is_running": state.is_running,
        "status": state.status,
        "last_report": state.last_report
    })

@app.route('/api/v1/report/latest', methods=['GET'])
def get_latest_report():
    if not state.last_report or not os.path.exists(state.last_report):
        return jsonify({"error": "No report found. Run analysis first."}), 404
        
    return send_file(
        os.path.abspath(state.last_report),
        as_attachment=True,
        download_name=state.last_report
    )

if __name__ == '__main__':
    # Disable debug mode to prevent reload on report generation
    app.run(host='0.0.0.0', port=5000, debug=False)
