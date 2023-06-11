# Sandboxing

Sandboxing is a concept where we try to sandbox mods from the users host system without loosing any performance like in a VM. Currently, we 

## Platforms

### Windows

There is no clear solution to this yet, but it should take heavy inspiration from [The Chromium Windows Sandbox](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/design/sandbox.md#Sandbox-Windows-architecture)

### MacOS

*From [RayAar/minecraft-macos-sandboxing, this repo has now moved to this document](https://github.com/RayBytes/minecraft-macos-sandboxing)*

*Documentation in progress*

TThe idea for MacOS sandboxing is to completely sandbox Minecraft. This will disable minecraft from accessing any harmful data which it could gain access to without this profile. The profile will* only give access to files which minecraft needs to run.

#### How does it work?

It uses MacOS's inbuilt `sandbox-exec` command to work, as sandbox-exec is a fully native-to-MacOS way to securely sandbox apps.

#### Usage

Run the command:
`sandbox-exec -f Path/To/The/Sandbox/Profile/minecraft-sandbox.sb /Applications/Minecraft.app/Contents/MacOS/launcher`


*Note: This project is still in development and may not function as it should, some extra files may still be given access to Minecraft which will be removed in future versions. Be vary of this before using this project.*
#### Sandbox Definition

See [macos-sandboxing.sb](./macos-sandbox.sb)


### Linux

We could use something like flatpak here, though its unlikely, the current most likely solution is to use linux namespaces to work like a docker-like system.

This is mainly solved other then implementation details

