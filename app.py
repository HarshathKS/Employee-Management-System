import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file,
    jsonify
)
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Secret Key
app.secret_key = "employee_secret_key"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'AddYourUsername'
app.config['MYSQL_PASSWORD'] = 'AddYourPassword'
app.config['MYSQL_DB'] = 'employee_management'

mysql = MySQL(app)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cur.fetchone()

        cur.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect('/dashboard')

        return "Invalid Username or Password"

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'username' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM employees")
    total_employees = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT department) FROM employees")
    total_departments = cur.fetchone()[0]

    cur.execute("SELECT AVG(salary) FROM employees")
    avg_salary = cur.fetchone()[0]

    cur.close()

    return render_template(
        'dashboard.html',
        username=session['username'],
        total_employees=total_employees,
        total_departments=total_departments,
        avg_salary=avg_salary
    )


# ---------------- EMPLOYEES LIST ----------------
@app.route('/employees')
def employees():

    if 'username' not in session:
        return redirect('/login')

    search = request.args.get('search')

    cur = mysql.connection.cursor()

    if search:
        cur.execute("""
            SELECT *
            FROM employees
            WHERE name LIKE %s
            OR department LIKE %s
        """, (f"%{search}%", f"%{search}%"))
    else:
        cur.execute("SELECT * FROM employees")

    employees = cur.fetchall()

    cur.close()

    return render_template(
        'employees.html',
        employees=employees
    )


# ---------------- ADD EMPLOYEE ----------------
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():

    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        salary = request.form['salary']
        joining_date = request.form['joining_date']

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO employees
            (name, email, phone, department, salary, joining_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            name,
            email,
            phone,
            department,
            salary,
            joining_date
        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/employees')

    return render_template('add_employee.html')


# ---------------- EDIT EMPLOYEE ----------------
@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):

    if 'username' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        salary = request.form['salary']
        joining_date = request.form['joining_date']

        cur.execute("""
            UPDATE employees
            SET
                name=%s,
                email=%s,
                phone=%s,
                department=%s,
                salary=%s,
                joining_date=%s
            WHERE id=%s
        """, (
            name,
            email,
            phone,
            department,
            salary,
            joining_date,
            id
        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/employees')

    cur.execute(
        "SELECT * FROM employees WHERE id=%s",
        (id,)
    )

    employee = cur.fetchone()

    cur.close()

    return render_template(
        'edit_employee.html',
        employee=employee
    )


# ---------------- DELETE EMPLOYEE ----------------
@app.route('/delete_employee/<int:id>')
def delete_employee(id):

    if 'username' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    return redirect('/employees')


# ---------------- API ----------------
@app.route('/api/employees')
def api_employees():

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            department,
            salary,
            joining_date
        FROM employees
    """)

    rows = cur.fetchall()

    cur.close()

    employees = []

    for row in rows:
        employees.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "department": row[4],
            "salary": row[5],
            "joining_date": str(row[6])
        })

    return jsonify(employees)


# ---------------- EXPORT EXCEL ----------------
@app.route('/export')
def export_excel():

    if 'username' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            department,
            salary,
            joining_date
        FROM employees
    """)

    rows = cur.fetchall()

    cur.close()

    df = pd.DataFrame(
        rows,
        columns=[
            'ID',
            'Name',
            'Email',
            'Phone',
            'Department',
            'Salary',
            'Joining Date'
        ]
    )

    df['Phone'] = df['Phone'].astype(str)

    filename = "employees.xlsx"

    with pd.ExcelWriter(
        filename,
        engine='openpyxl'
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name='Employees'
        )

    return send_file(
        filename,
        as_attachment=True
    )


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('username', None)

    return redirect('/login')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)

