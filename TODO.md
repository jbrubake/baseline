# Ansible

## Playbooks

- Make playbooks modular so pieces can be run as needed
- Convert some tasks into task files
- Package install blocks should report failed packages but not fail the playbook
- Source host-specific scripts
- Update Python packages installed with `pip`, `pipx` and `pip-safe`
- Update Python `venvs` when system `python` is updated
- Update Perl modules

### main.yaml

- Install `ubi` with an RPM
- Generate bash completion from Python scripts using `shtab`
- Create swap space to enable hibernation

### personal.yaml

- Remove directories only if empty
- Set `changed_when` for all `command` tasks
- Use `path_join` when generating `desired_xdg`
- Do additional SSH keys need to be generated?
- Installing `mopidy` plugins with `pip` always shows changed, likely due to how
    the `pip` module works
- Run `gcloud init` if `gcloud` is installed
- Configure ansible {stdout,sterr}_callback
- Update mopidy plugins
- Update packages installed from source
- Create a systemd service to delete old Sidebery snapshots
- Update fortune dat files. (Could this instead be done with a local CI/CD pipeline?)
- Generate files from `dotfiles` templates
- Copy `libvirt` images from a local repository

## Roles

- Make any relavant tasks usable by a normal user
- (new) prepare system to build Packer LXC containers
- (new) audio setup
- (new) "gaming" setup that installs steam, wine, winetricks, vassal, etc.

### common

- Where should generated passwords be written by default?
- Generated passwords are being saved on the remote machine. Is that OK?

### google-cloud

- Improve idempotency of `google-cloud-cli` install

### libvirt

- Verify that libvirtd service starts on boot
- Do users need to be in the kvm group as well?

### lisp

- Is it possible to install quicklisp system-wide?

### mail

- Split package list into required and optional

### rust

- Verify that `changed_when` in the `Update rust` task works properly when
    updating multiple rust toolchains

### virtualbox

- Do users need added to the `vboxusers` group?

### x11

- Create a Wayland role ar at least use the Wayland X11 wrapper
- What are the minimum required packages for X?
- Move packages lists out of `tasks` and into `vars/main.yaml`
- Install Microsoft Core Fonts
- Is the Gnome keyring task only needed when using GDM?
- Make the Gnome keyring task optional

## Modules

### ubi

- Validate all return values
- Validate that check mode works correctly
- Support getting the checksum value from a URL
- Include `ubi` error message if a file cannot be downloaded

# Packages

## Failing to Install

Error: `does not verify: no digest`

Name                    | Type  | Description  | URL
----                    | ----  | -----------  | ---
google-earth-pro-stable | third | Google Earth | http://www.google.com/earth

Error: `Failed to import OpenPGP keys into temporary keyring: Compute cert len failed`

Name        | Type  | Description                                                                                 | URL
----        | ----  | -----------                                                                                 | ---
powershell  | third | PowerShell - Cross-platform automation and configuration tool/framework                     | https://microsoft.com/powershell
terraform   | third | Terraform enables you to safely and predictably create, change, and improve infratstructure | https://terraform.io/
tofu        | third | OpenTofu lets you declaratively manage your cloud infrastructure                            | https://opentofu.org
wine-stable | third | WINE Is Not An Emulator - runs MS Windows programs                                          | https://www.winehq.org

## Consider for Install

Package             | Type | Description                                | URL
-------             | ---- | -----------                                | ---
Term::ExtendedColor | cpan | Color screen output using 256 colors       | https://metacpan.org/pod/Term::ExtendedColor
File::LsColor       | cpan | Colorize input filenames just like ls does | https://metacpan.org/pod/File::LsColor
pydf                | pipx | df(1) clone with colour output             | https://github.com/garabik/pydf

# Post Baseline Tasks

- Prompt user to login to firefox sync
- Prompt user to configure Tridactyl Native Messaging by typing
  `:installnative<ENTER>` in Firefox and then running the command it prints

