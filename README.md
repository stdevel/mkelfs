```
mkelfs
======

mkelfs is a tiny python application for creating kickstart trees for EL-like distros (e.g. CentOS, Fedora, ScientificLinux,...).



USAGE
=====

mkelfs.py [options]

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
  -o DISTRO, --distro=DISTRO
                        defines for which distro the files are downloaded
                        (default: centos) - other possible values: fedora, sl
  -f, --force           defines whether pre-existing kickstart files shall be
                        overwritten
  -q, --quiet           don't print status messages to stdout
  -d, --debug           enable debugging outputs



EXAMPLES
========

$ mkelfs.py --release 6.5 --arch x86_64

downloads the latest kickstart files for CentOS 6.5 x86_64 to var/satellite/kickstart_tree.
Mirror http://mirrors.kernel.org/centos is used.


$ mkelfs.py --release 4.1 --arch i386 --target /var/museum/ks --mirror http://vault.centos.org

downloads the antiquated CentOS release 4.1 for i386 from the CentOS Vault mirror site.
Files are stored in /var/museum/ks


$ mkelfs.py -r 6.4 -a x86_64 -m http://www.nic.funet.fi/pub/Linux/INSTALL/scientific -o scientific -fq

downloads the Scientific Linux release 6.4 x86_64 from a Finnish mirror. Pre-existing files are overwritten and no additional output is generated.


$ mkelfs.py -f -r 20 -a i386 -m http://mirror.digitalnova.at/fedora/linux -o fedora

downloads the 32-bit kickstart files for Fedora release 20 from a Austrian mirror.



CREDITS
=======
Zordrak, thanks a lot for providing a bash script which inspired me to do this.
Link to post: http://blog.tpa.me.uk/2013/12/10/creating-a-spacewalk-cobbler-kickstart-tree-for-centos/



FEEDBACK
=======
Feedback is always welcome - this is my first python script so feel free to help me optimizing it! :-)
```
