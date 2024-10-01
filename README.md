# ![Acestream logo](acestream/data/images/streamer-32.png) Acestream Flatpak

It's just the program you can downlaod from the official [web](https://docs.acestream.net/products/#linux) site and packaged into a flatpak.

To build the flatpak clone the repo and build it with the command:

``` bash
git clone https://github.com/jaimejj54/acestream-flatpak.git
cd acestream-flatpak
flatpak-builder --force-clean --install-deps-from=flathub --repo=repo builddir org.Acestream.engine.yml
flatpak build-bundle repo acestream-engine.flatpak org.Acestream.engine
flatpak install --user acestream-engine.flatpak
```

## Additional configuration files

In order to open acestream and a video player with just clicking an acestream link I use some additional files and configurations. First, I use a simple script (`acestream.sh`) that checks if acestream is running and opens it if not. Then, it opens the video player (in this case the flatpak version of mpv) with the link corresponding to the link received. The link is of type <acestream://123456789abcdefghijklmnopqrstuvwxyz>. You can choose your favorite video player changing 'flatpak run io.mpv.Mpv --profile=acestream' with the path of the program (for example, vlc).

I place the file in `~/scripts/`, but if you want to it in other folder change the path in the desktop file:

```bash
cp acestream.sh ~/scripts/
```

To handle the click on the link I installed a desktop file (`acestream-mpv.desktop`) that runs the script.

```bash
sudo desktop-file-install acestream-mpv.desktop
gio mime x-scheme-handler/acestream acestream-mpv.desktop
```

## mpv configuration file

As you might have seen, I use a custom profile for mpv. The configuration file is `mpv.conf`.

For classic mpv:

```bash
cp mpv.conf ~/.config/mpv/
```

For flatpak mpv:

```bash
cp mpv.conf ~/.var/app/io.mpv.Mpv/config/mpv/
```

## Known issues

- The tray icon is not shown in KDE. In GNOME three dots are displayed (Adawaita theme), but it can be fixed. Enter the extension settings and add an entry in the AppIndicator and KStatusNotifierItem Support. The ID is `acestream-engine`. If you have an icon theme installed there may be a custom icon. For example, the [Tela Icon](https://github.com/vinceliuice/Tela-icon-theme) theme has its own. The icon name is `acestream-tray`. Nevertheless, you can set the path of the image you want to be displayed (`~/acestream-flatpak/acestream/data/images/streamer-32.png`).

- The port used by acestream might be different than mine. You can change it in the script or by clicking the tray icon, in remote access.

---

Please, any question or suggestion contact me.
