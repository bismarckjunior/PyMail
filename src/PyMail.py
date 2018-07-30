#-*-coding: utf-8-*-
# Author: Bismarck Gomes Souza Junior <bismarckgomes@gmail.com>
# Class for sending bulk e-mails
import os, re, sys, cgi, webbrowser
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from csv import read_csv, read_ini
from bar import ProgressBar


class PyMail:

    smtp_ = { 'gmail':   {'port': 587, 'host':"smtp.gmail.com"},
              'outlook': {'port': 587, 'host':"smtp-mail.outlook.com"}}
    extensions_ = {'images': ['jpg', 'jpeg', 'png'],
                   'docs':   ['txt', 'doc', 'docx', 'pdf', 'xls', 'xlsx', 
                              'csv', 'ptt', 'pttx', 'html', 'md']}

    def __init__(self, user, username=None, password=None, type_msg="plain"):
        self.user_ = user
        self.password_ = password
        self.username_ = user if (username is None) else username
        self.type_msg_ = type_msg
        self.server_ = None
        self.emails_ = []
        self.path_emails_ = './html'
        self.path_ = './'

    def __del__(self):
        if (self.server_ is not None):
            self.__disconnect()

    def __connect(self):
        ini = self.user_.find('@')
        domain = self.user_[ini+1:self.user_.find('.', ini)]

        # Check domain
        if (domain not in self.smtp_):
            raise Exception(37, "Invalid domain (%s)" % domain)

        # Get smtp
        smtp = self.smtp_[domain]

        # Initialize server
        self.server_ = SMTP(smtp["host"], smtp["port"])
        self.server_.ehlo()
        self.server_.starttls()
        self.server_.ehlo()
        self.server_.login(self.user_, self.get_password())

    def __disconnect(self):
        self.server_.close()

    def __send_email(self, to, msg, subject=None, cc="", bcc="", attachs=[]):
        msg, subject = self.get_msg_and_subject(msg, subject)

        email = MIMEMultipart()
        email['From'] = self.username_
        email['To'] = to
        email['Subject'] = subject
        email.attach(MIMEText(msg, self.type_msg_))

        if cc: email['Cc'] = cc
        if bcc: email['Bcc'] = bcc

        for filename in attachs:
            if filename:
                self.attach_to_email(email, filename)

        self.submmit_email(email)

    def __send_mass_email(self):

        # Creating progress bar
        nEmails = len(self.emails_)
        bar = ProgressBar(nEmails, name=' Sending...       ', width=30, perc=False)

        # Send e-mail
        for i, email in enumerate(self.emails_):
            self.submmit_email(email)

            # Update progress bar
            bar.update(i+1)

        print

    def run(self, status, cmd, *args, **kwargs):
        print " {0:<16s}".format(status),
        
        try:
            cmd(*args, **kwargs)

        except Exception as e:
            n = e.args[0]
            msg = e.args[1]
            if (len(msg) > 40):
                msg = msg[:40] + '...'
            print "[ERROR %d]: %s" % (n, msg)
            return False

        else:
            print "[OK]"

        return True

    def disconnect(self):
        
        self.run("Disconnecting...", self.__disconnect)

    def connect(self):
        print "\n Accessing...     [%s]" % self.user_
        return self.run("Connecting...", self.__connect)

    def attach_to_email(self, email, filename):
        ext = filename[filename.rfind('.')+1:]
        basename = os.path.basename(filename)
        full_path = os.path.join(self.path_, filename)

        # Check attachment
        if (os.path.exists(full_path)):
            data = open(full_path, 'rb').read()
        else:
            raise Exception(80, "No attachment found (%s)" % basename)

        # Attachs
        if (ext in self.extensions_['images']):
            email.attach(MIMEImage(data, name=basename))

        elif (ext in self.extensions_['docs']):
            att = MIMEApplication(data)
            att.add_header('Content-Disposition', 'attachment', filename=basename)
            email.attach(att)

        else:
            raise Exception(85, "Invalid attachment file (%s)" % basename)

        if (not hasattr(email, 'attachs_path_')):
            email.attachs_path_ = {}

        path = os.path.join(os.path.dirname(full_path), "..")
        path = os.path.join(path, basename)
        email.attachs_path_[basename] = path

    def send_email(self, to, msg, subject=None, cc="", bcc="", attachs=[]):
        
        cmd = lambda: self.__send_email(to, msg, subject, cc, bcc, attachs)

        self.run("Sending...", cmd)

    def send_mass_email(self, msg, csv_file, subject=None,
        key_to="E-mail", key_cc="Cc", key_bcc="Bcc",
        key_subject="Subject", key_attach="Attachments"):

        msg, subject = self.get_msg_and_subject(msg, subject)
        csv = read_csv(os.path.join(self.path_, csv_file))

        # try:
        if (True):
            # Check recipient
            if (key_to not in csv):
                raise Exception(116, "Column \"%s\" with e-mails not found" % key_to)

            # Check subject
            if (subject is None and key_subject not in csv):
                raise Exception(119, "Subject not defined")

            # Create e-mails
            if (self.emails_ == []):
                self.create_emails(msg, csv, subject, key_to, key_cc, key_bcc,
                                   key_subject, key_attach)

            # Check e-mails
            webbrowser.open(os.path.join(self.path_emails_, 'email_001.html'))

            # Continue?
            if ( raw_input('\nDo you want to send created e-mails? [y/N] ') != 'y' ):
                print '\nAborted!'
                return

            # Connect to server
            if (not self.connect()):
                return
            
            # Send mass email
            self.__send_mass_email()

            # Disconnect
            self.disconnect()

        # except Exception as e:
        #     print "[ERROR %d]: %s" % e.args

    def create_emails(self, msg, csv, subject=None,
        key_to="E-mail", key_cc="Cc", key_bcc="Bcc",
        key_subject="Subject", key_attach="Attachments"):
        
        self.emails_ = []

        # Check subject
        if (subject is None):
            f_sub = lambda i: csv[key_subject][i]
        else:
            f_sub = lambda i: subject

        # Creating progress bar
        nEmails = len(csv.values()[0])

        # Creating e-mails
        for i in range(nEmails):
            to = csv[key_to][i]

            email = MIMEMultipart()
            email['From'] = self.username_
            email['To'] = to

            # Subject
            sub = f_sub(i)
            sub_keys = re.findall(r"\{\{(.+?)\}\}", sub)
            sub_fmt = re.sub(r"\{\{(.+?)\}\}", "%s", sub)
            email['Subject'] = sub_fmt % tuple([csv[key][i] for key in sub_keys])

            # Cc: carbon copy
            if (key_cc in csv):
                email['Cc'] = csv[key_cc][i]

            # Bcc: Blind carbon copy
            if (key_bcc in csv):
                email['Bcc'] = csv[key_bcc][i]

            # Attachements
            if (key_attach in csv):
                for filename in csv[key_attach][i].split(';'):
                    if filename:
                        self.attach_to_email(email, filename)

            # Body
            msg_keys = re.findall(r"\{\{(.+?)\}\}", msg)
            msg_fmt = re.sub(r"\{\{(.+?)\}\}", "%s", msg)
            body = msg_fmt % tuple([csv[key][i] for key in msg_keys])
            email.attach(MIMEText(body, self.type_msg_))

            # Create html
            self.create_email_html(i+1, nEmails, email)

            # Append e-mail
            self.emails_.append(email)

    def submmit_email(self, email):
        if (self.server_ is None):
            self.show_email_cmd(email)
        else:
            self.server_.sendmail(self.username_, email['To'], email.as_string())

    def get_data_from_email(self, email):
        data = { 'Subject': email['Subject'],
                 'To':      email['To'],
                 'Cc':      email['Cc'] if email['Cc'] else '',
                 'Bcc':     email['Bcc'] if email['Bcc'] else ''}

        if (self.user_ == self.username_):
            data['From'] = email['From'] 
        else:
            data['From'] = "%s <%s>" % (self.username_, self.user_)

        data['msg'] = ''
        data['attachments'] = []

        # Break email contents in pieces
        pieces = []
        for piece in ('\n'+email.as_string()).split("--=========="):
            d = {}
            lines = piece.split('\n')[1:-1]
            for i, line in enumerate(lines):
                if (':' in line):
                    k,v = line.split(':')
                    d[k] = v
                else:
                    d['data'] = '\n'.join(lines[i+1:])
                    break
            if d:
                pieces.append(d)
        
        # Join pieces
        for piece in pieces:
            ctype = piece['Content-Type']

            if ('text/' in ctype):
                data['msg'] += piece['data']

            if ('image/' in  ctype):
                attach = ctype[ctype.find("e=")+3:-1]
                data['attachments'].append(attach)

            if ('application/' in ctype):
                dispos = piece['Content-Disposition']
                attach = dispos[dispos.find("e=")+3:-1]
                data['attachments'].append(attach)

        return data

    def get_password(self):
        if (self.password_ is not None):
            return self.password_

        try:
            import Tkinter, tkSimpleDialog
            root = Tkinter.Tk() 
            root.withdraw() 
            pwd = tkSimpleDialog.askstring("Password", 
                                           "E-mail: %s\n\nEnter password:" % self.user_, 
                                           show='*', parent=root)
            root.destroy()
        except:
            from getpass import getpass
            pwd = getpass()

        return pwd

    def get_msg_and_subject(self, msg, subject):

        if (os.path.exists(msg)):
            if (msg.endswith('.html')):
                self.type_msg_ = "html"

            self.path_ = os.path.dirname(msg)
            self.path_emails_ = os.path.join(self.path_, 'html')
            with open(msg, 'r') as f:
                lines = f.readlines()

                pos = lines[0].find('Subject:')
                if (pos>=0):
                    if (subject is None): 
                        subject = lines[0][pos+8:].strip()

                    msg = "".join(lines[1:]).strip()
                else:
                    msg = "".join(lines).strip()

        return msg, subject

    def show_email_cmd(self, email):
        data = self.get_data_from_email(email)

        print
        print '='*80
        print "{:12s} {:s}".format('From:', data['From'])
        print "{:12s} {:s}".format('To:', data['To'])
        print "{:12s} {:s}".format('Subject:', data['Subject'])
        if data['Cc']: print "{:12s} {:s}".format('Cc:', data['Cc'])
        if data['Bcc']: print "{:12s} {:s}".format('Bcc:', data['Bcc'])
        
        if (data['attachments']):
            print "{:12s} {:s}".format('Attachments:', str(data['attachments']))

        print "\n---\n\n%s\n" % data['msg']
        print '='*80

        # print '*'*80
        # print email.as_string()
        # print '*'*80
        print

    def create_email_html(self, e_id, nEmails, email):
        data = self.get_data_from_email(email)
        path = self.path_emails_

        with open('html.dll', 'r') as f:
            html = f.read()

        filename = os.path.join(path, 'email_%03d.html' % e_id)

        if (os.path.exists(path)):
            if (e_id == 1):
                for fname in os.listdir(path):
                    os.remove(os.path.join(path, fname))
        else:
            os.makedirs(path)

        with open(filename, 'w') as f:
            
            page_1 = 'email_%03d.html' % 1
            page_n = 'email_%03d.html' % nEmails
            sts_1 = sts_n = ''

            if (e_id == 1):
                page_b = page_1 = ''
                sts_b = sts_1 = 'disabled'
            else:
                page_b = 'email_%03d.html' % (e_id-1)
                sts_b = ''

            if (e_id == nEmails):
                page_a = page_n = ''
                sts_a = sts_n = 'disabled'
            else:
                page_a = 'email_%03d.html' % (e_id+1)
                sts_a = ''

            main = 'index.hml'

            attachments = [] 

            for att in data['attachments']:
                attachments.append('<a href="%s">%s</a>' % (email.attachs_path_[att], att))
            
            subject = cgi.escape(data['Subject'])
            from_ = cgi.escape( data['From'] )
            to = cgi.escape(data['To'])
            cc = cgi.escape(data['Cc'])
            bcc = cgi.escape(data['Bcc'])
            attachs = "; ".join(attachments)
            msg = data['msg']

            if (self.type_msg_ == "plain"):
                msg = cgi.escape(msg).replace("\n", "<br>")

            h = html.format(e_id, nEmails, page_1, sts_1, page_b, sts_b, main, 
                            page_a, sts_a, page_n, sts_n, 
                            unicode(subject,'utf-8').encode('ascii', 'xmlcharrefreplace'),
                            from_, to, cc, bcc, attachs, 
                            unicode(msg,'utf-8').encode('ascii', 'xmlcharrefreplace'))
            f.write(h)


if __name__ == '__main__':
    
    print '='*50
    print '         PyMail 0.1 <www.goo.gl/TDpSQC>'
    print '='*50
    try:
        if len(sys.argv) > 1:
            ini_file = sys.argv[1]

        else:
            print 
            print 'Arraste uma arquivo ".ini" para o este script.'
            print 'Exemplo:'
            print '  [Settings]'
            print '  user     = "email@gmail.com"'
            print '  username = "Seu Nome"'
            print '  msg_file = "Email.txt"'
            print '  csv_file = "Email.csv"\n'

            eg_file = "../example/Emails.ini"
            run = raw_input('Run exemple "%s"? [y/N] ' % eg_file)
            
            ini_file = None if (run != 'y') else eg_file

        if (ini_file):
            ini = read_ini(ini_file)
            d = ini['Settings']
            pwd = d['password'] if 'password' in d else None
            path = os.path.dirname(ini_file)
            mail = PyMail(d['user'], d['username'], pwd)
            msg_file = os.path.join(path, d['msg_file'])
            csv_file = os.path.join(path, d['csv_file'])
            mail.send_mass_email(msg_file, csv_file)

    except:
        print sys.exc_info()[0]
        import traceback
        print traceback.format_exc()

    finally:
        print '='*50
        raw_input('\nPress enter to close...')
        