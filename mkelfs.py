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
import xmlrpclib
import getpass
import stat

#list of supported API levels
supportedAPI = ["11.1","12","13","13.0","14","14.0","15","15.0"]

#defining default mirrors
default_centos="http://mirror.centos.org/centos"
default_scientific="http://ftp.scientificlinux.org/linux/scientific"
default_fedora="http://mirrors.kernel.org/fedora"

if __name__ == "__main__":
        #define description, version and load parser
        desc='''%prog is used to create kickstartable distribution trees of EL-like distros like CentOS, Fedora and ScientificLinux. Optionally you can also create kickstart distributions on Spacewalk, Red Hat Satellite and SUSE Manager. Login credentials are assigned using the following shell variables:

        SATELLITE_LOGIN username
        SATELLITE_PASSWORD password

        It is also possible to create an authfile (permissions 0600) for usage with this script. The first line needs to contain the username, the second line should consist of the appropriate password.
        If you're not defining variables or an authfile you will be prompted to enter your login information.

        Checkout the GitHub page for updates: https://github.com/stdevel/mkelfs'''

        parser = OptionParser(description=desc,version="%prog version 0.4")

        #-r / --release
        parser.add_option("-r", "--release", action="store", type="string", dest="release", help="define which release to use (e.g. 6.5)", metavar="RELEASE")

        #-x / --arch
        parser.add_option("-x", "--arch", action="store", type="string", dest="arch", help="define which architecture to use (e.g. x86_64)", metavar="ARCH")

        #-t / --target
        parser.add_option("-t", "--target", action="store", type="string", dest="target", default="/var/satellite/kickstart_tree", help="define where to store kickstart files. A subfolder will be created automatically. (default: /var/satellite/kickstart_tree)", metavar="DIR")
        
        #-m / --mirror
        parser.add_option("-m", "--mirror", dest="mirror", action="store", type="string", help="define a valid EL mirror to use - DON'T add the trailing slash! Have a loot at the EL mirror list (e.g. http://www.centos.org/download/mirrors) for alternatives", metavar="MIRROR")

        #-o / --distribution
        parser.add_option("-o", "--distro", dest="distro", default="centos", action="store", type="string", help="defines for which distro the files are downloaded (default: centos) - other possible values: fedora, scientific", metavar="DISTRO")

        #-f / --force
        parser.add_option("-f", "--force", dest="force", default=False, action="store_true", help="defines whether pre-existing kickstart files shall be overwritten")

        #-i / --ignore-existing
        parser.add_option("-i", "--ignore-existing", dest="ignoreExisting", default=False, action="store_true", help="don't throw errors if downloaded files are already existing (e.g. testing purposes")

        #-q / --quiet
        parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

        #-d / --debug
        parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="enable debugging outputs")

        #-c / --create-distribution
        parser.add_option("-c", "--create-distribution", dest="createDistribution", default=False, action="store_true", help="creates a kickstart distribution on the Spacewalk / Red Hat Satellite or SUSE Manager server")

        #-b / --base-channel
        parser.add_option("-b", "--base-channel", dest="baseChannel", type="string", default="", help="defines the name of the distro base-channel", metavar="CHANNEL")

        #-a / --authfile
        parser.add_option("-a", "--authfile", dest="authfile", metavar="FILE", default="", help="defines an auth file to use instead of shell variables")

        #-s / --server
        parser.add_option("-s", "--server", dest="server", metavar="SERVER", default="localhost", help="defines the server to use")

        #parse arguments
        (options, args) = parser.parse_args()

        #check whether all required options are given
        if options.release is None and options.arch is None:
                parser.error("missing values for release and arch!")
        else:
                #make options being lower-case in case you missed it
                options.distro = options.distro.lower()
                options.release = options.release.lower()
                options.arch = options.arch.lower()

                #setup default mirror URL (if no other defined) depending on selected distro
                if options.mirror == None:
                        if options.distro.lower() == "scientific": options.mirror = default_scientific
                        if options.distro.lower() == "fedora": options.mirror = default_fedora
                        if options.distro.lower() == "centos": options.mirror = default_centos
                if options.distro.lower() == "scientific": url = options.mirror+"/"+options.release+"/"+options.arch+"/os"
                elif options.distro.lower() == "fedora": url = options.mirror+"/releases/"+options.release+"/Fedora/"+options.arch+"/os"
                else: url = options.mirror+"/"+options.release+"/os/"+options.arch

                #print debug output if required
                if options.debug: print("release: " + options.release + "\narch: " + options.arch + "\ntarget: " + options.target + "\nmirror: " + options.mirror + "\nforce: " + `options.force` + "\nverbose: " + `options.verbose` + "\ndebug: " + `options.debug` + "\ndistro: " + options.distro + "\nURL: " + url)

        #define URL and login information
        SATELLITE_URL = "http://"+options.server+"/rpc/api"

        #setup client and key depending on mode
        client = xmlrpclib.Server(SATELLITE_URL, verbose=options.debug)
        if options.authfile:
                #use authfile
                if options.debug: print "DEBUG: using authfile"
                try:
                        #check filemode and read file
                        filemode = oct(stat.S_IMODE(os.lstat(options.authfile).st_mode))
                        if filemode == "0600":
                                if options.debug: print "DEBUG: file permission ("+filemode+") matches 0600"
                                fo = open(options.authfile, "r")
                                s_username=fo.readline()
                                s_password=fo.readline()
                                key = client.auth.login(s_username, s_password)
                        else:
                                if options.verbose: print "ERROR: file permission ("+filemode+") not matching 0600!"
                                exit(1)
                except OSError:
                        print "ERROR: file non-existent or permissions not 0600!"
                        exit(1)
        elif "SATELLITE_LOGIN" in os.environ and "SATELLITE_PASSWORD" in os.environ:
                #shell variables
                if options.debug: print "DEBUG: checking shell variables"
                key = client.auth.login(os.environ["SATELLITE_LOGIN"], os.environ["SATELLITE_PASSWORD"])
        else:
                #prompt user
                if options.debug: print "DEBUG: prompting for login credentials"
                s_username = raw_input("Username: ")
                s_password = getpass.getpass("Password: ")
                key = client.auth.login(s_username, s_password)

        #check whether the API version matches the minimum required
        api_level = client.api.getVersion()
        if not api_level in supportedAPI:
                print "ERROR: your API version ("+api_level+") does not support the required calls. You'll need API version 1.8 (11.1) or higher!"
                exit(1)
        else:
                if options.debug: print "INFO: supported API version ("+api_level+") found."

        #search for base-channel or check base-channel
        listChannels = client.channel.listAllChannels(key)
        if options.debug: print "INFO: all channels" + str(listChannels)
        if options.baseChannel != "":
                #check base-channel
                if options.baseChannel not in str(listChannels):
                        print "ERROR: base-channel '" + options.baseChannel + "' does not exist!"
                        exit(1)
                else:
                        for dict in listChannels:
                                if dict["label"] == options.baseChannel:
                                        if options.arch == "i386":
                                                if dict["arch_name"] != "IA-32":
                                                        print "ERROR: base-channel '" + options.baseChannel + "' has a different architecture!"
                                                        exit(1)
                                        else:
                                                if dict["arch_name"] != options.arch:
                                                        print "ERROR: base-channel '" + options.baseChannel + "' has a different architecture!"
                                                        exit(1)
        else:
                #search base-channel
                for dict in listChannels:
                        #print dict
                        if dict["label"] == options.distro+"-"+options.release+"-"+options.arch:
                                if options.verbose: print "INFO: found matching base channel '" + dict["label"] + "'"
                                options.baseChannel = dict["label"]

        #last check if we configured a base-channel
        if options.baseChannel == "":
                print "ERROR: unable to find a valid base-channel, please check your channels!"
                exit(1)

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
                        elif options.ignoreExisting == False:
                                #abort with error
                                print >> sys.stderr, "ERROR: kickstart tree directory ("+options.target+"/"+options.distro+"-"+options.release+"-"+options.arch+") already exists! Use -f / --force to overwrite!"
                                exit(1)

                #create directory and change directory
                if options.ignoreExisting == False: os.system("mkdir "+options.distro+"-"+options.release+"-"+options.arch)
                os.chdir(options.target+"/"+options.distro+"-"+options.release+"-"+options.arch)

                #download files
                if options.ignoreExisting == False:
                        if options.verbose: print "INFO: about to download kickstart files for EL "+options.release+" "+options.arch+" from mirror "+options.mirror+"..."
                        for i in ["images","isolinux","repodata"]:
                                #setting offset based on mirror and distro
                                if options.distro == "fedora": dir_offset=6
                                elif "vault" in options.mirror: dir_offset=3
                                elif options.distro == "scientific": dir_offset=5
                                else: dir_offset=4
                                if options.debug: print "INFO: dir_offset: "+`dir_offset`
                                #run wget with or without quiet mode
                                cmd = "wget -e robots=off -r -nH --cut-dirs="+`dir_offset`+" --no-parent --reject 'index.html*' "+url+"/"+i+"/"
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
                                        if options.verbose: print "INFO: successfully downloaded kickstart files for EL "+options.release+" "+options.arch+"!\nUse this file path for cobbler or the webui: "+options.target+"/"+options.distro+"-"+options.release+"-"+options.arch

        else:
                print >> sys.stderr, "ERROR: path non-existent or non-writable!"

        #create kickstart distribution
        if options.createDistribution:
                if options.verbose: print "INFO: Creating kickstart distribution..."
                #set install type
                if options.distro == "fedora": installType = "fedora"
                else:
                        if "2.1" in options.release: installType = "rhel_2.1"
                        if "3." in options.release: installType = "rhel_3"
                        if "4." in options.release: installType = "rhel_4"
                        if "5." in options.release: installType = "rhel_5"
                        if "6." in options.release: installType = "rhel_6"
                        if "7." in options.release: installType = "rhel_7"
                if options.debug: print "DEBUG: install type is '" + installType + "'"

                #create distribution
                result = client.kickstart.tree.create(key,"KD-"+options.distro+"-"+options.release+"-"+options.arch,options.target+"/"+options.distro+"-"+options.release+"-"+options.arch,options.baseChannel,installType)
                if result == 1:
                        if options.verbose: print "Successfully created kickstart distribution 'KD-" + options.distro+"-"+options.release+"-"+options.arch + "'"

        #logout and exit
        client.auth.logout(key)
