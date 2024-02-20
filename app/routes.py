from flask import render_template, Blueprint, request, redirect, send_file, send_from_directory, Response, jsonify
import subprocess
from pathlib import Path
import base64
import hashlib

routes = Blueprint('app', __name__)


def sha256code(data):
    data = data.encode('utf-8')
    
    sha256_hash = hashlib.sha256(data).hexdigest()
    
    return sha256_hash

@routes.route('/')
def index():
    ipClient = Path(f"userCodes/{sha256code(request.remote_addr)}.py")

    code = ""

    if ipClient.is_file():
        with open(f"userCodes/{sha256code(request.remote_addr)}.py", "r") as arquivo:
            conteudo = arquivo.read()
            code = conteudo
    else:
        code = """import HelloProgrammer
import coffe
import keyboard

print("Welcome to CloudPython, your Python online interpreter!")

    # You can run your code with the keyword F5.
    # You can get a picture of your code by using ray.so with F3.
    # You can download your code with ctrl + s.
    # You can switch between the editor and terminal using F2
    # You can share your code with F4
    # Get this welcome by clicking the upper right button.
    # Some libraries are blocked for security on our site.
    # If you need to contact me, my GitHub handle is @wezlleyv
    # This project is open-source you can see the code in:
    # www.github.com/wezlleyv/cloudpython
        
print("Now, you can grab a coffee and code!")
"""

    return render_template('index.html', codeprevious=code)

@routes.route('/download/<code>')
def download_file(code):
    try:
        with open(f"userCodes/{sha256code(request.remote_addr)}.py", "w") as file:
            text = base64.b64decode(code)
            text = text.decode("utf-8")
            file.write(text)
            file.close()
        return send_file(Path(f"../userCodes/{sha256code(request.remote_addr)}.py"), as_attachment=True, download_name="main.py")
    except Exception as e:
        return str(e), 500

@routes.route('/share/<code>')
def share_code(code):
    shareCode = base64.b64decode(code)
    shareCode = shareCode.decode('utf-8')
    return render_template('index.html', codeprevious=shareCode)

@routes.route('/python', methods=['POST'])
def interpreterCode():
    if request.method == "POST":
        data = request.form.get("code")
        
        with open(f"userCodes/{sha256code(request.remote_addr)}.py", "w") as file:
            file.write(data)

        file.close()

        try:
            resultado = subprocess.check_output(['python', f"userCodes/{sha256code(request.remote_addr)}.py"], stderr=subprocess.STDOUT, timeout=10, universal_newlines=True)
            return resultado

        except SyntaxError as e:
            return e
    
        except subprocess.CalledProcessError as e:
            return jsonify({'erro': e.output}), 400
        
        except subprocess.TimeoutExpired:
            return jsonify({'erro': 'Tempo limite excedido ao executar o código'}), 400
        
        except Exception as e:
            return jsonify({'erro': str(e)}), 400