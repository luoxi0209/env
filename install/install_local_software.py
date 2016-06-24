import commands
import os
import sys
import traceback

app_list = [
            ('jdk1.8',
             'env/lang/jdk1.8',
             'http://download.oracle.com/otn-pub/java/jdk/8u91-b14/jdk-8u91-linux-x64.tar.gz',
             'tar -xzvf',
             ''),
            ('maven3',
             'tools/maven3',
             'http://mirror.bit.edu.cn/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz',
             'tar -xzvf',
             ''),
           ]

class Installer(object):
    """ Installer
    """
    def __init__(self, root_dir):
        """ init
        """
        self.downloader="wget"
        self.tmp_dir="%s/run/tmp/software_down" % root_dir
        self.tmp_file="%s/A" % self.tmp_dir
        self.info_log_template = '\033[94m%s\033[0m'
        self.warning_log_template = '\033[93m%s\033[0m'
        self.success_log_template = '\033[92m%s\033[0m'
        self.error_log_template = '\033[91m%s\033[0m'

    def run(self, name, dest_dir, src_url, decompress_cmd, extract_path=''):
        """ run
        """
        try:
            # dest exist check
            if os.path.exists(dest_dir):
                print self.warning_log_template % (
                    'dest dir %s is exist, so install %s skip' % (dest_dir, name))
                return
            print self.info_log_template % ('start to install %s' % name)

            # clean tmpdir
            cmd='rm -rf %s && mkdir %s' % (self.tmp_dir, self.tmp_dir)
            print self.info_log_template % (cmd)
            ret, ret_str = commands.getstatusoutput(cmd)
            cmd='ls %s' % (self.tmp_dir)
            print self.info_log_template % (cmd)
            ret, ret_str = commands.getstatusoutput(cmd)
            if ret:
                print self.error_log_template % (
                    'clean tmpdir %s failed' % (self.tmp_dir))
                return

            # download software
            cmd='%s "%s" -O %s' % (self.downloader, src_url, self.tmp_file)
            print self.info_log_template % (cmd)
            ret, ret_str = commands.getstatusoutput(cmd)
            if ret:
                print self.error_log_template % ('download %s failed:%s' % (name, ret_str))
                return

            # decompress software
            cmd='cd %s && %s %s' % (self.tmp_dir, decompress_cmd, self.tmp_file)
            print self.info_log_template % (cmd)
            ret, ret_str = commands.getstatusoutput(cmd)
            if ret:
                print self.error_log_template % ('decompress %s failed:%s' % (name, ret_str))
                return
            cmd='rm %s' % (self.tmp_file)
            print self.info_log_template % (cmd)
            ret, ret_str = commands.getstatusoutput(cmd)
            if ret:
                print self.error_log_template % (
                    'clean download file %s failed:%s' % (self.tmp_file, ret_str))
                return

            # move to dest
            filelist = os.listdir(self.tmp_dir)
            if extract_path == '':
                if len(filelist) == 1:
                    src = '%s/%s' % (self.tmp_dir, filelist[0])
                else:
                    src = self.tmp_dir
                cmd = 'mv %s %s' % (src, dest_dir)
                print self.info_log_template % (cmd)
                ret, ret_str = commands.getstatusoutput(cmd)
                if ret:
                    print self.error_log_template % ('move to dest failed:%s' % (ret_str))
                    return
            else:
                cmd = 'mv %s/%s %s' % (self.tmp_dir, extract_path, dest_dir)
                print self.info_log_template % (cmd)
                ret, ret_str = commands.getstatusoutput(cmd)
                if ret:
                    print self.error_log_template % ('move to dest failed:%s' % (ret_str))
                    return

            print self.success_log_template % (
                'install %s from %s to %s successfully' % (name, src_url, dest_dir))
        except:
            print self.error_log_template % (
                'install %s failed:%s' % (name, traceback.format_exc()))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python %s root_dir' % sys.argv[0]
        exit(1)
    installer = Installer(sys.argv[1])
    for item in app_list:
        installer.run(*item)
