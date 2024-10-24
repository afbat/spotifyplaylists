# spotifyplaylists
## About

I really love making playlists, but I'm also really lazy about it. For many years, I relied on IFTTT to automatically generate monthly playlists based on songs that I 'liked' during a monthly period. So liking songs has very much become ingrained in how I utilize Spotify in terms of engaging in 'liking' behavior as a deliberate mechanism of playlist creation.

Last year, IFTTT started charging for this applet and apparently I'm also pretty cheap too when it comes to playlist making (I mean, as one should be...). So as an attempt to improve my python skills while productively procrastinating my dissertation, and also cope with no longer having a playlist output from all these now-normalized 'like' responses,  I decided to mess around with `spotipy`.

Lastly, this is one of several 'fun' projects that I have been playing with in my free time for the purpose of improving my python skills. Sure, it essentially picks up an established practiced that I have had for the last ten years, in terms of shaping my engagement with the Spotify's interface with the specific intention of adding content through what is going on on the back end. These are habits that are difficult to break once deeply embedded into a technology relationship and routine. But more so, this is part of a larger trend in which I push myself to think more computationally about the problems, tedious and repetitive tasks, or ones that are just take up too much time in a packed schedule. As a result, I push myself to try new things and improve skills that will make my research easier (and sometimes a little more fun) in the process. 

## What it can do
- creates and/or updates a playlist for the current month
    - goes through and checks if there's already a playlist for this month and year
        - if there's not, it makes one
    - then it goes through and identifies all the songs that were 'liked' during that month and year
        - if there's already a playlist, it checks for duplicates and skips those
    - then it adds all the non-duplicate songs that were liked during that month and year period
- creates and/or updates a playlist for the previous month (because sometimes I'm really bad about remembering to actually run it)
    - goes through and checks if there's already a playlist for last month and the current year
        - if the current month is January, then it checks for the December with the previous year
        - if there's not a playlist for the previous month, then it makes one
    - then it goes through and identifies all the songs that were 'liked' during the previous month
        - if there's already a previous month playlist, it checks for duplicates and skips those
    - then it adds all the non-duplicate songs that were liked during last month

## What it can't do (yet)
- can not run automatically or update in the background
    - my goal is to figure out how to not have to run this manually every month. I'll probably end up using some combo of cron jobs and selenium but honestly haven't spent a lot of time thinking about it. That will probably take a backseat to my actual work like writing code relevant to my dissertation.
- probably a lot of other things that other people care about, and I probably do too, but haven't realized because I'm so focused on replacing my IFTTT-Spotify flow

## Running it

I need to write this out in some detail but the basics are:
  - go to <a href ="https://developer.spotify.com/dashboard"> Spotify Deverloper Dashboard </a>
    - 'Create App'
    - Set App Status to 'Development Mode'
    - Set App Name (I just called it 'playlist builder')
    - Set App Description (I just put 'generate monthly playlists')
    - Set Redirect URL: https://localhost:8888/callback
  _From this you will be able to retrieve your 'client id' and 'client secret'_
  - open '/bin/auth.py'
    - put your 'client id' from the deverloper dash into 'client_id'
    - put your 'client secret' into 'client_secret'
  - open playlist-env (I just launch it in terminal)
  - run `pip install -r requirements.txt`
    - you may need to modify this further based on what you have installed already
  - open `/bin/activate.csh` and set the path for your virtual environment under `setenv VIRTUAL_ENV`
  - `spotipy_test.py` is from `spotipy`'s materials to test
  - run `update.py` and this will create a playlist for the current month if there isn't one yet, and then add all songs that you liked during that month. Or if there's already a playlist, it will update any songs that don't already appear for the current month. It will do this for the previous month as well.



 Anyway, still working out a bunch of kinks with it and learning along the way, so always welcome to feedback!
