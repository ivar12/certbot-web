import cherrypy
import subprocess
import os
import shutil
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

class CertbotWeb:
    @cherrypy.expose
    def index(self, domain=None, action=None):
        message = ""
        if cherrypy.request.method == "POST" and domain and action:
            domain = domain.strip()
            if action == "issue":
                message = self.run_certbot_issue(domain)
            elif action == "renew":
                message = self.run_certbot_renew(domain)

        tmpl = env.get_template("index.html")
        cherrypy.response.headers['Content-Type'] = 'text/html'
        return tmpl.render(message=message)

    def run_certbot_issue(self, domain):
        cmd = [
            "certbot", "certonly",
            "--dns-cloudflare",
            "--dns-cloudflare-credentials", "/secrets/cloudflare.ini",
            "--non-interactive", "--agree-tos",
            "--email", "ivar@networktechlab.nl",
            "-d", domain
        ]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                self.copy_certs(domain)
            return f'<div class="alert alert-success" role="alert"><h3>Certificate for {domain} created successfully.</h3></div><pre>{result.stdout.decode()}</pre></div>'
        except Exception as e:
            return f"<h3>Error issuing certificate for {domain}:</h3><pre>{e}</pre>"

    def run_certbot_renew(self, domain):
        cmd = ["certbot", "renew", "--cert-name", domain]
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                self.copy_certs(domain)
            return f'<div class="alert alert-success" role="alert"><h3>Certificate for {domain} renewed successfully.</h3></div><pre>{result.stdout.decode()}</pre>'
        except Exception as e:
            return f"<h3>Error renewing certificate for {domain}:</h3><pre>{e}</pre>"

    def copy_certs(self, domain):
        source_dir = f"/etc/letsencrypt/live/{domain}"
        dest_dir = f"/public-certs/{domain}"

        os.makedirs(dest_dir, exist_ok=True)

        for filename in ["fullchain.pem", "privkey.pem"]:
            src = os.path.join(source_dir, filename)
            dst = os.path.join(dest_dir, filename)

            if os.path.exists(src):
                shutil.copy2(src, dst)
                os.chmod(dst, 0o644)

if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080
    })

    cherrypy.quickstart(
        CertbotWeb(),
        "/",
        {
            "/": {
                "tools.sessions.on": True,
                "tools.staticdir.root": os.path.abspath(os.getcwd())
            },
            "/static": {
                "tools.staticdir.on": True,
                "tools.staticdir.dir": "static"
            }
        }
    )