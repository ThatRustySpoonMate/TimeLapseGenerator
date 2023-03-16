<h1>MP4 Video to Timelapse MP4 Video Converting Utility</h1>
<hr>
<br>
<h2>How to use</h2>
<ol>
    <li>Put your mp4 file to convert in the same directory as the script.</li>
    <li>Open the script directory in a command prompt/PowerShell window.</li>
    <li>Run the script and pass it relevant parameters as so:</li>
    <p style="margin-left: 40px;"> >Python VTTL src_path.mp4 ram_hdd_mode frame_rate speed_multiplier</p>
    <p style="margin-left: 40px;">frame_rate determines the  is the relative or absolute path to the mp4 source file</p>
    <p style="margin-left: 40px;">int: ram_hdd_mode determines if the video conversion will buffer frames in ram or the filesystem (0 = RAM, 1 = HDD) </p>
    <p style="margin-left: 40px;">int: frame_rate determines the output file frame rate</p>
    <p style="margin-left: 40px;">float: speed_multiplier takes into account the source frame rate, output desired frame rate, number of frames in the source video and will speed the video up by this amount.</p>
</ol>

<p>The script will then start converting the source video into a timelapse and will show progress indicators. <strong >NOTE: Source video will NOT be deleted once the video is converted.</strong> </p>
