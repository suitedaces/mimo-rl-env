Occasional calls to history API returning excess entries
### SABnzbd version

4.5.2

### Operating system

Unraid/Docker

### Using Docker image

linuxserver

### Description

Every so often, a call to the SAB history API has been returning two entries for the same NZO_ID, with both of them marked as a status of "Completed" but one of them missing the storage path.  Calling the API again shortly after returns only the one entry (the second slot).  Apologies if I'm misunderstanding and this is an intentional response, but I assumed that for a Completed download it should have one history entry and know the final destination.

I can't consistently reproduce the timing that results in this happening, but am getting it in around 1/100 loops of post processing from mylar when it checks the history queue.

```json
{
   "history":{
      "total_size":"14.8 T",
      "month_size":"412.8 G",
      "week_size":"40.9 G",
      "day_size":"14.9 G",
      "slots":[
         {
            "completed":1752669335,
            "name":"Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire",
            "nzb_name":"Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire.nzb",
            "category":"comics",
            "pp":"D",
            "script":"Default",
            "report":"",
            "url":"http://servermonkey3.home.arpa:8090/api?apikey=--REDACTED--&cmd=downloadNZB&nzbname=Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire.nzb",
            "status":"Completed",
            "nzo_id":"SABnzbd_nzo_h4h4kvnz",
            "storage":"",
            "path":"/media/downloads/usenet/incomplete/Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire",
            "script_line":"",
            "download_time":3,
            "postproc_time":0,
            "stage_log":[
               {
                  "name":"Source",
                  "actions":[
                     "http://servermonkey3.home.arpa:8090/api?apikey=--REDACTED--&cmd=downloadNZB&nzbname=Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire.nzb"
                  ]
               },
               {
                  "name":"Download",
                  "actions":[
                     "Downloaded in 3 seconds at an average of 14.2 MB/s<br/>Age: 3680d"
                  ]
               },
               {
                  "name":"Servers",
                  "actions":[
                     "news.usenetserver.com=46.9 MB"
                  ]
               },
               {
                  "name":"Repair",
                  "actions":[
                     "[Angela-Asgards.Assassin.004.(2015).(Digital).(Zone-Empire)] Quick Check OK",
                     "Trying RAR renamer"
                  ]
               }
            ],
            "downloaded":49282231,
            "completeness":"None",
            "fail_message":"",
            "url_info":"",
            "bytes":49282231,
            "size":"47.0 MB",
            "meta":"None",
            "series":"",
            "duplicate_key":"angela",
            "md5sum":"",
            "password":"None",
            "action_line":"Moving: Angela - Asgard's Assassin 004 (2015) (Digital) (Zone-Empire).cbr",
            "loaded":false,
            "retry":false,
            "archive":false
         },
         {
            "completed":1752669335,
            "name":"Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire",
            "nzb_name":"Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire.nzb",
            "category":"comics",
            "pp":"D",
            "script":"Default",
            "report":"",
            "url":"http://servermonkey3.home.arpa:8090/api?apikey=--REDACTED--&cmd=downloadNZB&nzbname=Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire.nzb",
            "status":"Completed",
            "nzo_id":"SABnzbd_nzo_h4h4kvnz",
            "storage":"/media/downloads/usenet/comics/Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire/Angela - Asgard's Assassin 004 (2015) (Digital) (Zone-Empire).cbr",
            "path":"/media/downloads/usenet/incomplete/Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire",
            "script_line":"",
            "download_time":3,
            "postproc_time":0,
            "stage_log":[
               {
                  "name":"Source",
                  "actions":[
                     "http://servermonkey3.home.arpa:8090/api?apikey=--REDACTED--&cmd=downloadNZB&nzbname=Angela.-.Asgards.Assassin.004.2015.Digital.Zone-Empire.nzb"
                  ]
               },
               {
                  "name":"Download",
                  "actions":[
                     "Downloaded in 3 seconds at an average of 14.2 MB/s<br/>Age: 3680d"
                  ]
               },
               {
                  "name":"Servers",
                  "actions":[
                     "news.usenetserver.com=46.9 MB"
                  ]
               },
               {
                  "name":"Repair",
                  "actions":[
                     "[Angela-Asgards.Assassin.004.(2015).(Digital).(Zone-Empire)] Quick Check OK",
                     "Trying RAR renamer"
                  ]
               }
            ],
            "downloaded":49282231,
            "completeness":"None",
            "fail_message":"",
            "url_info":"",
            "bytes":49282231,
            "meta":"None",
            "series":"None",
            "md5sum":"798feef96d14b4d612286f08abc969f8",
            "password":"None",
            "duplicate_key":"angela",
            "archive":false,
            "size":"47.0 MB",
            "action_line":"",
            "loaded":false,
            "retry":false
         }
      ],
      "ppslots":1,
      "noofslots":1,
      "last_history_update":15933,
      "version":"4.5.2"
   }
}
```
