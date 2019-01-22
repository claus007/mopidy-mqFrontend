******************
Mopidy-mqFrontend
******************

This is a bridge between mopidy and a mosquitto server.

States where send out to mosquitto.

Mopidy listens on control commands. (not yet working)

The standard topic is mopidy but you can configure anything
you want. There are different sub topics for the state changes and
for controlling there is one sub topic called "control".

Intension is an easy integration into home automation programs like openhab.

Last but not least there is one message which you can use to keep your speaker
turned on - it is send in an aquidistant intervall like a heratbeat.

Please, execuse me if I go not so deep into details but this extension
is still under heavy development and many things will change...

Nevertheless you can try it if you want to of course on your own risk.
Look at the license.

So long - hope it helps you!

Running
=========================

Install by cloning:
-------------------

    git clone https://github.com/claus007/mopidy-mqFrontend.git

    cd mopidy-mqFrontend

    sudo python setup.py install

Configuration
-------------

Parameters are:

    enable      true if extension is enabled
    
    path        topic under which this control is published (default: mopidy)
    
    host        host to connect to (default: localhost)
    
    port        port on host (default:1883)

Testing
=======

If you did everything well you can test if everything works fine.
(Assuming that most of the settings are defaults)

Receiving messages from mopidy:

    mosquitto_sub -v --topic mopidy/#

Sending:

    mosquitto_pub -v -m "play" -t mopidy/control

Structure
=========

+Extension

   +Mainactor

     +Statuspublisher

        +EventTranslator

     +ControlerSubscriber

Project resources
=================

- `Source code <https://github.com/claus007/mopidy-mqFrontend>`_
- `Issue tracker <https://github.com/claus007/mopidy-mqFrontend/issues>`_
- `Development branch tarball <https://github.com/claus007/mopidy-mqFrontend/tarball/master#egg=Mopidy-mqFrontend-dev>`_

