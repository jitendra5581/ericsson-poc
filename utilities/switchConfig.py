# Importing the necessary modules
import difflib
import datetime
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
from netmiko import ConnectHandler
from django.conf import settings
 
#defining the command to send to each device
command = 'show running'
 
class SwitchScanner(object):
    #defined class and the init function contains initialization for information of virtual arista devices fro successful ssh connection
    def __init__(self, device_type, ip_address, username, password, secret):
        self.device_type=device_type
        self.ip=ip_address
        self.username=username
        self.password=password
        self.secret=secret
 
    #defining write function to read configuration information of network devices from yesterday's date and today's date and compare those two files
    def generate_log_file(self):
        #establishing session to connect to device using SSH
        session = ConnectHandler(device_type=self.device_type, ip=self.ip, username=self.username,
                             password=self.password, secret=self.secret)
        #entering the session
        enable = session.enable()
        #sending commmand and storing output
        output = session.send_command(command)
        #defining the file from yesterday, for comparison
        log_file_path = settings.LOGS_URL
        old_configfile = log_file_path + self.ip + '_' + (
            datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        #writing the command to a file for today
        with open('configfiles/' + self.ip + '_' + datetime.date.today().isoformat(), 'w') as new_configfile:
            new_configfile.write(output + '\n')
        #extracting differences between yesterday's and todays file in HTML format
        print("*****************************************")
        with open(old_configfile, 'r') as old_file, open(
            'configfiles/' + self.ip + '_' + datetime.date.today().isoformat(),
            'r') as new_file:
            compare = difflib.HtmlDiff().make_file(fromlines=old_file.readlines(), tolines=new_file.readlines(),
                                               fromdesc=(datetime.date.today() - datetime.timedelta(
                                                   days=1)).isoformat(),
                                               todesc=datetime.date.today().isoformat())
            #sending differences to mail function for forwarding as email
            # read_from_files.mail(compare)
    #defining function for sending comparison report via email
    '''
    def mail(compare):
        fromaddr = 'percipientnms@gmail.com'
        toaddr = 'anupam@echelonedge.com'
        #using mimemultipart to email differences
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Configuration comparision Report'
        msg.attach(MIMEText(compare, 'html'))
        try:
         #server = smtplib.SMTP('smtp.gmail.com', 587)
         print("trying to establish session with gmail")
         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
         print("session established")
         server.ehlo()
         server.login('percipientnms@gmail.com', 'percipient@123')
         print("login successful")
         server.sendmail(fromaddr, toaddr, msg.as_string())
         server.quit()
         print("email sent successfully")
        except Exception as e:
            print(e)
            print('something went wrong...')
    '''
#defining information of each arista virtual switches like device_type,ip,username and password
'''
if __name__ == "__main__":
    Switch1 = read_from_files("cisco_ios", "192.168.250.2", "cisco", "cisco", "cisco")
    #sending information of each virtual device to write function for reading and comparison
    read_from_files.write_fromfile(Switch1)
    #Switch2 = read_from_files("hp_procurve", "192.168.100.254", "cisco", "cisco")
    #read_from_files.write_fromfile(Switch2)
'''    
