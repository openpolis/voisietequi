# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.package.name = "squeeze64.box"
  config.vm.box = "squeeze64"
  config.vm.box_url = "http://dl.dropbox.com/u/937870/VMs/squeeze64.box"

  # Host-only network required to use NFS shared folders
  config.vm.network :hostonly, "10.10.10.10"

  # Shared folders -----------------------------------------------------------
  hosthome = "#{ENV['HOME']}/"
  config.vm.share_folder("v-root", "/vagrant", ".", :nfs => true)
  config.vm.share_folder("v-hosthome", "/home/vagrant/.hosthome", hosthome)
  config.vm.share_folder "salt_file_root", "/srv", "provisioning/salt/roots/"

  # Provisioning -------------------------------------------------------------

  ## salt minion install and configuration override
  config.vm.provision :shell, :inline => "/vagrant/provisioning/shell/bootstrap-salt-minion.sh"
  config.vm.provision :shell, :inline => "cp /vagrant/provisioning/salt/minion.conf /etc/salt/minion"

  ## initialize the rest of the system
  config.vm.provision :shell, :inline => "su vagrant -c /vagrant/provisioning/shell/init-system.sh"

  ## Use all the defaults:
  config.vm.provision :salt do |salt|
    salt.run_highstate = true

    ## Optional Settings:
    salt.minion_config = "provisioning/salt/minion.conf"
    salt.temp_config_dir = "/tmp/"
    salt.salt_install_type = "stable"
    salt.salt_install_args = ""

  end


end
