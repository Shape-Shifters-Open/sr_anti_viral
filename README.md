# sr_anti_viral
Simple suite that installs scriptJobs to counteract known "viral" scriptJobs spread through asset sharing.

Put the entire folder in your `site_packages` folder, then add the following to your `userSetup.py`:
```
# sr_anti_viral Start:
import sr_anti_viral
sr_anti_viral.protection.register_protection_script()
# sr_anti_viral End
```

This will "cauterize" any file that contains the script nodes that spread the known virus.  Presently, hard-coded to target the rapidly spreading script job that shows a message that translates to "Your file is health, that is all I am here to say," and goes on to create `vaccine.py` and alter the `userSetup.py`.

If your userSetup.py has already been altered by this, this tool won't revert those changes or remove the new `.py` files from the scripts folder- but it will prevent any Maya session from adding more.
