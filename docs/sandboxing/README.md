# Sandboxing

Sandboxing is a concept where we try to sandbox mods from the users host system without loosing any performance like in a VM. Currently, we 

## Platforms

### Windows

There is no clear solution to this yet, but it should take heavy inspiration from [The Chromium Windows Sandbox](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/design/sandbox.md#Sandbox-Windows-architecture)

### Linux

We could use something like flatpak here, though its unlikely, the current most likely solution is to use linux namespaces to work like a docker-like system.

This is mainly solved other then implementation details

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

#### Notice

If you would like to: 
- Use another launcher (while sandboxed)
- Play minecraft pre-1.7

You would need to use the python file [patcher.py](./macos/patcher.py)

###### Usage 

For patching the profile:
`python patcher.py --dir=/path/to/sandbox/file/minecraft-sandbox.sb --user-patch`

