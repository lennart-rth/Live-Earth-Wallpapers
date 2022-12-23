import os
import re
import subprocess
import pathlib
import subprocess
import xml.etree.ElementTree as ET

class Systemd:
    def __init__(self):
        self.service_name = "liewa.service"
        self.timer_name = "liewa.timer"

    def update(self):
        timer_cmd = f"systemctl --user status {self.timer_name}"
        service_cmd = f"systemctl --user status {self.service_name}"
        proc = subprocess.Popen(timer_cmd.split(), stdout=subprocess.PIPE)
        timer_output = proc.communicate()[0].decode("utf-8")
        proc = subprocess.Popen(service_cmd.split(), stdout=subprocess.PIPE)
        service_output = proc.communicate()[0].decode("utf-8")
        running = False
        if re.search("(?<=Active:\s)\w*", timer_output):
            running = True

        return timer_output+'\n'+service_output,running

    def create_scheduler(self):
        cwd = pathlib.Path(__file__).parent.resolve()
        zwi = os.path.dirname(cwd)

        service = os.path.join(zwi,"liewa.service")
        timer = os.path.join(zwi,"liewa.timer")

        cwd = pathlib.Path(__file__).parent.resolve()
        zwi = os.path.dirname(cwd)
        zwi = os.path.dirname(zwi)
        cli_dir = os.path.join(zwi,"cli.py")

        with open(service, "w") as f:
            f.write(f"""[Unit]
Description=Liewa Service
[Service]
Type=simple
ExecStart={os.popen('which python3').read().strip()} {cli_dir}
[Install]
WantedBy=graphical.target""")
        with open(timer, "w") as f:
            f.write("""[Unit]
Description=Liewa Timer
[Timer]
OnCalendar=*-*-* *:00:00
OnCalendar=*-*-* *:30:00
OnCalendar=*-*-* *:*:00
[Install]
WantedBy=timers.target""")

        os.system(f"cp {service} ~/.config/systemd/user/")
        os.system(f"cp {timer} ~/.config/systemd/user/")

        os.system(f"systemctl --user enable {self.timer_name}")
        self.reload_scheduler()
        os.system(f"systemctl --user start {self.timer_name}")
        subprocess.Popen(f"systemctl --user status {self.timer_name}".split())

        # os.system(f"rm {self.service_name}") #achtubg!!!
        # os.system(f"rm {self.timer_name}")

    def delete_scheduler(self):
        for unit_file in [self.timer_name,self.service_name]:
            os.system(f"systemctl --user stop {unit_file}")
            os.system(f"systemctl --user disable {unit_file}")
            os.system(f"rm ~/.config/systemd/user/{unit_file}")
        self.reload_scheduler()

    def reload_scheduler(self):
        os.system("systemctl --user daemon-reload")


class Launchd:
    def __init__(self):
        cwd = pathlib.Path(__file__).parent.resolve()
        zwi = os.path.dirname(cwd)
        zwi = os.path.dirname(zwi)
        self.plist_path = os.path.join(zwi,"com.liewa.daemon.plist")
        if not os.path.exists(os.path.join(zwi,'stderr.log')) : open(os.path.join(zwi,'stderr.log'), 'a').close()
        if not os.path.exists(os.path.join(zwi,'stdout.log')) : open(os.path.join(zwi,'stdout.log'), 'a').close()
        self.update()
    
    def update(self):
        cwd = pathlib.Path(__file__).parent.resolve()
        zwi = os.path.dirname(cwd)
        zwi = os.path.dirname(zwi)
        out = os.path.join(zwi,"stdout.log")
        with open(out,"r+") as f:
            out_lines = f.readlines()
        print(" ".join(out_lines))
        with open(out,"w") as f:
            f.seek(0)
            f.truncate()
        out = os.path.join(zwi,"stderr.log")
        with open(out,"r+") as f:
            err_lines = f.readlines()
        print(" ".join(err_lines))
        with open(out,"w") as f:
            f.seek(0)
            f.truncate()
        
        if len(" ".join(err_lines)) >= 5:
            return "Error occurred!\n\n"+" ".join(err_lines) + "\n\nError occurred!", True
        
        if len(" ".join(out_lines)) >= 5:
            return "Success!\n\n"+" ".join(out_lines) + "\n\nSuccess!", True
        
        return " ".join(err_lines) + " ".join(out_lines), True

    def create_scheduler(self):
        subprocess.run(f"launchctl load {self.plist_path}",shell=True)

    def delete_scheduler(self):
        subprocess.run(f"launchctl unload {self.plist_path}",shell=True)

    def reload_scheduler(self):
        subprocess.run(f"launchctl start {self.plist_path}",shell=True)



class Schtasks:
    def __init__(self):
        #cwd = pathlib.Path(__file__).parent.resolve()
        #zwi = os.path.dirname(cwd)
        #zwi = os.path.dirname(zwi)
        #filename = os.path.join(zwi,'liewaSchtask.xml')
        #ET.register_namespace("", "http://schemas.microsoft.com/windows/2004/02/mit/task")
        #tree = ET.parse(filename)
        #root = tree.getroot()
        #node = root[4][0][0]            #get the Command Node
        #node.text = os.path.join(zwi,"cli.vbs")
        #author = root[0][1]
        #author.text = str(os.environ['COMPUTERNAME'])+"\\"+ str(os.getlogin())
        #tree.write(os.path.join(zwi,'liewaSchtask.xml'))
        self.update()
    
    def update(self):
        cmd = 'schtasks /Query /tn "liewa"'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output,err = proc.communicate()
        running = False
        if re.search("Bereit", output.decode("ISO-8859-1")):
            running = True

        return output.decode("ISO-8859-1"), running

    def create_scheduler(self):
        cwd = pathlib.Path(__file__).parent.resolve()
        zwi = os.path.dirname(cwd)
        zwi = os.path.dirname(zwi)
        cli_dir = os.path.join(zwi,"cli.vbs")
        os.system(f'schtasks /Create /sc minute /mo 30 /tn "liewa" /tr "{cli_dir}" /f')
        #os.system(f'schtasks /create /tn liewa /xml liewaSchtask.xml')

    def delete_scheduler(self):
        os.system('schtasks /Delete /tn "liewa" /f')

    def reload_scheduler(self):
        os.system('schtasks /Run /tn "liewa"')


if __name__ == "__main__":
    taks = Schtasks()