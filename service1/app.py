from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# Hardcoded employee data — no database needed for this lab
EMPLOYEES = [
    {"id": 1, "name": "Alice Johnson",   "department": "IT Security",  "salary": 120000, "email": "alice@company.com"},
    {"id": 2, "name": "Bob Martinez",    "department": "Operations",    "salary": 65000,  "email": "bob@company.com"},
    {"id": 3, "name": "Charlie Singh",   "department": "Finance",       "salary": 85000,  "email": "charlie@company.com"},
    {"id": 4, "name": "Diana Fernandez", "department": "HR",            "salary": 75000,  "email": "diana@company.com"},
    {"id": 5, "name": "Eric Wang",       "department": "Engineering",   "salary": 95000,  "email": "eric@company.com"},
]


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "Employee API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


@app.route('/employees', methods=['GET'])
def get_employees():
    # No auth check here — auth is handled by Kong gateway
    return jsonify({
        "service": "Employee API",
        "count": len(EMPLOYEES),
        "data": EMPLOYEES
    })


@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    employee = next((e for e in EMPLOYEES if e['id'] == emp_id), None)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"service": "Employee API", "data": employee})


@app.route('/employees/department/<dept>', methods=['GET'])
def get_by_department(dept):
    results = [e for e in EMPLOYEES if e['department'].lower() == dept.lower()]
    return jsonify({
        "service": "Employee API",
        "department": dept,
        "count": len(results),
        "data": results
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
