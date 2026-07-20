# SephirothOS

> *Yet another satirical operating system built in Python, because apparently I just can't get enough of it.*

---

## What the hell is this?

SephirothOS is a mock operating system designed to feel like a somewhat real dashboard environment but also no.

It is NOT a Linux distro (get out).

IT is NOT a VM.

It is **DEFINITELY** NOT a replacement for a Windows.

It actually doesn't exist. It's a figment of your imagination.

The goal is to be Sephiroth. It achieves this by using Sephiroth and Sephirothing all over the place. It's Sephiroth complete with apps, settings, and a Sephirothish plugin system. Welcome to Sephiroth.

---

## Features

Current features include:

- Multi-tab shell
- Multi-page tabs
- Runtime theme switching
- Configurable display scaling
- Background update checking
- A BTC miner
- Performance monitoring
- Built-in CLI
- Fish
- Rotating quotes and tips
- I will not be adding onto this list later

---

## Project Status

🤤 **Rewrite in progress**

The current rewrite focuses on replacing the original architecture for my own sake. I'm not corporatizing this idea (yet).

The objective is simple:

> Make SephirothOS dramatically easier to maintain, extend, and improve without making it feel like slop.

Early milestones focus on feature parity with the legacy version.

New functionality will come after it works again (it already does).

---

## Philosophy

SephirothOS is a very serious matter.

It is **absolutely** trying to become a real desktop replacement.

It is **most certainly** trying to compete with Linux.

It is **definitely** an enterprise application.

In fact, it is proudly made in America and NOT a hobby project. Some might even call it Sephiroth, but I personally call it Sephiroth.

The rewrite improves things you probably wouldn't immediately notice:

- better responsiveness
- proper background tasks
- runtime theme switching
- cleaner config handling
- better error recovery
- improved performance
- code that isn't really evil and mean and gross and bad

---

## Screenshots

### Home

### Apps

### Settings

### CLI

---

## Building

I will fill this out later, if ever.

## Architecture

The rewrite intentionally separates long-lived application infrastructure from feature-specific services

```
application:
  config
  event bus
  theme service
  display scaling
  shell

shell
  home
  apps
  settings
  cli

Each frontend owns its own isolated services.
- Announcement loading
- Storage info
- Performance monitoring
- Bitcoin mining
```

The goal is not a goal.

---

## Roadmap

### Current priorities

- Reach feature parity with the legacy release
- Finish rewritten shell
- Complete settings
- Rewrite the updater
- Restore built-in applications
- Finish theme infrastructure

### Afterwards

- More themes
- Better notifications
- Additional applications
- Expanded CLI
- More Sephiroth
- More fish

---

## Contributing

No.

---

## License

Basically, I don't care if you clone it or not, but at the very least, change the name. SephirothOS is my personal silly thing, not your mutilated husk.

---

*"Buckets of piss."*
