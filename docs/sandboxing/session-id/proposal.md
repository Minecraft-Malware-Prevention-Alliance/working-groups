# Session ID Security Proposal

This proposal seeks to sandbox tokens used to log in to Minecraft servers, which are called session IDs.

## Background

Currently, session IDs are stored on the Minecraft client. The client presents the session IDs to Mojang's session server when logging into a server. This configuration presents several issues when it comes to security. A malicious Minecraft mod could potentially read the session IDs from the process, and send it to its owner. This would allow the malware spreader to use the victim's session IDs to log in to Minecraft servers for 24 hours. There is no way to invalidate the session ID, and the only recourse the victim has is to disable multiplayer in their Xbox settings.

## Proposed solution

For clarity, we will refer to Java process that runs Minecraft as the Minecraft process, and the other process as the session ID process.

At some point during or before the launch, the session ID is given to the session ID process. The session ID is them removed from the Minecraft process. The Minecraft process then has `com.mojang.authlib.yggdrasil.YggdrasilMinecraftSessionService#joinServer` rerouted to ask the session ID process to join servers instead. The session ID process then uses the session ID to contact the Mojang session servers.

If sandboxing is being used, the session ID process ideally should be separated by from the Minecraft process while still being able to communicate with it.

## Reasons for this solution

This solution stays secure even if the Minecraft process is fully under the control of an attacker. 

## Pros

This solution is relatively simple to implement and can work well within the current modding framework. It is not invasive and keeps multiplayer/multiplayer verification working while being totally invisible to the client.

## Cons

This solution requires modifying Authlib, which is not released under an open source licence. This would present copyright issues, which would make implementation more difficult. In addition, Authlib is liable to change because Mojang has made no guarantees about its stability

## Implementation details

The Minecraft and the session ID process should be separated by a sandbox, but that is beyond the scope of this proposal. If the session ID process is written in Java, care must be taken in order to ensure that it cannot be attached to. This can be done with the JVM flag `+XX:DisableAttachMechanism`.

Implementations of this system must not use the arguments to a process to pass the session ID, as it may expose the Session ID through OS mechanisms such as the procfs or Windows' process API

## Alternatives

Using a `URLStreamHandler` was considered instead, but this presents a few issues.
- Mods may set their own URLStreamHandler, which would then cause logging into online mode servers to mysteriously fail
- URLStreamHandlers may slow down networking

## Concerns

### DRM

Because this modifies Authlib, it could be seen as modifying DRM by potentially allowing you to choose a different session server and bypass certain protections.

## Implementations

[NoSession](https://github.com/thefightagainstmalware/NoSession) is an implementation of a similar system. Full disclosure: One of the authors of this proposal the maintainer of this implementation.
