# Acestream Flatpak
It's just the program you can downlaod from the official web site and packaged into a flatpak.

To build the flatpak colen the repo and build it with the command:
<code>
git clone https://github.com/jaimejj54/acestream-flatpak.git
cd acestream-flatpak
flatpak-builder --force-clean --install-deps-from=flathub --repo=repo builddir org.Acestream.engine.yml
flatpak build-bundle repo acestream-engine.flatpak org.Acestream.engine
flatpak install --user acestream-engine.flatpak
<code>
