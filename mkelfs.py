#!/usr/bin/env python

# mkelfs.py - script for downloading kickstart-relevant
# files for EL-like distros like CentOS, Fedora etc.
#
# 2014 By Christian Stankowic
# <info at stankowic hyphen development dot net>
# https://github.com/stdevel
#

from optparse import OptionParser
import sys
import os
import shutil

if __name__ == "__main__":
        #define description, version and load parser
        desc="%prog is used to create kickstartable distribution trees of EL-like distros like CentOS, Fedora and ScientificLinux"
        parser = OptionParser(description=desc,version="%prog version 0.1")

        #-r / --release
        parser.add_option("-r", "--release", action="store", type="string", dest="release", help="define which release to use (e.g. 6.5)", metavar="RELEASE")
        #-a / --arch
        parser.add_option("-a", "--arch", action="store", type="string", dest="arch", help="define which architecture to use (e.g. x86_64)", metavar="ARCH")
        #-t / --target
        parser.add_option("-t", "--target", action="store", type="string", dest="target", default="/var/satellite/kickstart_tree", help="define where to store kickstart files. A subfolder will be created automatically. (default: /var/satellite/kickstart_tree)", metavar="DIR")
        #-m / --mirror
        parser.add_option("-m", "--mirror", dest="mirror", default="http://mirrors.kernel.org/centos", action="store", type="string", help="define a valid EL mirror to use (default: CentOS - http://mirrors.kernel.org/centos) - DON'T add the trailing slash! Have a loot at the EL mirror list (e.g. http://www.centos.org/download/mirrors) for alternatives", metavar="MIRROR")
        #-o / --distribution
        parser.add_option("-o", "--distro", dest="distro", default="centos", action="store", type="string", help="defines for which distro the files are downloaded (default: centos) - other possible values: fedora, sl", metavar="DISTRO")
        #-f / --force
        parser.add_option("-f", "--force", dest="force", default=False, action="store_true", help="defines whether pre-existing kickstart files shall be overwritten")
        #-q / --quiet
        parser.add_option("-q", "--quiet",
                          action="store_false", dest="verbose", default=True,
                          help="don't print status messages to stdout")
        #-d / --debug
        parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="enable debugging outputs")

        #parse arguments
        (options, args) = parser.parse_args()

        #check whether all required options are given - currently BROKEN :(
        if options.release is None and options.arch is None:
                parser.error("missing values for release and arch!")
        else:
                #print debug output if required
                if options.debug: print("release: " + options.release + "\narch: " + options.arch + "\ntarget: " + options.target + "\nmirror: " + options.mirror + "\nforce: " + `options.force` + "\nverbose: " + `options.verbose` + "\ndebug: " + `options.debug` + "\ndistro: " + options.distro)

                #setup URL depending on selected distro
                if options.distro.lower() == "scientific": url = options.mirror+"/"+options.release+"/"+options.arch+"/os"
                elif options.distro.lower() == "fedora": url = options.mirror+"/releases/"+options.release+"/Fedora/"+options.arch+"/os"
                else: url = options.mirror+"/"+options.release+"/os/"+options.arch
                if options.debug: print("URL: " + url)

                #check whether target is writable
                if os.access(options.target, os.W_OK):
                        if options.verbose: print "INFO: path exists and writable"

                        #switch to directory and create subfolder non-existent
                        os.chdir(options.target)

                        #check whether the directory already exists
                        if os.path.exists(options.distro+"-"+options.release+"-"+options.arch):

                                #delete content of directory if force given
                                if options.force == True:
                                        shutil.rmtree(options.target+"/"+options.distro+"-"+options.release+"-"+options.arch)
                                        if options.verbose: print "INFO: deleted directory ("+options.target+"/"+options.distro+"-"+options.release+"-"+options.arch+") because -f / --force given"
                                else:
                                        #abort with error
                                        print >> sys.stderr, "ERROR: kickstart tree directory ("+options.target+"/"+options.distro+"-"+options.release+"-"+options.arch+") already exists! Use -f / --force to overwrite!"
                                        exit(1)

                        #create directory and change directory
                        os.system("mkdir "+options.distro+"-"+options.release+"-"+options.arch)
                        os.chdir(options.target+"/"+options.distro+"-"+options.release+"-"+options.arch)

                        #download files
                        if options.verbose: print "INFO: about to download kickstart files for EL "+options.release+" "+options.arch+" from mirror "+options.mirror+"..."
                        for i in ["images","isolinux","repodata"]:
                                #run wget with or without quiet mode
                                cmd = "wget -e robots=off -r -nH --cut-dirs=4 --no-parent --reject 'index.html*' "+url+"/"+i+"/"
                                if options.verbose == False:
                                        cmd = cmd+" --quiet"
                                        retcode = os.system(cmd)
                                else:
                                        retcode = os.system(cmd)

                                #print error if wget had a error
                                if retcode != 0:
                                        print >> sys.stderr, "ERROR: some error occurred (see output above!) - hint: check URL ("+options.mirror+"/"+options.release+")"
                                        exit(1)
                                else:
                                        if options.verbose: print "INFO: successfully downloaded kickstart files for EL "+options.release+" "+options.arch+"!"
                else:
                        print >> sys.stderr, "ERROR: path non-existent or non-writable!"
