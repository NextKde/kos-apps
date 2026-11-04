# Notices

KOS Weather is derived from NextKde and distributed under GPL-3.0-or-later; see
LICENSE and SOURCE_PROVENANCE.md. Preserve existing source notices. Copyright
remains with the respective NextKde contributors and upstream authors.

The exported `shared/demo-ui` QML, GLSL and QSB implementations were synchronized
by NextKde from `nextkdeAppDemo/shared/qml`. NextKde's module notice identifies both
parent and upstream as GPL-3.0. The preserved `shared/demo-ui/upstream-sha256.json`
records upstream asset hashes; standalone packaging does not replace those assets.
Particle textures and shader assets are included from pinned Weather sources.

Qt 6, optionally KDE Frameworks 6 WindowSystem, and the Go toolchain/standard
library are external system dependencies with their own licenses. They are not
source-vendored here. Redistributors of binaries must satisfy those dependencies'
license and source obligations as well as GPL obligations for this application.
No third-party Go modules are required.

Weather forecasts and geocoding use Open-Meteo (https://open-meteo.com/);
source data attribution and service terms apply independently of this source
license. Air-quality data use the Open-Meteo Air Quality API and its underlying
CAMS data. See https://open-meteo.com/en/docs and
https://open-meteo.com/en/docs/air-quality-api for provider attribution, data
licenses and usage limits. This repository does not redistribute provider data.
The app's upstream UI retains its Open-Meteo attribution.

Application metainfo declares its metadata CC0-1.0, as in the upstream source.
