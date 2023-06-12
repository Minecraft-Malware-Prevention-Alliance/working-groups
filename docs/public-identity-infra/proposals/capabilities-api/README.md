> ***Note:** this is a draft. **Constructive** criticism will be welcomed.*
# Capabilities API
This document proposes locking dangerous packages and classes,
and allowing CAs to give a mod capabilities, allowing it to access forbidden classes.

Formerly known as the Permissions API. 

### Proposal Contributors
- [Laxla](https://github.com/LaylaMeower)

### Proposal Origins
- [This discussion](https://discord.com/channels/1115852272245686334/1117392205787693107/1117454247529812115) in the MMPA discord, in `#wg-public`

### Definitions
- **CA** - Certificate/Capability Authority, see [the working group](../../README.md).

## Goals
- Preventing mods from accessing dangerous packages
- Allowing all current possible mod functionality to stay possible

## Non-Goals
- Allowing CAs to monopolize mod features
- Defining what will happen to a CA when breaking the trust laws, nor defining said trust laws
- Deciding *how* jars will be signed
- Defining the process that CAs should go through before giving capabilities (that is their own thing to figure out)

## Proposal
While signing is useful for checking mods weren't modified or infected,
it has lots more potential—we can send much more than simply, "hey, this is the mod!".
We can tell the CA more, for example, that this mod wants to use unsafe code, or natives, or Mixins...

We propose to add a capabilities API that allows mods to use forbidden packages and classes, under approval from the CA.

This proposal improves the security of using things such as classloading, reflection, unsafe blocks, native code, etc.,
but doesn't prevent us from using them completely.

In the case of failed communication with the CA, we propose to show a big red scary warning pop up,
with the classic "Here be dragons!" warning and "I know what I'm doing!" button,
and give mods the capabilities they need to work.

### How will that work?

When sending the mod's certificate to the CA to approve, we'll append a list of capabilities the mod needs.
The CA will take these capabilities into account, and may reject the certificate we've sent.

#### Tech Talk

There are three ways to implement the check for forbidden code.
We propose to require a mod-loader to implement at least two of them.
1. **Java Agent** - requires an argument to the `java` command.
2. **Custom Classloader** - implementing `ClassLoader` and delegating to the original one after some checks. There are two variations of this method:
   - **Plural Classloader** - creating a new classloader per mod.
   - **Singular Classloader** - creating a single custom classloader, that'll use the stack trace to see what mod has invoked what. Will require additional security measures, such as using Java 9's modules.
3. **ASM Scan** - inspecting the jar with ASM before even loading it. This is the slowest method of all, although debatable-y the safest. 

### But won't someone Mixin into another mod, "stealing" their capabilities?

We're proposing two solutions:
1. Creating *two* Mixin capabilities (note that mixing somewhere still requires the capability to use the target class): 
   1. `mixin` - allows to Mixin Minecraft classes.
   2. `mixin-elevated` - allows to Mixin other mods.
2. Creating a _dynamic_ mixin capability, `mixin-$package` - listing all mixin targets to the CA.

This will improve the security of Mixins—although we check for forbidden code in the mixin package, too.

### But won't that delay mod reviews by a lot?

Yes, unfortunately.

### Wait, but what about the file system?

We propose to create a _cross-mod-loader_ API
(as in, the same signature in all mod-loaders; not necessarily the same implementation)
to allow mods to read and write files from the `.minecraft/config` directory,
and the `~/.minecraft/config/global` directory.

#### Tech Talk

This could be done by using the `okio` library,
blocking the `okio.FileSystem.SYSTEM`, `okio.FileSystem.Companion.SYSTEM`
and `okio.FileSystem.Companion.getSYSTEM()` code elements,
and creating custom file systems that mods will be able to use (`GlobalConfigFileSystem` and `LocalConfigFileSystem`).

### Examples of dangerous packages
*[Source](https://docs.google.com/document/d/1EpynBXdKLD69F0F0nk-Sph3FXd18IMs8PhXENB7dl6g/edit#heading=h.b4y2p3mjmgab); Credit to the [MoCKoGE](https://GitHub.com/LaylaMeower/MoCKoGE) community, especially [NerjalNosk](https://github.com/NerjalNosk)*
* `java.io` - Direct access to the file system is dangerous.
* `java.nio` - same as above.
* `sun.nio` - Another file I/O alternative.
* `java.lang.ClassLoader` - Allows restriction bypass.
* `jdk.internal` - Provides access to the JVM internal aspects (e.g., a variation of ASM).
* `sun.misc.Unsafe` - Allows bypassing the restrictions set here.
* `java.lang.ProcessBuilder` - allows running arbitrary code.
* `java.reflect` - allows to modify code.
* `java.lang.reflect` - core part of the above package.
* `java.lang.Package` - ensues reflection exposition.
* `kotlin.reflect.full` - A branch of the kotlin reflection library (`kotlin.reflect`) that also allows modification.
* `sun.reflect` - regular reflection alternative
* `java.lang.runtime` - another reflection alternative.
* `java.lang.invoke` - yet another reflection alternative.
* `java.lang.instrument` - Agents and bytecode injection.
* `java.lang.constant` - not really sensible, but only really useful for Java internals, and using it shouldn’t be considered.
* `java.lang.Compiler` - runtime compiler accessor.
* `java.lang.Console` - Provides access to many JVM-controlling functions.
* `java.lang.System` - seems fairly explicit as for how that can be sensible.
* `java.lang.LiveStackFrame` - JVM bug, intended to be package private.
* `java.lang.Runtime` - includes System-related methods. Only accessible ones should be provided via a façade.
* `java.lang.Shutdown` - Can force-stop process (alternative to `System.exit()`).
* `java.lang.Terminator` - yet another alternative to `System.exit()`.
* `java.lang.StackWalker` - Can be exploited to know more of the already run code. Still under debate.
* `java.rmi` - Remote Method Invocation can cause some fairly serious security issues when it comes to multi-device connections.
* `javax.rmi` - Alternative for the above.
* `sun.rmi` - Yet another RMI alternative.
* `org.objectweb.asm` - ASM can be used to modify bytecode on runtime. Yes, it's another reflection alternative. And it's VERY powerful.
* `org.spongepowered.asm` - Yes indeed, we're suggesting to restrict the mixin library. It can be used to modify other mod's behaviors.

> ***Note:** this list is a WIP, and contributions are welcomed.*

## Alternatives
- _Simply have "loader plugins" that execute without blocking access to special classes._
  Popular mods such as sodium use lots of unsafe code,
  ![IMS, Admin: sodium already needs unsafe for like 50% of the codebase](sodium_unsafe.png "Discord message from IMS")
  and a big warning window every time you open Minecraft with sodium can be very irritating.
- *Don't block dangerous code at all.* But we're talking security, and that's unsecure.