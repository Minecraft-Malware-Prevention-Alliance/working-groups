> ***Note:** this is a draft.*
# Permissions API
This document proposes locking dangerous packages and classes, and allowing the trust root to give mods permissions to access locked classes.

### Proposal Contributors
- [Laxla](https://github.com/LaylaMeower)

### Proposal Origins
- [This discussion](https://discord.com/channels/1115852272245686334/1117392205787693107/1117454247529812115) in the MMPA discord, in `#wg-public`

### Definitions
- **CA** - Certificate Authority

## Goals
- Preventing mods from accessing dangerous packages
- Allowing all current possible mod functionality to stay possible

## Non-Goals
- Allowing CAs to monopolize mod features
- Defining what will happen to a CA when breaking the trust laws, nor defining said trust laws
- Deciding *how* jars will be signed
- Defining the process that CAs should go through before allowing permissions (that is their own thing to figure out)

## Proposal
While signing is useful for checking mods weren't modified or infected,
it has lots more potential—we can send much more than simply, "hey, this is the mod!". We can tell the CA more: that this mod wants to use unsafe code, or natives, or Mixins...

We propose to add a permissions API that allows mods to use forbidden packages and classes.

This proposal improves the security of using things such as classloading, reflection, unsafe blocks, native code, etc., but doesn't prevent us from using them completely.

In the case of failed communication with the CA, we propose to show a big red scary warning pop up,
with the classic "Here be dragons!" warning and "I know what I'm doing!" button, and give mods the permission they require to work.

### How will that work?

When sending the mod's certificate to the CA to approve, we'll append a list of permissions the mod needs to use. The CA will read the mod data and the permissions, and tell us if the mod is secure. If it is, we'll load it.

#### Tech Talk

There are three ways to implement the check for forbidden code. We propose to require a modloader to implement at least two of them.
1. **Java Agent** - requires an argument to the `java` command.
2. **Custom Classloader** - implementing `ClassLoader` and delegating to the original one after some checks. There are two variations of this method:
  - **Plural Classloader** - creating a new classloader per mod.
  - **Singular Classloader** - creating a single custom classloader, that'll use the stack trace to see what mod has invoked what. Will require additional security measures, such as using Java 9's modules.
3. **ASM Scan** - inspecting the jar with ASM before even loading it. This is the slowest method of all, although debatably the safest. 

### But won't someone Mixin into another mod, stealing their permissions?

We propose creating *two* Mixin permissions:
1. `mixin` - allows to Mixin Minecraft classes.
2. `mixin-elevated` - allows to Mixin other mods.

This will improve the security of Mixins - although we check for forbidden code in the mixin package, too.

### Examples of dangerous packages
 *[Source](https://docs.google.com/document/d/1EpynBXdKLD69F0F0nk-Sph3FXd18IMs8PhXENB7dl6g/edit#heading=h.b4y2p3mjmgab); Credit to the [MoCKoGE](https://GitHub.com/LaylaMeower/MoCKoGE) community, especially [NerjalNosk](https://github.com/NerjalNosk)*
* `java.io` - Direct access to the file system is dangerous.
* `java.nio` - same as above.
* `sun.nio` - Another file I/O alternative
* `java.lang.ClassLoader` - Allows restriction bypass
* `jdk.internal` - Provides access to the JVM internal aspects (e.g., a variation of ASM)
* `sun.misc.Unsafe` - Allows bypassing the restrictions set here.
* `java.reflect` - allows to modify code.
* `java.lang.reflect` - core part of the above package.
* `java.lang.Package` - ensues reflection exposition.
* `kotlin.reflect.full` - A branch of the kotlin reflection library (`kotlin.reflect`) that also allows modification
* `sun.reflect` - regular reflection alternative
* `java.lang.runtime` - another reflection alternative
* `java.lang.invoke` - yet another reflection alternative
* `java.lang.instrument` - Agents and bytecode injection
* `java.lang.constant` - not really sensible, but only really useful for Java internals, and using it shouldn’t be considered
* `java.lang.Compiler` - runtime compiler accessor
* `java.lang.Console` - Provides access to many JVM-controlling functions
* `java.lang.System` - seems fairly explicit as for how that can be sensible
* `java.lang.LiveStackFrame` - JVM bug, intended to be package private.
* `java.lang.Runtime` - includes System-related methods. Only accessible ones should be provided via a façade
* `java.lang.Shutdown` - Can force-stop process (alternative to `System.exit()`)
* `java.lang.Terminator` - yet another alternative to `System.exit()`
* `java.lang.StackWalker` - More of a safety issue, can be exploited to know more of the already run code.
* `java.rmi` - Remote Method Invocation can cause some fairly serious security issues when it comes to multi-device connections
* `javax.rmi` - Alternative for the above
* `sun.rmi` - Yet another RMI alternative
* `org.objectweb.asm` - ASM can be used to modify bytecode on runtime. Yes, it's another reflection alternative. And it's VERY powerful.
* `org.spongepowered.asm` - Yes indeed, we're suggesting to restrict the mixin library. It can be used to modify other mod's behaviors.

## Alternatives
- _Simply have "loader plugins" that execute without blocking access to special classes._
  Popular mods such as sodium use lots of unsafe code,
  ![Discord message from IMS](soidum_unsafe.png)
  and a big warning window every time you open Minecraft with sodium can be very irritating.
- *Don't block dangerous code at all.* But we're talking security, and that's unsecure.