# Assets Directory

This directory contains media assets for the portfolio site.

## Video Intro

- `intro.webm` - 10-second cinematic intro video (1920x1080, 12fps, VP9 WebM, ~3MB)
- `intro_poster.jpg` - Poster frame for the video (50KB recommended)

### Video Specifications

- **Duration**: 10 seconds
- **Resolution**: 1920 × 1080
- **Frame Rate**: 12 fps
- **Format**: VP9 WebM
- **Size**: ~3 MB (must be < 25 MB for GitHub Pages)
- **Content**: Logo swipe → terminal $ prompt → metrics dashboard fade

### Creating the Video

You can create this video using:
- FFmpeg: `ffmpeg -i source.mp4 -vf "scale=1920:1080,fps=12" -c:v libvpx-vp9 -b:v 3M -c:a none intro.webm`
- Video editing software (Premiere, Final Cut, DaVinci Resolve)
- Online tools that support VP9 encoding

### Notes

- Video must be **muted** for autoplay to work
- File must be **< 25 MB** and NOT tracked by Git-LFS
- Use `playsinline` attribute for iOS compatibility

