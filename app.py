import os
import ftplib
from flask import Flask, redirect, url_for, render_template, send_file, request
from werkzeug.utils import secure_filename
from forms import LoginForm, MakeDirectory, UploadForm
app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = 'secret_key'  

path = ''



@app.route('/task', methods=['POST'])
def task():
    host = request.form['host']
    username = request.form['username']
    password = request.form['password']
    path = request.form['path']
    ftp = ftplib.FTP(host, username, password)
    ftp.cwd('/')
    ftp.cwd('Litvinov_4041')
    print(ftp.nlst())
    directories = ftp.nlst()
    for i in range(65, 73):
        if chr(i) in directories:
            ftp.cwd(chr(i))
            for d in ftp.nlst():
                ftp.rmd(d)
            ftp.cwd('..')
        ftp.mkd(chr(i))
        ftp.cwd(chr(i))
        for i in range(10):
            ftp.mkd(str(i))
        ftp.cwd('..')
    ftp.nlst()
    return redirect(url_for('ftp_connection', host = host, username = username, password=password, path=path))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            host = form.hostname.data
            username = form.username.data
            password = form.password.data
            ftp = ftplib.FTP(host, username, password)
            print(ftp.nlst())
            ftp.quit()
            return redirect(url_for('ftp_connection', host=host, username=username, password=password, path = 'start'))
        except:
            return redirect(url_for('wrong_data'))
    return render_template('login.html', form=form)

@app.route('/ftp_connection/<host>/<username>/<password>/<path>', methods = ['GET', 'POST'])
def ftp_connection(host, username, password, path):
    ftp = ftplib.FTP(host, username, password)
    if path == 'start':
        path_list = ['start']
        ftp.cwd('/')
        content = ftp.nlst()
    else:
        path_list = path.split('+')
        path = '/'.join(path_list[1:])
        ftp.cwd(path)
        content = ftp.nlst()
    ftp.quit()
    files = []
    directories = []
    for c in content:
        if '.' in c:
            files.append(c)
        else:
            directories.append(c)
    return render_template('ftp_connection.html', files=files, directories=directories, path_list = path_list, host=host, username=username, password=password)

@app.route('/download/<host>/<username>/<password>/<path>/<target_file>', methods = ['GET', 'POST'])
def download(host, username, password, path, target_file):
    ftp = ftplib.FTP(host, username, password)
    if path == 'start':
        ftp.cwd('/')
    else:
        path_list = path.split('+')
        ftp.cwd('/' + '/'.join(path_list[1:]))
    local_filename = f'D:/cloud_technologies/{target_file}'
    with open(local_filename, 'wb') as file:
        ftp.retrbinary('RETR ' + target_file, file.write)
    ftp.quit()
    send_file(local_filename, as_attachment=True)
    return redirect(url_for('ftp_connection', host = host, username = username, password=password, path=path))


@app.route('/upload_files/<host>/<username>/<password>/<path>', methods=['GET', 'POST'])
def upload_files(host, username, password, path):
    ftp = ftplib.FTP(host, username, password)
    if path == 'start':
        path_list = ['start']
        ftp.cwd('/')
        content = ftp.nlst()
    else:
        path_list = path.split('+')
        path = '/'.join(path_list[1:])
        ftp.cwd(path)
        content = ftp.nlst()
    files = []
    directories = []
    for c in content:
        if '.' in c:
            files.append(c)
        else:
            directories.append(c)
    ftp.quit()
    return render_template('upload_files.html', files=files, directories=directories, path_list = path_list, host=host, username=username, password=password)


@app.route('/upload', methods=['POST'])
def upload():
    host = request.form['host']
    username = request.form['username']
    password = request.form['password']
    path = request.form['path']
    ftp = ftplib.FTP(host, username, password)
    if path == 'start':
        path_list = ['start']
        ftp.cwd('/')
    else:
        path_list = path.split('+')
        path = '/'.join(path_list[1:])
        ftp.cwd(path)
    if 'file' not in request.files:
        return 'Файл не был загружен'
    file = request.files['file']
    if file.filename == '':
        return 'Файл не был выбран'
    if file:
        ftp.storbinary(f'STOR {file.filename}', file)
        ftp.quit()
        return render_template('upload_success.html')
    return 'Произошла ошибка при загрузке файла'



@app.route('/make_catalog/<host>/<username>/<password>/<path>', methods = ['GET', 'POST'])
def make_catalog(host, username, password, path):
    ftp = ftplib.FTP(host, username, password)
    if path == 'start':
        path_list = ['start']
        ftp.cwd('/')
        content = ftp.nlst()
    else:
        path_list = path.split('+')
        path = '/'.join(path_list[1:])
        ftp.cwd(path)
        content = ftp.nlst()
    files = []
    directories = []
    for c in content:
        if '.' in c:
            files.append(c)
        else:
            directories.append(c)
    form = MakeDirectory()
    if form.validate_on_submit():
        ftp.mkd(form.catalog_name.data)
        ftp.quit()
        return redirect(url_for('ftp_connection', host = host, username = username, password=password, path='+'.join(path_list)))
    return render_template('make_catalog.html', form=form, files=files, directories=directories, path_list = path_list, host=host, username=username, password=password)

@app.route('/wrong_data')
def wrong_data():
    return render_template('wrong_data.html')

if __name__ == '__main__':
    app.run(debug=True)
