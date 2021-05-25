import pyodbc
from flask import Flask, redirect, url_for, render_template, request, session,jsonify
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

server = 'DESKTOP-24OJSD9'
database = 'bank'

cons = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER='+server+';\
        DATABASE='+database+'; \
            Trusted_connection=yes;')

cursor = cons.cursor()
cursor.execute('Select * from bank.dbo.AccountInfo')


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username']) +'''<button id="user_login" class="float-left submit-button" >Log out</button>

            <script type="text/javascript">
                document.getElementById("user_login").onclick = function () {
                    location.href = "http://127.0.0.1:5000/logout";
                };
            </script> '''
    return '''<button id="user_login" class="float-left submit-button" >Log in for user</button>

            <script type="text/javascript">
                document.getElementById("user_login").onclick = function () {
                    location.href = "http://127.0.0.1:5000/login-user";
                };
            </script>

    <button id="admin_login" class="float-left submit-button" >Log in for admin</button>

    <script type="text/javascript">
    document.getElementById("admin_login").onclick = function () {
        location.href = "http://127.0.0.1:5000/login-admin";
    };
    </script>'''

@app.route('/login-user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username=request.form['username']
        cursor.execute('Select top 1 AccountId from bank.dbo.AccountInfo where AccountID=?', username)
        result = cursor.fetchall()
        if len(result)!=0:
            pas=request.form['password']
            cursor.execute('Select top 1 Pass from bank.dbo.AccountInfo where AccountID=? and Pass=?', (username,pas))
            res=cursor.fetchall()
            if len(res)!=0:
                session['username'] = username
                return redirect(url_for('user'))
    return '''
        <form method="post" id="user_login">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
              </form>
              <button type="submit" form="user_login" value="Submit">Log in</button>
'''

@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        return '''<button id="new-account" class="float-left submit-button"  >Deposit</button>

            <script type="text/javascript">
                document.getElementById("new-account").onclick = function () {
                    location.href = "http://127.0.0.1:5000/user/deposit";
                };
            </script>

    

    <button id="see-all3" class="float-left submit-button" >Withdraw</button>

    <script type="text/javascript">
    document.getElementById("see-all3").onclick = function () {
        location.href = "http://127.0.0.1:5000/user/withdraw";
    };
    </script>

    <button id="see-all2" class="float-left submit-button" >Transfer</button>

    <script type="text/javascript">
    document.getElementById("see-all2").onclick = function () {
        location.href = "http://127.0.0.1:5000/user/transfer";
    };
    </script>

    <button id="see-all4" class="float-left submit-button" >Save money</button>

    <script type="text/javascript">
    document.getElementById("see-all4").onclick = function () {
        location.href = "http://127.0.0.1:5000/user/save-money";
    };
    </script>

<button id="change" class="float-left submit-button" >Change password</button>

    <script type="text/javascript">
    document.getElementById("change").onclick = function () {
        location.href = "http://127.0.0.1:5000/user/change-password";
    };
    </script>

    <button id="user_login" class="float-left submit-button" >Log out</button>

            <script type="text/javascript">
                document.getElementById("user_login").onclick = function () {
                    location.href = "http://127.0.0.1:5000/logout";
                };
            </script> '''
    return redirect(url_for('login-user'))

@app.route('/user/change-password', methods=['GET', 'POST'])
def change_password():
    if 'username' in session:
        if request.method == 'POST':
            if request.form['new'] == request.form['confirm']:
                username=session['username']
                password=request.form['password']
                cursor.execute('Select top 1 Pass from bank.dbo.AccountInfo where Pass=?', password)
                cursor.execute('update AccountInfo set Pass=? where AccountId=?;',(request.form['confirm'],username) )
                return 'Password changed  '+'''<button id="admin" class="float-left submit-button" >Back</button>

                <script type="text/javascript">
                    document.getElementById("admin").onclick = function () {
                        location.href = "http://127.0.0.1:5000/user";
                    };
                </script> '''
            return ''' <form method="post" id="user_login">
                    <label for="password">Your old password:</label>
                    <input type="password" id="password" name="password" required>
                    <label for="new"> New password:</label>
                    <input type="password" id="new" name="new" required>
                    <label for="confirm"> Confirm new password:</label>
                    <input type="password" id="confirm" name="confirm" required>
                  </form>
                   <button type="submit" form="user_login" value="Submit">Change password</button>

                  <button id="out" class="float-left submit-button" >Cancel</button>

    <script type="text/javascript">
    document.getElementById("out").onclick = function () {
        location.href = "http://127.0.0.1:5000/user";
    };
    </script>'''
        return ''' <form method="post" id="user_login">
                    <label for="password">Your old password:</label>
                    <input type="password" id="password" name="password" required>
                    <label for="new"> New password:</label>
                    <input type="password" id="new" name="new" required>
                    <label for="confirm"> Confirm new password:</label>
                    <input type="password" id="confirm" name="confirm" required>
                  </form>
                   <button type="submit" form="user_login" value="Submit">Change password</button>

                  <button id="out" class="float-left submit-button" >Cancel</button>

    <script type="text/javascript">
    document.getElementById("out").onclick = function () {
        location.href = "http://127.0.0.1:5000/user";
    };
    </script>'''
    return redirect(url_for('login_user'))
@app.route('/user/transfer', methods=['GET', 'POST'])
def transfer(): # xac thuc mat khau -> Thuc hien transaction -> tru tien username_from, Cong tien username_to
    if 'username' in session:
        if request.method == 'POST':
            username_to=request.form['username']
            username_from=session['username']
            amount=request.form['amount']
            pas=request.form['password']
            cursor.execute('Select top 1 Pass from bank.dbo.AccountInfo where AccountID=? and Pass=?', (username_from,pas))
            res=cursor.fetchall()
            if len(res)!=0:
                cursor.execute(' update AccountInfo set amount=amount - ? where AccountId=?; ',(amount,username_from))
                cons.commit()
                cursor.execute(' update AccountInfo set amount=amount + ? where AccountId=?;',(amount,username_to))
                cons.commit()
                strin='Transfer money'
                cursor.execute('insert into  trans(act,moment,username_from,username_to,amount) values( ?,getdate(),?,?,?)',(strin,username_from,username_to,amount))
                cons.commit()
                return 'Succesfully transferred!    '+ '''<button id="user_login" class="float-left submit-button" >Log out</button>

            <script type="text/javascript">
                document.getElementById("user_login").onclick = function () {
                    location.href = "http://127.0.0.1:5000/logout";
                };
            </script> 
            <button id="see-all2" class="float-left submit-button" >Back to user</button>

    <script type="text/javascript">
    document.getElementById("see-all2").onclick = function () {
        location.href = "http://127.0.0.1:5000/user";
    };'''
        return ''' <form method="post" id="user_login">
                    <label for="username">Target user:</label>
                    <input type="text" id="username" name="username" required><br><br>
                    <label for="amount">Amount:</label>
                    <input type="number" id="amount" name="amount" required>
                    <label for="password">Confirm password:</label>
                    <input type="password" id="password" name="password" required>
                  </form>
                   <button type="submit" form="user_login" value="Submit">Log in</button>

                  <button id="see-all2" class="float-left submit-button" >Cancel</button>

    <script type="text/javascript">
    document.getElementById("see-all2").onclick = function () {
        location.href = "http://127.0.0.1:5000/user";
    };
    </script>
    '''
    return redirect(url_for('login_user'))
    
@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():  
    if request.method == 'POST':
        username=request.form['username']
        cursor.execute('Select top 1 AccountId from bank.dbo.Admin where AccountID=?', username)
        result = cursor.fetchall()
        if len(result)!=0:
            pas=request.form['password']
            cursor.execute('Select top 1 Pass from bank.dbo.Admin where AccountID=? and Pass=?', (username,pas))
            res=cursor.fetchall()
            if len(res)!=0:
                session['username'] = username
                return redirect(url_for('admin'))
    return '''
        <form method="post" id="user_login">
                <label for="username">Admin:</label>
                <input type="text" id="username" name="username" required><br><br>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
              </form>
              <button type="submit" form="user_login" value="Submit">Log in</button>
'''

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        return '''<button id="new-account" class="float-left submit-button" >Create new user account</button>

            <script type="text/javascript">
                document.getElementById("new-account").onclick = function () {
                    location.href = "http://127.0.0.1:5000/admin/new-account";
                };
            </script>

    <button id="see-all" class="float-left submit-button" >See all user accounts</button>

    <script type="text/javascript">
    document.getElementById("see-all").onclick = function () {
        location.href = "http://127.0.0.1:5000/admin/see-all-account";
    };
    </script>

<button id="viewtransaction" class="float-left submit-button" >View transaction</button>

            <script type="text/javascript">
                document.getElementById("viewtransaction").onclick = function () {
                    location.href = "http://127.0.0.1:5000/admin/view-transaction";
                };
            </script>
    <button id="user_login" class="float-left submit-button" >Log out</button>

            <script type="text/javascript">
                document.getElementById("user_login").onclick = function () {
                    location.href = "http://127.0.0.1:5000/logout";
                };
            </script>
              '''
    return redirect(url_for('login_admin'))

@app.route('/admin/view-transaction', methods=['GET', 'POST'])
def view_transaction():
    if 'username' in session:
        cursor.execute('select act,moment,username_from,username_to,amount from trans Group by act,moment,username_from,username_to,amount')
        result = cursor.fetchall()
        data=[]
        for row in result:
            data.append([x for x in row])
        if len(result) ==0:
            return 'There is no transaction in the system' +'''<button id="admin" class="float-left submit-button" >Return to admin</button>

            <script type="text/javascript">
                document.getElementById("admin").onclick = function () {
                    location.href = "http://127.0.0.1:5000/admin";
                };
            </script> '''
        jsed=jsonify(data)
        return jsed
    return """<button id="user_login" class="float-left submit-button" >Back</button>

            <script type="text/javascript">
                document.getElementById("user_login").onclick = function () {
                    location.href = "http://127.0.0.1:5000/admin";
                };
            </script>"""
@app.route('/admin/new-account', methods=['GET', 'POST'])
def new_account():
    if 'username' in session:
        if request.method == 'POST':
            accountid=request.form['accountid']
            pas=request.form['password']
            amount=request.form['amount']
            cursor.execute("insert into AccountInfo (AccountID,Pass,Amount) values(?,?,?)", (accountid,pas,amount))
            cons.commit()
            return 'Created account: '+accountid+' with $'+amount+'       '+'''<button id="admin" class="float-left submit-button" >Return to admin</button>

                <script type="text/javascript">
                    document.getElementById("admin").onclick = function () {
                        location.href = "http://127.0.0.1:5000/admin";
                    };
                </script> '''
        return '''
           <form method="post" id="newaccount">
                  <label for="account-id">Account Id:</label>
                  <input type="text" id="accountid" name="accountid" maxlength="15" required><br><br>
                  <label for="password">Password:</label>
                 <input type="password" id="password" name="password" required><br><br>
                    <label for="amount">Amount:</label>
                 <input type="number" id="amount" name="amount" min="50000" required>
               </form>
               <button type="submit" form="newaccount" value="Submit">Create new account</button>
    '''
    return redirect(url_for('login_admin'))
@app.route('/admin/see-all-account', methods=['GET', 'POST'])
def see_all_account():
    if 'username' in session:
        cursor.execute('select AccountId,Amount from AccountInfo Group by AccountId,Amount')
        #cursor.execute('select * from AccountInfo')
        result = cursor.fetchall()
        data=[]
        for row in result:
            data.append([x for x in row])
        if len(result) ==0:
            return 'There is no account in the system' +'''<button id="admin" class="float-left submit-button" >Return to admin</button>

            <script type="text/javascript">
                document.getElementById("admin").onclick = function () {
                    location.href = "http://127.0.0.1:5000/admin";
                };
            </script> '''
        jsed=jsonify(data)
        return jsed
    return redirect(url_for('login_admin'))
if __name__=="__main__":
    app.run()
