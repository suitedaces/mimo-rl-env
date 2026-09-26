stream.dash: support for dynamic manifests with SegmentLists
### Checklist

- [X] This is a bug report and not [a different kind of issue](https://github.com/streamlink/streamlink/issues/new/choose)
- [X] [I have read the contribution guidelines](https://github.com/streamlink/streamlink/blob/master/CONTRIBUTING.md#contributing-to-streamlink)
- [X] [I have checked the list of open and recently closed bug reports](https://github.com/streamlink/streamlink/issues?q=is%3Aissue+label%3A%22bug%22)
- [X] [I have checked the commit log of the master branch](https://github.com/streamlink/streamlink/commits/master)

### Streamlink version

6.2.1

### Description

TLDR: It seems that the dash implementation doesn't filter the segments when a reload has happened, causing all segments to be downloaded again.

I have a livestream with a manifest that contains below SegmentList:

```
...
	<Representation id="video-5" mimeType="video/mp4" codecs="avc1.64001e" bandwidth="4600000" width="1920" height="1080">
		<SegmentList presentationTimeOffset="52459080" timescale="1000" duration="4000" startNumber="2">
			<Initialization sourceURL="4792k/ugSxF45MOHE/init-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61" />
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185772-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185773-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185774-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185775-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185776-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185777-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185778-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185779-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185780-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185781-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185782-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185783-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185784-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185785-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185786-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185787-video.mp4?hdntl=exp=1696435540~acl=/*~hmac=1eba0a04cd7d2ec0d55a3a1e2317a9d77d375b1f8a42f0926914bf7575aebd61"/>
		</SegmentList>
	</Representation>
...
```

Nothing really spectacular here, but it seems that the DASH code starts downloading from the top, instead of only the last 3 as with HLS. This is probably a different feature request, but it's somewhat related.

The issue is that after a reload, the whole manifest is reloaded, and it starts downloading at the top again, instead of only the new Segments.

After reload:
```
...
	<Representation id="video-5" mimeType="video/mp4" codecs="avc1.64001e" bandwidth="4600000" width="1920" height="1080">
		<SegmentList presentationTimeOffset="52459080" timescale="1000" duration="4000" startNumber="4">
			<Initialization sourceURL="4792k/ugSxF45MOHE/init-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39" />
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185774-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185775-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185776-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185777-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185778-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185779-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185780-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185781-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185782-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185783-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185784-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185785-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185786-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185787-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185788-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
			<SegmentURL media="4792k/ugSxF45MOHE/178185/segment_178185789-video.mp4?hdntl=exp=1696435545~acl=/*~hmac=a0a36aa15b7c308b9a9e764777805c4ecfb09be9f410767484a1715c25ddfc39"/>
		</SegmentList>
	</Representation>
...
```

I've looked at the code, and it seems the whole playlist is reloaded in `stream.dash.reload()` and there is no code to filter out already downloaded segments.

I'm using streamlink through the Python API, with `.open()` and `.read()`, hence the timestamps and thread names in the debug output.

### Debug log

```text
2023-10-04 10:17:31,764.764 debug      MainThread streamlink.plugins.dash URL=https://dcs-live-uw1.mp.lura.live/server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903; params={}
2023-10-04 10:17:31,766.766 debug      MainThread urllib3.connectionpool Starting new HTTPS connection (1): dcs-live-uw1.mp.lura.live:443
2023-10-04 10:17:32,014.014 debug      MainThread urllib3.connectionpool https://dcs-live-uw1.mp.lura.live:443 "GET /server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903 HTTP/1.1" 200 None
2023-10-04 10:17:32,016.016 debug      MainThread charset_normalizer Encoding detection: utf_8 is most likely the one.
2023-10-04 10:17:32,026.026 debug      MainThread streamlink.utils.l10n Language code: en_US
2023-10-04 10:17:32,026.026 debug      MainThread streamlink.stream.dash Available languages for DASH audio streams: NONE (using: n/a)
2023-10-04 10:17:32,027.027 info      MainThread iptvstreamer Opening stream to https://dcs-live-uw1.mp.lura.live/server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903
2023-10-04 10:17:32,029.029 debug      MainThread streamlink.stream.dash Opening DASH reader for: ('0', None, 'video-5') - video/mp4
2023-10-04 10:17:32,034.034 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment initialization: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.034361Z)
2023-10-04 10:17:32,036.036 debug      MainThread streamlink.stream.dash Opening DASH reader for: ('0', None, 'audio-5') - audio/mp4
2023-10-04 10:17:32,038.038 debug ThreadPoolExecutor-0_0 urllib3.connectionpool Starting new HTTPS connection (1): video-live.dpgmedia.net:443
2023-10-04 10:17:32,040.040 debug Thread-DASHStreamWorker streamlink.stream.dash Reloading manifest ('0', None, 'video-5')
2023-10-04 10:17:32,046.046 debug      MainThread asyncio Using selector: EpollSelector
2023-10-04 10:17:32,046.046 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment initialization: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.046390Z)
2023-10-04 10:17:32,048.048 debug Thread-DASHStreamWorker streamlink.stream.dash Reloading manifest ('0', None, 'audio-5')
2023-10-04 10:17:32,054.054 debug ThreadPoolExecutor-1_0 urllib3.connectionpool Starting new HTTPS connection (2): video-live.dpgmedia.net:443
2023-10-04 10:17:32,055.055 debug Thread-DASHStreamWorker urllib3.connectionpool Starting new HTTPS connection (2): dcs-live-uw1.mp.lura.live:443
2023-10-04 10:17:32,060.060 debug      MainThread streamlink.stream.ffmpegmux ffmpeg version 6.0-static https://johnvansickle.com/ffmpeg/  Copyright (c) 2000-2023 the FFmpeg developers
2023-10-04 10:17:32,060.060 debug      MainThread streamlink.stream.ffmpegmux  built with gcc 8 (Debian 8.3.0-6)
2023-10-04 10:17:32,060.060 debug      MainThread streamlink.stream.ffmpegmux  configuration: --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --enable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libdav1d --enable-libxvid --enable-libzvbi --enable-libzimg
2023-10-04 10:17:32,060.060 debug      MainThread streamlink.stream.ffmpegmux  libavutil      58.  2.100 / 58.  2.100
2023-10-04 10:17:32,060.060 debug      MainThread streamlink.stream.ffmpegmux  libavcodec     60.  3.100 / 60.  3.100
2023-10-04 10:17:32,060.060 debug      MainThread streamlink.stream.ffmpegmux  libavformat    60.  3.100 / 60.  3.100
2023-10-04 10:17:32,061.061 debug      MainThread streamlink.stream.ffmpegmux  libavdevice    60.  1.100 / 60.  1.100
2023-10-04 10:17:32,061.061 debug      MainThread streamlink.stream.ffmpegmux  libavfilter     9.  3.100 /  9.  3.100
2023-10-04 10:17:32,061.061 debug      MainThread streamlink.stream.ffmpegmux  libswscale      7.  1.100 /  7.  1.100
2023-10-04 10:17:32,061.061 debug      MainThread streamlink.stream.ffmpegmux  libswresample   4. 10.100 /  4. 10.100
2023-10-04 10:17:32,061.061 debug      MainThread streamlink.stream.ffmpegmux  libpostproc    57.  1.100 / 57.  1.100
2023-10-04 10:17:32,061.061 info      MainThread streamlink.utils.named_pipe Creating pipe streamlinkpipe-9-1-4469
2023-10-04 10:17:32,062.062 info      MainThread streamlink.utils.named_pipe Creating pipe streamlinkpipe-9-2-6040
2023-10-04 10:17:32,062.062 debug      MainThread streamlink.stream.ffmpegmux ffmpeg command: /usr/local/bin/ffmpeg -nostats -y -i /tmp/streamlinkpipe-9-1-4469 -i /tmp/streamlinkpipe-9-2-6040 -c:v copy -c:a copy -copyts -start_at_zero -f mpegts pipe:1
2023-10-04 10:17:32,063.063 debug Thread-1 (copy_to_pipe) streamlink.stream.ffmpegmux Starting copy to pipe: /tmp/streamlinkpipe-9-1-4469
2023-10-04 10:17:32,063.063 debug Thread-2 (copy_to_pipe) streamlink.stream.ffmpegmux Starting copy to pipe: /tmp/streamlinkpipe-9-2-6040
2023-10-04 10:17:32,163.163 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/init-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1280
2023-10-04 10:17:32,163.163 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 1: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.163452Z)
2023-10-04 10:17:32,164.164 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment initialization: completed
2023-10-04 10:17:32,186.186 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185950-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1745420
2023-10-04 10:17:32,192.192 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/init-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1208
2023-10-04 10:17:32,192.192 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 1: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.192871Z)
2023-10-04 10:17:32,193.193 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment initialization: completed
2023-10-04 10:17:32,214.214 debug Thread-DASHStreamWorker urllib3.connectionpool https://dcs-live-uw1.mp.lura.live:443 "GET /server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903 HTTP/1.1" 200 None
2023-10-04 10:17:32,216.216 debug Thread-DASHStreamWorker charset_normalizer Encoding detection: utf_8 is most likely the one.
2023-10-04 10:17:32,221.221 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185950-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 103963
2023-10-04 10:17:32,350.350 debug Thread-DASHStreamWorker urllib3.connectionpool https://dcs-live-uw1.mp.lura.live:443 "GET /server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903 HTTP/1.1" 200 None
2023-10-04 10:17:32,371.371 debug Thread-DASHStreamWorker charset_normalizer Encoding detection: utf_8 is most likely the one.
2023-10-04 10:17:32,379.379 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 2: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.379296Z)
2023-10-04 10:17:32,382.382 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 1: completed
2023-10-04 10:17:32,403.403 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185951-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1880960
2023-10-04 10:17:32,529.529 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 2: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.529373Z)
2023-10-04 10:17:32,531.531 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 1: completed
2023-10-04 10:17:32,572.572 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185951-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 100474
2023-10-04 10:17:32,589.589 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 3: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.589479Z)
2023-10-04 10:17:32,591.591 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 2: completed
2023-10-04 10:17:32,592.592 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 3: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.592798Z)
2023-10-04 10:17:32,594.594 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 2: completed
2023-10-04 10:17:32,609.609 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185952-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 102117
2023-10-04 10:17:32,616.616 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185952-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1749488
2023-10-04 10:17:32,664.664 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 4: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.664882Z)
2023-10-04 10:17:32,665.665 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 3: completed
2023-10-04 10:17:32,690.690 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185953-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 99864
2023-10-04 10:17:32,743.743 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 5: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.743061Z)
2023-10-04 10:17:32,743.743 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 4: completed
2023-10-04 10:17:32,789.789 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185954-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 104877
2023-10-04 10:17:32,798.798 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 6: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.798310Z)
2023-10-04 10:17:32,799.799 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 5: completed
2023-10-04 10:17:32,803.803 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 4: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.803131Z)
2023-10-04 10:17:32,805.805 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 3: completed
2023-10-04 10:17:32,819.819 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185955-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 100514
2023-10-04 10:17:32,827.827 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185953-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1762684
2023-10-04 10:17:32,832.832 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 7: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.832448Z)
2023-10-04 10:17:32,832.832 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 6: completed
2023-10-04 10:17:32,903.903 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185956-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 102101
2023-10-04 10:17:32,909.909 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 8: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:32.909266Z)
2023-10-04 10:17:32,909.909 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 7: completed
2023-10-04 10:17:32,937.937 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185957-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 103303
2023-10-04 10:17:33,001.001 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 9: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.001522Z)
2023-10-04 10:17:33,001.001 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 8: completed
2023-10-04 10:17:33,009.009 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 5: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.009335Z)
2023-10-04 10:17:33,011.011 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 4: completed
2023-10-04 10:17:33,023.023 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185958-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 102846
2023-10-04 10:17:33,033.033 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 10: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.033628Z)
2023-10-04 10:17:33,035.035 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185954-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1868840
2023-10-04 10:17:33,036.036 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 9: completed
2023-10-04 10:17:33,061.061 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185959-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 101360
2023-10-04 10:17:33,102.102 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 11: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.102506Z)
2023-10-04 10:17:33,102.102 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 10: completed
2023-10-04 10:17:33,129.129 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185960-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 100342
2023-10-04 10:17:33,171.171 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 12: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.171730Z)
2023-10-04 10:17:33,173.173 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 11: completed
2023-10-04 10:17:33,197.197 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185961-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 98520
2023-10-04 10:17:33,226.226 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 13: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.226648Z)
2023-10-04 10:17:33,227.227 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 12: completed
2023-10-04 10:17:33,236.236 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 6: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.236336Z)
2023-10-04 10:17:33,243.243 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 5: completed
2023-10-04 10:17:33,262.262 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185955-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1805453
2023-10-04 10:17:33,271.271 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185962-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 105987
2023-10-04 10:17:33,322.322 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 14: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.322592Z)
2023-10-04 10:17:33,324.324 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 13: completed
2023-10-04 10:17:33,377.377 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185963-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 104956
2023-10-04 10:17:33,430.430 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 15: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.430328Z)
2023-10-04 10:17:33,430.430 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 14: completed
2023-10-04 10:17:33,442.442 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 7: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.442022Z)
2023-10-04 10:17:33,445.445 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 6: completed
2023-10-04 10:17:33,458.458 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185964-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 99766
2023-10-04 10:17:33,463.463 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185956-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1776850
2023-10-04 10:17:33,509.509 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 16: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.509435Z)
2023-10-04 10:17:33,511.511 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 15: completed
2023-10-04 10:17:33,633.633 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185965-audio.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 100069
2023-10-04 10:17:33,639.639 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 8: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.639391Z)
2023-10-04 10:17:33,643.643 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 7: completed
2023-10-04 10:17:33,661.661 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 16: completed
2023-10-04 10:17:33,664.664 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185957-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1811807
2023-10-04 10:17:33,826.826 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 9: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.826676Z)
2023-10-04 10:17:33,828.828 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 8: completed
2023-10-04 10:17:33,850.850 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185958-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1451015
2023-10-04 10:17:33,994.994 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 10: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:33.994051Z)
2023-10-04 10:17:33,995.995 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 9: completed
2023-10-04 10:17:34,019.019 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185959-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1708892
2023-10-04 10:17:34,192.192 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 11: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:34.192532Z)
2023-10-04 10:17:34,194.194 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 10: completed
2023-10-04 10:17:34,215.215 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185960-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 2003115
2023-10-04 10:17:34,396.396 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 12: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:34.396210Z)
2023-10-04 10:17:34,399.399 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 11: completed
2023-10-04 10:17:34,421.421 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185961-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1879514
2023-10-04 10:17:34,598.598 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 13: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:34.598858Z)
2023-10-04 10:17:34,600.600 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 12: completed
2023-10-04 10:17:34,636.636 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185962-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1966124
2023-10-04 10:17:34,813.813 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 14: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:34.813721Z)
2023-10-04 10:17:34,815.815 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 13: completed
2023-10-04 10:17:34,915.915 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185963-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1732372
2023-10-04 10:17:35,183.183 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 15: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:35.183834Z)
2023-10-04 10:17:35,185.185 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 14: completed
2023-10-04 10:17:35,332.332 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185964-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1932602
2023-10-04 10:17:35,582.582 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 16: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:35.582728Z)
2023-10-04 10:17:35,587.587 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 15: completed
2023-10-04 10:17:35,679.679 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185965-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1711226
2023-10-04 10:17:35,898.898 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 16: completed

2023-10-04 10:17:37,032.032 debug Thread-DASHStreamWorker streamlink.stream.dash Reloading manifest ('0', None, 'video-5')
2023-10-04 10:17:37,033.033 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment initialization: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.033701Z)
2023-10-04 10:17:37,051.051 debug Thread-DASHStreamWorker streamlink.stream.dash Reloading manifest ('0', None, 'audio-5')
2023-10-04 10:17:37,054.054 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment initialization: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.054544Z)
2023-10-04 10:17:37,056.056 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/init-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1280
2023-10-04 10:17:37,057.057 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 1: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.057090Z)
2023-10-04 10:17:37,057.057 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment initialization: completed
2023-10-04 10:17:37,076.076 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/init-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 1208
2023-10-04 10:17:37,076.076 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 1: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.076652Z)
2023-10-04 10:17:37,077.077 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment initialization: completed
2023-10-04 10:17:37,079.079 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185950-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1745420
2023-10-04 10:17:37,100.100 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185950-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 103963
2023-10-04 10:17:37,141.141 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 2: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.141307Z)
2023-10-04 10:17:37,141.141 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 1: completed
2023-10-04 10:17:37,211.211 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185951-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 100474
2023-10-04 10:17:37,212.212 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 3: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.212637Z)
2023-10-04 10:17:37,213.213 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 2: completed
2023-10-04 10:17:37,227.227 debug Thread-DASHStreamWorker urllib3.connectionpool https://dcs-live-uw1.mp.lura.live:443 "GET /server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903 HTTP/1.1" 200 None
2023-10-04 10:17:37,247.247 debug Thread-DASHStreamWorker charset_normalizer Encoding detection: utf_8 is most likely the one.
2023-10-04 10:17:37,257.257 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185952-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 102117
2023-10-04 10:17:37,272.272 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 2: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.272361Z)
2023-10-04 10:17:37,274.274 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 1: completed
2023-10-04 10:17:37,275.275 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 4: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.275781Z)
2023-10-04 10:17:37,276.276 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 3: completed
2023-10-04 10:17:37,280.280 debug Thread-DASHStreamWorker urllib3.connectionpool https://dcs-live-uw1.mp.lura.live:443 "GET /server/play/OV3pDTvQYW5cMWeXW/manifest.mpd?anvsid=m177610521-na549ea847f984f7defa73e3830473903 HTTP/1.1" 200 None
2023-10-04 10:17:37,297.297 debug Thread-DASHStreamWorker charset_normalizer Encoding detection: utf_8 is most likely the one.
2023-10-04 10:17:37,303.303 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185953-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 99864
2023-10-04 10:17:37,305.305 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185951-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1880960
2023-10-04 10:17:37,342.342 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 5: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.342266Z)
2023-10-04 10:17:37,342.342 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 4: completed
2023-10-04 10:17:37,391.391 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185954-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 104877
2023-10-04 10:17:37,496.496 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 3: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.496420Z)
2023-10-04 10:17:37,500.500 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 2: completed
2023-10-04 10:17:37,517.517 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185952-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1749488
2023-10-04 10:17:37,694.694 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 6: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.693999Z)
2023-10-04 10:17:37,694.694 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 5: completed
2023-10-04 10:17:37,699.699 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 4: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.699439Z)
2023-10-04 10:17:37,702.702 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 3: completed
2023-10-04 10:17:37,716.716 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185955-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 100514
2023-10-04 10:17:37,722.722 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185953-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1762684
2023-10-04 10:17:37,749.749 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 7: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.749239Z)
2023-10-04 10:17:37,750.750 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 6: completed
2023-10-04 10:17:37,799.799 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185956-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 102101
2023-10-04 10:17:37,837.837 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 8: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.837639Z)
2023-10-04 10:17:37,837.837 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 7: completed
2023-10-04 10:17:37,886.886 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185957-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 103303
2023-10-04 10:17:37,916.916 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 5: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.916398Z)
2023-10-04 10:17:37,919.919 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 4: completed
2023-10-04 10:17:37,926.926 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 9: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.926446Z)
2023-10-04 10:17:37,926.926 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 8: completed
2023-10-04 10:17:37,937.937 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185954-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1868840
2023-10-04 10:17:37,950.950 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185958-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 102846
2023-10-04 10:17:37,994.994 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 10: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:37.994961Z)
2023-10-04 10:17:37,995.995 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 9: completed
2023-10-04 10:17:38,042.042 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185959-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 101360
2023-10-04 10:17:38,130.130 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 6: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.130829Z)
2023-10-04 10:17:38,132.132 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 5: completed
2023-10-04 10:17:38,154.154 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185955-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1805453
2023-10-04 10:17:38,316.316 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 7: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.316477Z)
2023-10-04 10:17:38,320.320 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 6: completed
2023-10-04 10:17:38,320.320 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 11: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.320806Z)
2023-10-04 10:17:38,322.322 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 10: completed
2023-10-04 10:17:38,338.338 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185956-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1776850
2023-10-04 10:17:38,345.345 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185960-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 100342
2023-10-04 10:17:38,390.390 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 12: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.390485Z)
2023-10-04 10:17:38,390.390 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 11: completed
2023-10-04 10:17:38,437.437 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185961-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 98520
2023-10-04 10:17:38,459.459 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 13: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.459783Z)
2023-10-04 10:17:38,460.460 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 12: completed
2023-10-04 10:17:38,508.508 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185962-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 105987
2023-10-04 10:17:38,517.517 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 14: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.517094Z)
2023-10-04 10:17:38,517.517 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 13: completed
2023-10-04 10:17:38,529.529 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 8: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.529086Z)
2023-10-04 10:17:38,530.530 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 7: completed
2023-10-04 10:17:38,538.538 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185963-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 104956
2023-10-04 10:17:38,546.546 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 15: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.546356Z)
2023-10-04 10:17:38,546.546 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 14: completed
2023-10-04 10:17:38,551.551 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185957-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1811807
2023-10-04 10:17:38,571.571 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185964-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 99766
2023-10-04 10:17:38,614.614 debug ThreadPoolExecutor-1_0 streamlink.stream.dash audio/mp4 segment 16: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.614774Z)
2023-10-04 10:17:38,616.616 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 15: completed
2023-10-04 10:17:38,637.637 debug ThreadPoolExecutor-1_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185965-audio.mp4?hdntl=exp=1696436252~acl=/*~hmac=742d6a4186669e0f5e94a3dfdb4b34ca9f7e64a0b058a651da3b51b138c7b5a2 HTTP/1.1" 200 100069
2023-10-04 10:17:38,682.682 debug Thread-DASHStreamWriter streamlink.stream.dash audio/mp4 segment 16: completed
2023-10-04 10:17:38,747.747 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 9: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.747640Z)
2023-10-04 10:17:38,749.749 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 8: completed
2023-10-04 10:17:38,772.772 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185958-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1451015
2023-10-04 10:17:38,901.901 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 10: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:38.901147Z)
2023-10-04 10:17:38,904.904 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 9: completed
2023-10-04 10:17:38,922.922 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185959-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1708892
2023-10-04 10:17:39,094.094 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 11: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:39.093988Z)
2023-10-04 10:17:39,095.095 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 10: completed
2023-10-04 10:17:39,122.122 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185960-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 2003115
2023-10-04 10:17:39,304.304 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 12: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:39.304407Z)
2023-10-04 10:17:39,309.309 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 11: completed
2023-10-04 10:17:39,327.327 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185961-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1879514
2023-10-04 10:17:39,495.495 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 13: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:39.495373Z)
2023-10-04 10:17:39,497.497 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 12: completed
2023-10-04 10:17:39,518.518 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185962-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1966124
2023-10-04 10:17:39,696.696 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 14: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:39.696014Z)
2023-10-04 10:17:39,700.700 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 13: completed
2023-10-04 10:17:39,722.722 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185963-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1732372
2023-10-04 10:17:39,876.876 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 15: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:39.876885Z)
2023-10-04 10:17:39,879.879 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 14: completed
2023-10-04 10:17:39,901.901 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185964-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1932602
2023-10-04 10:17:40,090.090 debug ThreadPoolExecutor-0_0 streamlink.stream.dash video/mp4 segment 16: downloading (2023-10-04T10:16:26.000000Z / 2023-10-04T10:17:40.090599Z)
2023-10-04 10:17:40,093.093 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 15: completed
2023-10-04 10:17:40,118.118 debug ThreadPoolExecutor-0_0 urllib3.connectionpool https://video-live.dpgmedia.net:443 "GET /live/ephemeral/Py1vlQKiKkE3miEiwpD10CMNeZELWKVq/vtm4-x-dist/4792k/ugSxF45MOHE/178185/segment_178185965-video.mp4?hdntl=exp=1696436251~acl=/*~hmac=2d5245e3f99f770856f92b33d2c6c8359bfc814f51848980a7d9bf313a5b9e68 HTTP/1.1" 200 1711226
2023-10-04 10:17:40,271.271 debug Thread-DASHStreamWriter streamlink.stream.dash video/mp4 segment 16: completed
```
