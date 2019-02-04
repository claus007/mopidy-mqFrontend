******************
Mopidy-mqFrontend
******************

This is a bridge between mopidy and a mosquitto server.

States where send out to mosquitto.

Mopidy listens on control commands.

Intention is an easy integration into home automation programs like openhab.

Therefore you *can*:
    * Start/Stop/Pause playback
    * Play playlist
    
Therfore you *can't*:
    * Edit/Modify playlists

Last but not least there is one message which you can use to keep your speaker
turned on - it is send in an aquidistant interval like a heartbeat.

Please, execuse me if I go not so deep into details but this extension
is still under development and some things may change...

Nevertheless you can try it !
Look at the license.

So long - hope it helps you!

Running on Ubuntu
=========================

Get it
-------------------

    git clone https://github.com/claus007/mopidy-mqFrontend.git

    cd mopidy-mqFrontend
    
    sudo service mopidy stop

    sudo python setup.py install

Configuration
-------------
Edit section mqfrontend in mopidy.conf according to your settings with:

>    sudo vi /etc/mopidy/mopidy.conf

For exact parameter description see: [Parameters.txt](docs/parameters.txt) or run:

``#import mopidy_mqFrontend.configdefinition``

``a=mopidy_mqFrontend.configdefinition.parameters_help()``

``print a``


Testing
-------
    sudo service mopidy restart

If you did everything well you can test if everything works fine.
(Assuming that most of the settings are defaults)

Receiving messages from mopidy:

    mosquitto_sub -v --topic mopidy/#

Sending commands:

    mosquitto_pub -v -m "play" -t mopidy/control

Structure
=========

I changed the structure drastically.
Instead of owning I turned to inheritance.
So:

Extension produces:

   MainActor
        -> ControlSubscriber
                -> Statuspublisher
                        -> MosquittoClientBase
                                -> pykka.ThreadingActor

Project resources
=================

- `Source code <https://github.com/claus007/mopidy-mqFrontend>`_
- `Issue tracker <https://github.com/claus007/mopidy-mqFrontend/issues>`_
- `Development branch tarball <https://github.com/claus007/mopidy-mqFrontend/tarball/master#egg=Mopidy-mqFrontend-dev>`_

