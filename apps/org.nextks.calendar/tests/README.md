# Calendar typography regression

With a Calendar build configured using `-DBUILD_TESTING=ON`, run
`ctest --test-dir BUILD -R 'kos-calendar.typography|kos-demo.menu-sizing' --output-on-failure`.
The checks use private D-Bus, PIM data and preference directories, then remove them.

To retain logs and screenshots, run
`python3 apps/org.nextks.calendar/tests/run-typography-review.py BUILD OUTPUT_DIRECTORY`.
Use a dedicated directory; language subdirectories must not already exist.
`KOS_TEST_OUTPUT_DIR` also retains results when invoking the test through CTest.
Optional trailing language codes are `zh_CN`, `en_US` and `pt_BR`.

The review covers four text presets at 900×630 and 760×500, settings, all four
calendar views, event/reminder editors, date/time pickers, repeated menu opening,
menu actions, a save into the private PIM and restoring defaults. The fixture
checks intrinsic label sizes and screenshots the largest presets for review.
It loads the application's QML with QtTest instrumentation and compiled shared
components; it does not operate the user's running Calendar instance.

The default backend is offscreen/software. For visual review in an authorized
isolated Wayland session, set `KOS_TEST_QPA=wayland`, `KOS_TEST_BACKEND=opengl`
and the session's `WAYLAND_DISPLAY` / `XDG_RUNTIME_DIR`. `KOS_TEST_SCALE=1.5`
can additionally exercise fractional display scaling. Such screenshots require
visual inspection; a successful geometry test alone is not visual acceptance.
