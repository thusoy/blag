# -*- mode: ruby -*-

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "ARTACK/debian-jessie"

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    config.vm.box_url = "https://atlas.hashicorp.com/ARTACK/boxes/debian-jessie"

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--usb", "off"]
        vb.customize ["modifyvm", :id, "--usbehci", "off"]
    end

    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    config.vm.synced_folder "salt", "/srv/salt"
    config.vm.synced_folder "pillar", "/srv/pillar"

    config.vm.network "private_network", ip: "10.20.30.50"

    config.vm.provision "shell",
        inline: "apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install python-git libssl1.0.0 -y"

    config.vm.provision :salt do |salt|
        salt.minion_config = "salt/vagrant-minion"
        salt.run_highstate = true
        salt.verbose = true
        salt.log_level = 'info'
    end

end
