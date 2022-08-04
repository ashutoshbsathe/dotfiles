# Arch Linux Install

1. Make sure you're connected to internet `ping google.com`
2. Type `lsblk` to locate the disk you want to install (something like `sda`) 
3. `cfdisk /dev/sda` to pull up partition manager
4. Make your partitions (usually 250-512M for EFI, 512M-4G for swap, ~20-50G for /root and rest for home)
5. Write the partition table from `cfdisk`
6. Type `lsblk` and make sure that the 4 partitions are where you want them to be
7. Make correct file systems for all the partitions
   1. `mkfs.vfat /dev/sda1` - EFI
   2. `mkswap /dev/sda2` & `swapon /dev/sda2` - swap
   3. `mkfs.ext4 /dev/sda[3,4]` - /root and /home partitions
8. Mounting correct partitions
   1. `mount /dev/sda3 /mnt`
   2. `mkdir -p /mnt/boot/efi; mount /dev/sda1 /mnt/boot/efi`
   3. `mkdir /mnt/home; mount /dev/sda4 /mnt/home`
9. Install the arch linux: `pacstrap /mnt base base-devel linux linux-firmware git vim neovim ` (choose `linux-lts` fpr LTS kernel -- usually recommended for nvidia drivers. Also install `nvidia` package with pacstrap)
   1. Optionally also install microcode for your CPU (recommended when running bare metal) `amd-ucode` or `intel-ucode`
10. Generate filesystem: `genfstab -U /mnt >> /mnt/etc/fstab`. Check that correct information got written: `cat /mnt/etc/fstab`
11. Change into arch installation using `arch-chroot /mnt`
12. Localization - Edit `/etc/locale.gen` and delete `#` from the beginning of `en_US.UTF-8 UTF-8` and save it. Then do `locale-gen` After this edit `/etc/locale.conf` and add `LANG=en_US.UTF-8`
13. Timezone - `ls /usr/share/zoneinfo` to list all zones and then `ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime` to select your zone. Now sync the clock properly `hwclock --systohc --utc`
14. Set the root password - type `passwd`
15. Set the hostname - Edit `/etc/hostname` Also do `systemctl enable dhcpcd` so that it will be started at boot time to get IP. `systemctl enable NetworkManager` if dhcpcd is not found
16. Install rEFInd - `sudo pacman -S refind efibootmgr networkmanager wpa_supplicant dialog mtools dosfstools linux-headers openssh`
    1. Do `refind-install --usedefault /dev/sda1 --alldrivers`
    2. `mkrlconf`
    3. Edit `/boot/refind_linux.conf` to delete first 2 entries corresponding to archiso
    4. Edit `/boot/efi/boot/refind.conf` search for "Arch Linux" and change the options part to change it to "root=/dev/sda1" instead of long UUID. Do this for `refind_linux.conf` file above too if needed
17. Add a user: `useradd -mG wheel ashutosh`
    1. Set password using `passwd ashutosh`
    2. Give sudo privileges `EDITOR=vim visudo` and look for `wheel` group. Look for the one with `wheel ALL= (ALL) ALL` and uncomment it (don't delete the % sign)
18. Finally `exit` from chroot and reboot

# AUR helper

1. `git clone https://aur.archlinux.org/yay-git.git`
2. `cd yay-git`
3. `makepkg -si`

# NVIDIA drivers

1. Install `nvidia` and `nvidia-settings` package. Swap `nvidia` with `nvidia-lts` package if you're using `linux-lts`
2. If that doesn't work, use `nvidia-beta` from AUR
3. Refer to [this](https://www.youtube.com/watch?v=sBzAC4glyvE) video in case something related to NVIDIA f's up

# Window Manager

[Example](https://www.youtube.com/watch?v=pouX5VvX0_Q)

1. Update for the sake of it `pacman -Sy`
2. Install X11 and dependencies:
   1. `sudo pacman -S xf86-video-fbdev xorg xorg-server xorg-xinit libx11 libxinerama webkit2gtk picom nitrogen firefox`
   2. You will also need following packages:
      1. `lxappearance` - a light tool to switch appearance of windows, fonts and gtk themes
      2. `nitrogen` - a free program for setting wallpapers. `feh` is also an alternative. These are must for restoring wallpapers properly
      3. `pcmanfm` -file manager that also lets you set wallpaper and desktop icons
      4. `xclip` - clipboard manager
      5. `libxft-bgra` - needed for some ricing stuff
3. Also install `lightdm` and `lightdm-gtk-greeter`. After installing these, go to `[Seat:*]` section of the ``/etc/lightdm/lightdm.conf` and change `greeter-session` to `lightdm-gtk-greeter`
   1. Add an entry for DWM too - `mkdir -p /usr/share/xsessions` and copy the `dwm.desktop` file from your git repo into it
4. Set your wallpaper using `feh` and then edit `/etc/lightdm/Xsession` and at the very end just before e`xec $@`, add `sh ~/.fehbg` to restore wallpaper
5. Need `xmenu` to be installed for my config

# Audio

1. Install `pulseaudio` and then `systemctl --user enable pulseaudio `
2. Also install `pavucontrol` and `pasystray`

# System Controls

1. `pamix-git` from AUR to configure the pulseaudio properly
2. `nmtui` - terminal interface for network manager or `nmcli`  for other stuff. `nmtui` is pretty much a must for working with window managers. TODO: Can we configure themes etc for `nmtui` ?
3. Install `dunst` and `notification-daemon` and then create the service file for `org.freedesktop.Notifications` using notification-daemon
4. Then you can use any systray with notifications in my build of dwm

# Customizations

1. Use yay to install `nerd-fonts-complete`

# X11 Config

* DPMS settings for arch might be in `/usr/share/X11/xorg.conf.d`
* `sleep 1; xset -dpms` to disable DPMS and prevent screen blanking. Install `xorg-xset` if command not found
