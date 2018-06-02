#!/cad/tools/Python-3.5.2/bin/python3
import os
import socket
import sys,re
os.chdir(sys.path[0])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vrg_site.settings")
import django
django.setup()

from configparser import ConfigParser
from socketserver import BaseRequestHandler,ThreadingTCPServer
from regression.models import VectorIssue,Category,DailyReport
from django.contrib.auth.models import User
from queue import Queue
import logger
from django.core.mail import EmailMessage
import socket
from django.urls import reverse
import re



def mail_create(vector):
    vector_path = socket.gethostname() + ":15900" + reverse('regression:vector',args=(vector.id,))
    subject = "[vector %d] %s" % (vector.id,vector.vector)
    message = """
        <html>
        <head>hi {name} ! You have got a new bug{id}</head>
        <body>
            <table border="1" cellspacing="0" cellpadding="8">
            <tr><td><TH align=right>category:</td><td>{category}</td></tr>
            <tr><td><TH align=right>content:</td><td>{content}</td></tr>
            </table>
            <p>Please login VRG web for more details</p>
        </body>
        </html>
    """.format(id=vector.id,name=vector.bugowner,content=vector.content,category=vector.category)
    tos = list(set([vector.bugowner.email,'marshallliu@zhaoxin.com']))
    msg = EmailMessage(subject,message,'marshallliu@zhaoxin.com',tos)
    msg.content_subtype='html'
    msg.send()



def saveCategory(type):
    admin = User.objects.get(username='felixm-h')
    l2_sva_fail = re.compile("l2-sva-fail")
    if l2_sva_fail.search(type) is not None:
        type = 'l2-sva-fail'
    if Category.objects.filter(title=type) :
        category = Category.objects.filter(title=type)[0]
    else:
        category = Category(title=type,owner=admin)
    category.save(flag=True)
    return category

def add_fail(cfg):
    status = cfg.get('vector','status')
    if status != 'FAIL':
        return None
    name = cfg.get('vector','name')
    content = cfg.get('fail','info')
    issue = VectorIssue(vector=name,content=content)

    issue.project = cfg.get('vector','project')

    issue.src_path  = cfg.get('path','vector')
    issue.wave_path = cfg.get('path','waveform')
    issue.log_path  = cfg.get('path','log')
    issue.set_top = False

    issue.design_git      = cfg.get('git','design_version')
    issue.env_git         = cfg.get('git','env_version')
    issue.design_git_date = cfg.get('git','design_date')
    issue.env_git_date    = cfg.get('git','env_date')

    type = cfg.get('fail','type')
    issue.category = saveCategory(type)
    owner = issue.category.owner
    issue.bugowner = owner

    issue.save()
    mail_create(issue)
    return issue


def add_report(cfg,cfg_file):
    report = DailyReport.objects.last()
    if report is None:
        report = DailyReport()
    elif not report.is_same_work_day():
        report = DailyReport()

    status = cfg.get('vector','status')
    project = cfg.get('vector','project')
    name = cfg.get('vector','name')
    if status == 'FAIL':
        report.add_fail()
        if re.search('CHX002_A0', project): report.add_fail_prj1()
        #if(project == 'CHX002_A0'): report.add_fail_prj1()
        #if(project == 'CHX002_A0_PVRG'): report.add_fail_prj1()
    else:
        #if(cfg.getint('transactions','total_request')==0):
        if cfg.getint('transactions','total_request')==0 and not re.search('top', name):
            raise Exception("pass vector total request cannot be 0 : %s" % cfg_file)
        #report.add_pass()
        if re.search('CHX002_A0', project): report.add_pass_prj1()
        #if(project == 'CHX002_A0'): report.add_pass_prj1()
        #if(project == 'CHX002_A0_PVRG'): report.add_pass_prj1()


    items = [
            'total_request',
            'c2m',
            'c2p',
            'p2c',
            'c2p_io',
            'c2p_mem',
            'c2p_special',
            'jtag',
            'hotwire',
            'cl0_l2_hit',
            'cl0_l2_miss',
            'cl1_l2_hit',
            'cl1_l2_miss',
            'cl0_msr_read',
            'cl0_msr_write',
            'cl1_msr_read',
            'cl1_msr_write',
            'fsbc_request',
            'fsbc_trigger',
            'interrupt_ipi',
            'interrupt_msi',
            'interrupt_sb',
            'c2m_s1',
            'c2p_s1',
            'p2c_s1',
            'c2p_io_s1',
            'c2p_mem_s1',
            'c2p_special_s1',
            'interrupt_ipi_s1',
            'interrupt_msi_s1',
            'interrupt_sb_s1',
            'cl0_l2_hit_s1',
            'cl0_l2_miss_s1',
            'cl1_l2_hit_s1',
            'cl1_l2_miss_s1',
            'cl0_msr_read_s1',
            'cl0_msr_write_s1',
            'cl1_msr_read_s1',
            'cl1_msr_write_s1',
            'fsbc_request_s1',
            'fsbc_trigger_s1',
            'hotwire_s1',
            'vpi_s0_s1',
            'vpi_s1_s0',
            ]
    for item in items:
        sum = getattr(report,item) + cfg.getint('transactions',item)
        setattr(report,item,sum)

    report.save()
    return report

def cfg_info(cfg_file):
    print("add info : %s" % cfg_file)
    cfg = ConfigParser()
    cfg.read(cfg_file)

    fail = add_fail(cfg)
    report = add_report(cfg,cfg_file)
    output = []
    if fail is not None:
        output.append(str(fail))
    output.append(str(report))
    return "\n".join(output)

class InfoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while(True):
            msg = self.request.recv(8192)
            if not msg:
                break
            cfg_file = str(msg,encoding='utf8')
            if not os.path.exists(cfg_file):
                error = "db-add-fail: No such INI File: %s" % cfg_file
                logger.log_info(error)
                self.request.send(bytes(error,encoding="utf8"))
                print(error)
                continue
            try:
                output = bytes(cfg_info(cfg_file),encoding="utf8")
                self.request.send(output)
                logger.log_info("success add %s" % cfg_file)
            except Exception as e:    
                error = "db-add-fail: " + str(e)
                print(error)
                logger.log_info(error)
                logger.log_debug(cfg_file)
                self.request.send(bytes(error,encoding="utf8"))
        

if __name__=='__main__':
    serv = ThreadingTCPServer(('',17400),InfoHandler)
    serv.serve_forever()

