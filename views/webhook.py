from views.base import BaseHandler


class WebHookHandler(BaseHandler):

    def post(self, *args, **kwargs):
        import subprocess
        cwd = "/root/src/anotherWeb"
        subprocess.Popen("git pull origin master; supervisorctl restart all", cwd=cwd, shell=True)

