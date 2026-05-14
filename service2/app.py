from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

PROJECTS = [
    {"id": 1, "name": "Network Upgrade",  "status": "active",   "budget": 250000, "owner": "alice",   "priority": "high"},
    {"id": 2, "name": "Security Audit",   "status": "active",   "budget": 85000,  "owner": "bob",     "priority": "critical"},
    {"id": 3, "name": "Cloud Migration",  "status": "planning", "budget": 500000, "owner": "charlie", "priority": "high"},
    {"id": 4, "name": "Payroll System",   "status": "active",   "budget": 175000, "owner": "alice",   "priority": "medium"},
    {"id": 5, "name": "DR Site Setup",    "status": "planning", "budget": 320000, "owner": "eric",    "priority": "high"},
]

TASKS = [
    {"id": 1, "project_id": 1, "title": "Inventory switches",      "assigned_to": "bob",     "status": "open"},
    {"id": 2, "project_id": 1, "title": "Draft upgrade plan",      "assigned_to": "charlie", "status": "in-progress"},
    {"id": 3, "project_id": 2, "title": "Run vulnerability scan",  "assigned_to": "bob",     "status": "open"},
    {"id": 4, "project_id": 2, "title": "Review firewall rules",   "assigned_to": "diana",   "status": "open"},
    {"id": 5, "project_id": 3, "title": "Assess app dependencies", "assigned_to": "eric",    "status": "open"},
]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "Projects API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route('/projects', methods=['GET'])
def get_projects():
    return jsonify({
        "service": "Projects API",
        "count": len(PROJECTS),
        "data": PROJECTS
    })


@app.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"service": "Projects API", "data": project})


@app.route('/projects/<int:project_id>/tasks', methods=['GET'])
def get_tasks(project_id):
    tasks = [t for t in TASKS if t['project_id'] == project_id]
    return jsonify({
        "service": "Projects API",
        "project_id": project_id,
        "count": len(tasks),
        "data": tasks
    })


@app.route('/projects/status/<status>', methods=['GET'])
def get_by_status(status):
    results = [p for p in PROJECTS if p['status'].lower() == status.lower()]
    return jsonify({
        "service": "Projects API",
        "status_filter": status,
        "count": len(results),
        "data": results
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
