# Sandboxing

Sandboxing is a concept where we try to sandbox mods from the users host system without loosing any performance like in a VM. Currently, we 

## Platforms

### Windows

There is no clear solution to this yet, but it should take heavy inspiration from [The Chromium Windows Sandbox](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/design/sandbox.md#Sandbox-Windows-architecture)

### Linux

Linux offers different kinds of isolation using namespacing.
A fairly low-level tool to access these capabilities is `unshare` that allows creating new namespaces for child processes.
`unshare` is fine, if full-isolation should be achieved, but we definitely need *some* access to the host system, and without integrating with multiple tools, `unshare` by itself is undesirable.
A popular tool that utilizes the same capabilities as `unshare` is `bubblewrap`, which is most prominently used by Flatpak. It also allows creating new namespaces, just like `unshare` but additionally provides easy ways to bind paths from the host into the mount namespace.

#### Bubblewrap

Using `bubblewrap` is quite simple. It can be configured by running the `bwrap` binary and defining command line arguments.
As the name suggests it acts as a wrapper, so after specifying bwrap options the main program inside the sandbox can be specified.

##### Base configuration

- `--unshare-all --share-net` - Try to create all kinds of namespaces except for networking
  - Doing unprivileged networking in userspace is slow, which is why we will NOT sandbox the root networking namespace
- `--die-with-parent` - Kill sandbox if launcher crashes/exits
- `--dev /dev --dev-bind-try /dev/dri /dev/dri` - Allow access to DRM devices for hardware accelerated rendering
- `--proc /proc` - Mount namespaced procfs at /proc
- `--unsetenv DBUS_SESSION_BUS_ADDRESS` - The sandbox doesn't have access to the dbus daemon anyway
- Read-only bind mounts
  - `/etc/drirc`
  - `/etc/gai.conf`
  - `/etc/gnutls`
  - `/etc/hostname`
  - `/etc/hosts`
  - `/etc/je_malloc.conf`
  - `/etc/localtime`
  - `/etc/machine-id` - TODO: what are consequences of omitting this
  - `/etc/os-release` - TODO: what are consequences of omitting this
  - `/etc/resolv.conf`
  - `/etc/selinux`
  - `/etc/timezone`
  - `/usr`
  - `/bin`
  - `/sbin`
  - `/lib`
  - `/lib32`
  - `/lib64`
  - `/sys/class`
  - `/sys/dev/char`
  - `/sys/devices/pci????:??` - Possibly multiple?
  - `/sys/devices/system/cpu`
  - Path to game assets and libraries
- Read-write bind mounts
  - Path to game root (`.minecraft`)

##### Desktop integration

- Read-only bind mounts
  - `$XDG_RUNTIME_DIR/pulse` - Access to PulseAudio daemon
  - `$XDG_RUNTIME_DIR/pipewire-?` - Access to PipeWire daemon (`pipewire-0` if unspecified)
  - `$XAUTHORITY` - X11 access
  - `/tmp/.X11-unix/X?` - X11 access (`X0` if `DESKTOP=:0`)
  - `$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY` - Wayland access (`$WAYLAND_DISPLAY` can also be an absolute path)

##### Distro-specific configuration

To solve issues with distro-specific symlinks of files, mostly in `/etc` (i.e. `resolv.conf -> /run/systemd/resolve/stub-resolv.conf`), bind mounts SHOULD use canonical file paths for the host side, while preserving the original path in the sandbox.

- Read-only bind mounts
  - `/nix/store` - Required for Nix installations
  - `/nix/var/nix/profiles` - Required for Nix installations
  - `/run/current-system/sw` - Required for NixOS installations

##### Supporting `xdg-open`

By default xdg-open would launch applications inside our sandbox. We can utilize `xdg-desktop-portal` to open links/paths on the host system.
To do this we *need* dbus, but we neither ensure that it's bound inside the sandboxing, neither do we pass the `DBUS_SESSION_BUS_ADDRESS` variable to the sandbox.
We don't want to allow full access to dbus, as that could allow sandbox escapes (some endpoints allow executing arbitrary commands on the host).
The Flatpak project maintains a tool called `xdg-dbus-proxy` that acts as a filtering reverse proxy for dbus.

As we only need access to `org.freedesktop.portal.*` the call to xdg-dbus-proxy is quite simple:

```console
# PROXIED_BUS_PATH can be an arbitrary path on the host
$ xdg-dbus-proxy $DBUS_SESSION_BUS_ADDRESS $PROXIED_BUS_PATH --filter '--call=org.freedesktop.portal.*=*' '--broadcast=org.freedesktop.portal.*=@/org/freedesktop/portal/*'
```

To give the sandbox access to this filtered dbus, the `bwrap` call must be extended by the following two parameters:
- `--bind $PROXIED_BUS_PATH /tmp/bus` - TODO: can this be read-only?
- `--setenv DBUS_SESSION_BUS_ADDRESS "unix:path=/tmp/bus"`

This is NOT enough to make xdg-open use portals yet. At its current state, we can convince xdg-open that it should use Portals by pretending to be a Flatpak.
This can be achieved by adding the following two parameters to `bwrap`:
- `--unsetenv XDG_CURRENT_DESKTOP` - Don't give xdg-utils any chance to guess the host desktop
- `--setenv DE flatpak` - Skip all further desktop checks in `xdg-utils`

##### Example implementations

- PrismLauncher/PrismLauncher#1160

### MacOS

*Implementation by Game_Time from [minecraft-macos-sandboxing, this repo has now been moved to this document](https://github.com/RayBytes/minecraft-macos-sandboxing)*

The idea for MacOS sandboxing is to completely sandbox Minecraft. This will disable minecraft from accessing any harmful data which it could gain access to. We used apple's sandbox-exec and created a profile for it. The profile will only give access to files which minecraft needs to run.

#### How does it work?

It uses MacOS's inbuilt `sandbox-exec` command to work, as sandbox-exec is a fully native-to-MacOS way to securely sandbox apps. It is used in the backend of many of MacOS's systems, and is still used in XCode's App Sandbox feature to this day. 

#### Usage

Run the command:
`sandbox-exec -f Path/To/The/Sandbox/Profile/minecraft-sandbox.sb /Applications/Minecraft.app/Contents/MacOS/launcher`

*Note: This project is now in beta testing, and may be used on clients properly. Report any bugs in the [discord](https://discord.gg/zPdFK47682)*

#### Sandbox Profile

See [macos-sandboxing.sb](./macos/macos-sandbox.sb)

# Notice

For other launchers, check out the launchers directory.

