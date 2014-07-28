mkelfs
======

`mkelfs.py` is a tiny python application for creating kickstart trees for EL-like distros (*e.g. CentOS, Fedora, ScientificLinux,...*).



Video
=====
[![Creating Enterprise Linux kickstart trees with mkelfs](http://img.youtube.com/vi/FLzz2znW2vc/0.jpg)](http://www.youtube.com/watch?v=FLzz2znW2vc)



Usage
=====
```
Usage: mkelfs.py [options]

mkelfs.py is used to create kickstartable distribution trees of EL-like
distros like CentOS, Fedora and ScientificLinux. Optionally you can also
create kickstart distributions on Spacewalk, Red Hat Satellite and SUSE
Manager. Login credentials are assigned using the following shell variables:
SATELLITE_LOGIN username         SATELLITE_PASSWORD password          It is
also possible to create an authfile (permissions 0600) for usage with this
script. The first line needs to contain the username, the second line should
consist of the appropriate password.         If you're not defining variables
or an authfile you will be prompted to enter your login information.
Checkout the GitHub page for updates: https://github.com/stdevel/mkelfs

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -r RELEASE, --release=RELEASE
                        define which release to use (e.g. 6.5)
  -x ARCH, --arch=ARCH  define which architecture to use (e.g. x86_64)
  -t DIR, --target=DIR  define where to store kickstart files. A subfolder
                        will be created automatically. (default:
                        /var/satellite/kickstart_tree)
  -m MIRROR, --mirror=MIRROR
                        define a valid EL mirror to use - DON'T add the
                        trailing slash! Have a loot at the EL mirror list
                        (e.g. http://www.centos.org/download/mirrors) for
                        alternatives
  -o DISTRO, --distro=DISTRO
                        defines for which distro the files are downloaded
                        (default: centos) - other possible values: fedora,
                        scientific
  -f, --force           defines whether pre-existing kickstart files shall be
                        overwritten
  -i, --ignore-existing
                        don't throw errors if downloaded files are already
                        existing (e.g. testing purposes
  -q, --quiet           don't print status messages to stdout
  -d, --debug           enable debugging outputs
  -c, --create-distribution
                        creates a kickstart distribution on the Spacewalk /
                        Red Hat Satellite or SUSE Manager server
  -b CHANNEL, --base-channel=CHANNEL
                        defines the name of the distro base-channel
  -a FILE, --authfile=FILE
                        defines an auth file to use instead of shell variables
  -s SERVER, --server=SERVER
                        defines the server to use
```



Examples
========
```
$ mkelfs.py --release 6.5 --arch x86_64 -c
```
downloads the latest kickstart files for CentOS 6.5 x86_64 to `/var/satellite/kickstart_tree`.
The default mirror. A kickstart distribution is created afterwards (*interactive login*).

```
$ mkelfs.py --release 4.1 --arch i386 --target /var/museum/ks --mirror http://vault.centos.org
```
downloads the antiquated CentOS release 4.1 for i386 from the CentOS Vault mirror site.
Files are stored in `/var/museum/ks`

```
$ mkelfs.py -r 6.4 -a x86_64 -o scientific -fq
```
downloads the Scientific Linux release 6.4 x86_64 from the default mirror. Pre-existing files are overwritten and no additional output is generated.

```
$ mkelfs.py -f -r 20 -a i386 -m http://mirror.digitalnova.at/fedora/linux -o fedora
```
downloads the 32-bit kickstart files for Fedora release 20 from a Austrian mirror.



Credits
=======
Zordrak, thanks a lot for providing a bash script which inspired me to do this.
Link to post: http://blog.tpa.me.uk/2013/12/10/creating-a-spacewalk-cobbler-kickstart-tree-for-centos/



Feedback
========
Feedback is always welcome - this is my first python script so feel free to help me optimizing it! :-)
