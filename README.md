```
mkelfs
======

mkelfs is a tiny python application for creating kickstart trees for EL-like distros (e.g. CentOS, Fedora, ScientificLinux,...).



USAGE
=====

mkelks [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -r RELEASE, --release=RELEASE
                        define which release to use (e.g. 6.5)
  -a ARCH, --arch=ARCH  define which architecture to use (e.g. x86_64)
  -t DIR, --target=DIR  define where to store kickstart files. A subfolder
                        will be created automatically. (default:
                        /var/satellite/kickstart_tree)
  -m MIRROR, --mirror=MIRROR
                        define a valid EL mirror to use (default: CentOS -
                        http://mirrors.kernel.org/centos) - DON'T add the
                        trailing slash! Have a loot at the EL mirror list
                        (e.g. http://www.centos.org/download/mirrors) for
                        alternatives
  -f, --force           defines whether pre-existing kickstart files shall be
                        overwritten
  -q, --quiet           don't print status messages to stdout
  -d, --debug           enable debugging outputs



EXAMPLES
========

mkelks --release 6.5 --arch x86_64

downloads the latest kickstart files for CentOS 6.5 x86_64 to var/satellite/kickstart_tree.
Mirror http://mirrors.kernel.org/centos is used.


mkelks --release 4.1 --arch i386 --target /var/museum/ks --mirror http://vault.centos.org

downloads the antiquated CentOS release 4.1 for i386 from the CentOS Vault mirror site.
Files are stored in /var/museum/ks



CREDITS
=======
Zordrak, thanks a lot for providing a bash script which inspired me to do this.
Link to post: http://blog.tpa.me.uk/2013/12/10/creating-a-spacewalk-cobbler-kickstart-tree-for-centos/



FEEDBACK
=======
Feedback is always welcome - this is my first python script so feel free to help me optimizing it! :-)
```
