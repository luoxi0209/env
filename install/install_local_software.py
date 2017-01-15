import commands
import os
import sys
import traceback

app_list = [
            {'name': 'jdk1.8',
             'select': False, # src_url has download protect
             'deploy_dir': 'env/lang/jdk1.8',
             'src_url': 'http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.tar.gz',
             'decompress_cmd': 'tar -xzvf',
             'extract_path': ''
            },
            {'name': 'maven3',
             'select': True,
             'deploy_dir': 'tools/maven3',
             'src_url': 'http://mirror.bit.edu.cn/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz',
             'decompress_cmd': 'tar -xzvf',
             'extract_path': ''
            },
            {'name': 'sublime_text_3',
             'select': True,
             'deploy_dir': 'ide/SublimeText/sublime_text_3',
             'src_url': 'https://download.sublimetext.com/sublime_text_3_build_3126_x64.tar.bz2',
             'decompress_cmd': 'tar -xvf',
             'extract_path': ''
            },
            {'name': 'idea',
             'select': True,
             'deploy_dir': 'ide/idea',
             'src_url': 'https://download.jetbrains.8686c.com/idea/ideaIC-2016.3.2-no-jdk.tar.gz',
             'decompress_cmd': 'tar -xvf',
             'extract_path': ''
            },
           ]
           
def log_info(msg):
    """ log info
    """
    print ('\033[94m%s\033[0m' % msg)

def log_warning(msg):
    """ log warning
    """
    print ('\033[93m%s\033[0m' % msg)
    
def log_success(msg):
    """ log success
    """
    print ('\033[92m%s\033[0m' % msg)

def log_error(msg):
    """ log error
    """
    print ('\033[91m%s\033[0m' % msg)

def run_cmd(cmd):
    """ run cmd
    """
    log_info(cmd)
    return commands.getstatusoutput(cmd)

class Installer(object):
    """ Installer
    """
    def __init__(self, root_dir):
        """ init
        """
        self.downloader = "wget"
        self.tmp_dir = "%s/run/tmp/software_down" % root_dir
        self.tmp_file = "%s/A" % self.tmp_dir

    def run(self, name, select, deploy_dir, src_url, decompress_cmd, extract_path):
        """ run
        """
        try:
            if not select:
                log_warning('%s is not select, so skip' % name)
                return
            # dest exist check
            if os.path.exists(deploy_dir):
                log_warning('dest dir %s is exist, so install %s skip' % (deploy_dir, name))
                return
            log_info('start to install %s' % name)

            # clean tmpdir
            cmd='rm -rf %s && mkdir -p %s' % (self.tmp_dir, self.tmp_dir)
            ret, ret_str = run_cmd(cmd)
            cmd='ls %s' % (self.tmp_dir)
            ret, ret_str = run_cmd(cmd)
            if ret:
                log_error('clean tmpdir %s failed' % (self.tmp_dir))
                return

            # download software
            cmd='%s "%s" -O %s' % (self.downloader, src_url, self.tmp_file)
            ret, ret_str = run_cmd(cmd)
            if ret:
                log_error('download %s failed:%s' % (name, ret_str))
                return

            # decompress software
            cmd='cd %s && %s %s' % (self.tmp_dir, decompress_cmd, os.path.basename(self.tmp_file))
            ret, ret_str = run_cmd(cmd)
            if ret:
                log_error('decompress %s failed:%s' % (name, ret_str))
                return
            cmd='rm %s' % (self.tmp_file)
            ret, ret_str = run_cmd(cmd)
            if ret:
                log_error('clean download file %s failed:%s' % (self.tmp_file, ret_str))
                return

            # move to dest
            filelist = os.listdir(self.tmp_dir)
            if extract_path == '':
                if len(filelist) == 1:
                    src = '%s/%s' % (self.tmp_dir, filelist[0])
                else:
                    src = self.tmp_dir
                cmd = 'mv %s %s' % (src, deploy_dir)
                ret, ret_str = run_cmd(cmd)
                if ret:
                    log_error('move to dest failed:%s' % (ret_str))
                    return
            else:
                cmd = 'mv %s/%s %s' % (self.tmp_dir, extract_path, deploy_dir)
                ret, ret_str = run_cmd(cmd)
                if ret:
                    log_error('move to dest failed:%s' % (ret_str))
                    return

            log_success('install %s from %s to %s successfully' % (name, src_url, deploy_dir))
        except:
            log_error('install %s failed:%s' % (name, traceback.format_exc()))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python %s root_dir' % sys.argv[0]
        exit(1)
    installer = Installer(sys.argv[1])
    for item in app_list:
        installer.run(**item)
