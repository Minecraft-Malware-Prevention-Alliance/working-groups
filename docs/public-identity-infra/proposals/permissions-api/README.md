> ***Note:** this is a draft.*
# Permissions API
This document proposes locking dangerous packages and classes, and allowing the trust root to give mods permissions to access locked classes.

### Proposal Contributors
- [Laxla](https://github.com/LaylaMeower)

### Proposal Origins
- [This discussion](https://discord.com/channels/1115852272245686334/1117392205787693107/1117454247529812115) in the MMPA discord, in `#wg-public`

## Goals
- Preventing mods from accessing dangerous packages
- Allowing all current possible mod functionality to stay possible

## Non-Goals
- Allowing trust authoroties to monopolize mod features
- Defining what will happen to an authority when breaking the trust laws, nor defining said trust laws

## Proposal
While signing is useful for checking mods weren't modified or infected,
it has lots more potential—as we can check for much more than simply "load" or "don't load".

We propose to add a permissions API that allows mods to use forbidden packages and classes.

> ***Note:** The following is an example and is not the actual syntax that'll be used.*

Currently, the trust authority simply sends a "load" and "don't load" response:
```json
{
  "mycoolmod": true,
  "fabricapi": true,
  "meowmeow2000": false
}
```
We propose changing it to a permission object:
```json5
{
  "mycoolmod": {
    "valid": true,
    "reflection": true,
    "unsafe": false,
    "natives": false
    // etc
  },
  "fabricapi": {
    "valid": true,
    "reflection": false,
    // etc
  },
  "meowmeow2000": {
    "valid": false
  }
  // etc
}
```

This proposal improves the security of using things such as classloading, reflection, unsafe blocks, native code, etc., but doesn't prevent us from using them completely.

In the case of failed communication with the trust authority, we propose to show a big red scary warning pop up,
with the classic "Here be dragons!" warning and "I know what I'm doing!" button.

Examples of dangerous packages ([Source](https://docs.google.com/document/d/1EpynBXdKLD69F0F0nk-Sph3FXd18IMs8PhXENB7dl6g/edit#heading=h.b4y2p3mjmgab); Credit to the MoCKoGE community, especially [NerjalNosk](https://github.com/NerjalNosk)):
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